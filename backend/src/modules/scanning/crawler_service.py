import logging
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import asyncio
import os
import json

from src.modules.scanning.crawler_manager import crawler_manager

# set up the logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Track the different Jobs
running_jobs = {}
# Format: {job_id: {status, created_at, config, progress, urls_processed, total_urls, logs}}
job_results = {}
# Format: {job_id, {status, result_file, urls_processed, completed_at, logs}}
active_connections = {}
# Format: {job_id: {websocket1, websocket2,...}}

# Pydantic models
class CrawlerConfig(BaseModel):
    """
    Configuration model for crawler jobs
    """
    target_url: str
    depth: Optional[int] = 1
    limit: Optional[int] = 100
    user_agent: Optional[str] = "Mozilla/5.0"
    delay: Optional[int] = 1000
    proxy: Optional[str] = None
    excluded_urls: Optional[str] = None
    crawl_date: Optional[str] = None
    crawl_time: Optional[str] = None

    # Handles any formatted issues from the frontend
    class Config:
        alias_generator = lambda field_name: field_name.replace('_', '-')
        populate_by_name = True

    # Log the received data from frontend
    def debug_request(cls, data: dict):
        logger.info(f'Raw request data: {data}')
        for key, value in data.items():
            logger.info(f'Field: {key}, Value: {value}, Type: {type(value)}')
        return data
    
class CrawlerJobResponse(BaseModel):
    """
    Response model for crawler job status.
    """
    job_id: str
    message: str
    status: str
    progress: Optional[float] = 0
    urls_processed: Optional[int] = 0
    total_urls: Optional[int] = 0

class CrawlerResultItem(BaseModel):
    """
    Model for a single crawler result item.
    """
    id: int
    url: str
    parentUrl: Optional[str] = None
    title: str
    wordCount: int
    charCount: int
    linksFound: int
    error: bool

class CrawlerResults(BaseModel):
    """
    Model for the complete crawler results
    """
    results: List[CrawlerResultItem]

class CrawlerProgressTracker:
    """
    Tracks progress of a crawler job and broadcasts updates through the websockets
    """
    def __init__(self, job_id):
        self.job_id = job_id
        self.visited_urls = set()
        self.total_processed = 0
        self.logs = []

    def add_log(self, message):
        """
        Add a log message and broadcast it to the connected clients
        """
        timestamp = datetime.now().strftime('%m-%d-%Y %H:%M:%S')
        log_entry = f'[{timestamp}] {message}'
        self.logs.append(log_entry)

        # Update the logs in running_jobs
        if self.job_id in running_jobs:
            running_jobs[self.job_id]['logs'] = self.logs
        logger.info(f'Job {self.job_id}: {message}')

        # Broadcast the log message to the other connected  websockets
        self._broadcast_message('log', {'message': log_entry})

    def update_progress(self, url=None, error=None):
        self.visited_urls.add(url)
        self.total_processed += 1

        # Update the job status of the current running job
        if self.job_id in running_jobs:
            limit = running_jobs[self.job_id].get('total_urls', 100)
            progress = min(int(self.total_processed / max(1, limit) * 1000), 99)

            running_jobs[self.job_id].update({
                'urls_processed': self.total_processed,
                'progress': progress
            })

            # Broadcast progress update to the connected websockets
            self._broadcast_message('progress', {
                'urls_processed': self.total_processed,
                'progress': progress,
                'total_urls': limit,
                'current_url': url
            })

        if error:
            self.add_log(f'Error processing {url}: {error}')
        else:
            self.add_log(f'processed: {url}')

    def set_status(self, status):
        """
        Set job status and broadcast to connected clients."""
        if self.job_id in running_jobs:
            running_jobs[self.job_id]['status'] = status
            self.add_log(f'Job status changed to: {status}')

            # Broadcast the status update to the connected websockets
            self._broadcast_message('status', {'status': status})

    def _broadcast_message(self, message_type, data):
        """
        Broadcast a message to all the connected clients through the websockets.
        """
        message = {
            'type': message_type,
            'job_id': self.job_id,
            'data': data
        }

        # Send it to all the clients
        if self.job_id in active_connections:
            for websocket in active_connections[self.job_id]:
                asyncio.create_task(websocket.send_json(message))

async def run_crawler_task(job_id: str, config: CrawlerConfig):
    """
    Run a crawler job asnychronously and update state.
    """
    # Create the progress tracker
    tracker = CrawlerProgressTracker(job_id)
    tracker.add_log(f'Starting cralwwer job with config: {config.model_dump()}')

    try:
        # Update job status
        tracker.set_status('running')
        running_jobs[job_id]['started_at'] = datetime.now().isoformat()

        # Initialize crawler manager
        crawler = crawler_manager()

        # TODO: Has default values, see if front end does this to remove it.
        # Config the Crawler
        crawler.configure_crawler(
            target_url=config.target_url,
            depth=config.depth or 3,
            limit=config.limit or 100,
            user_agent=config.user_agent or 'Mozilla/5.0',
            delay=config.delay or 1000,
            proxy=config.proxy or '',
            crawl_date=config.crawl_date or datetime.now().strftime('%m-%d-%Y'),
            crawl_time=config.crawl_time or datetime.now().strftime('%H:%M'),
            excluded_urls=config.excluded_urls or ''
        )

        tracker.add_log('Crawler config successfully')

        # Custom progress callback function
        def progress_callback(url, error=None):
            tracker.update_progress(url, error)

        # Add progress callback to the crawler manager 
        crawler.progress_callback = progress_callback

        # Start the crawler
        tracker.add_log('Starting crawler execution')
        results = await crawler.start_crawl()
        tracker.add_log('Crawler execution completed')

        # Save the results with the job id so it can be identified
        # TODO: update this to work correctly
        if os.path.exists("./crawler_table_data.json"):
            with open("crawler_table_data.json", 'r') as file:
                table_data = json.load(file)


            # Save the results in a new location with id
            result_file = f'crawler_results_{job_id}.json'
            with open(result_file, 'w') as file:
                json.dump(table_data, file, indent=2)

            tracker.add_log(f'Results saved to {result_file}')

            # Update job status
            job_results[job_id] = {
                'status': 'completed',
                'results_file': result_file,
                'urls_processed': len(table_data),
                'completed_at': datetime.now().isoformat(),
                'total_urls': len(table_data),
                'logs': tracker.logs,
            }

            # Broadcast completion message
            tracker._broadcast_message('complete', {
                'urls_processed': len(table_data),
                'total_urls': len(table_data),
                'message': 'Crawler job completed successfully'
            })
        
        else:
            tracker.add_log('No results data file found')
            job_results[job_id] = {
                'status': 'completed',
                'message': 'No results data file found!',
                'urls_processed': tracker.total_processed,
                'completed_at': datetime.now().isoformat(),
                'logs': tracker.logs
            }

            # Broadcast message with error
            tracker._broadcast_message('complete', {
                'urls_processed': tracker.total_processed,
                'message': 'Crawler job completed with no results file'
            })

        # Remove this test from running jobs
        if job_id in running_jobs:
            del running_jobs[job_id]

        tracker.add_log(f'Job {job_id} completed without errors..')

    except Exception as e:
        error_message = f'Eroor in crawler job: {str(e)}'
        logger.error(f'Error in crawler job {job_id}: {e}')
        tracker.add_log(error_message)

        # Broadcast the error message
        tracker._broadcast_message('error', {
            'message': error_message,
        })

        # Update job status to error
        if job_id in running_jobs:
            running_jobs[job_id]['status'] = 'error'
            running_jobs[job_id]['error'] = error_message

            # Move the job to job_results
            job_results[job_id] = {
                'status': 'error',
                'error': error_message,
                'urls_processed': tracker.total_processed,
                'completed_at': datetime.now().isoformat(),
                'logs': tracker.logs
            }

            # Remove from the running_jobs list
            del running_jobs[job_id]