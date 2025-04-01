from fastapi import FastAPI, Request, BackgroundTasks, HTTPException
from fastapi import FastAPI, Request, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from strawberry.fastapi import GraphQLRouter
from fastapi.responses import JSONResponse
import strawberry
import logging
import uvicorn
import time
import json
import os
from datetime import datetime
import uuid
import json
import os
from datetime import datetime
import uuid

# TODO: import the ml and the crawler services
from src.modules.ai.credential_generator import Credential_Generator
from src.modules.ai.web_scraper import WebScraper
from src.modules.scanning.crawler_manager import crawler_manager

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Job tracking
running_jobs = {}
job_results = {}

# Pydantic model for crawler configuration
class CrawlerConfig(BaseModel):
    target_url: str
    depth: Optional[int] = 1
    limit: Optional[int] = 100
    user_agent: Optional[str] = "Mozilla/5.0"
    delay: Optional[int] = 1000
    proxy: Optional[str] = None
    excluded_urls: Optional[str] = None
    crawl_date: Optional[str] = None
    crawl_time: Optional[str] = None

    # Handles formatting data from fronted.
    class Config:
        alias_generator = lambda field_name: field_name.replace('_', '-')
        populate_by_name = True
        
    # This method logs the received data
    @classmethod
    def debug_request(cls, data: dict):
        logger.info(f"Raw request data: {data}")
        for key, value in data.items():
            logger.info(f"Field: {key}, Value: {value}, Type: {type(value)}")
        return data
    
# Pydantic model for ml algorithm configuration
class MLAlgorithmConfig(BaseModel):
    # TODO: add the different variables that will be passed.
    target_url: str

    # Handles formatting data from fronted.
    class Config:
        alias_generator = lambda field_name: field_name.replace('_', '-')
        populate_by_name = True
        
    # TODO: Add the section to handle formatting the data that is given from the frontend.
    # This method logs the received data
    @classmethod
    def debug_request(cls, data: dict):
        logger.info(f"Raw request data: {data}")
        for key, value in data.items():
            logger.info(f"Field: {key}, Value: {value}, Type: {type(value)}")
        return data

# Response model for crawler job status
class CrawlerJobResponse(BaseModel):
    job_id: str
    message: str
    status: str
    progress: Optional[float] = None
    urls_processed: Optional[int] = None
    total_urls: Optional[int] = None

# Pydantic model for crawler results
class CrawlerResultItem(BaseModel):
    id: int
    url: str
    parentUrl: Optional[str] = None
    title: str
    wordCount: int
    charCount: int
    linksFound: int
    error: bool

class CrawlerResults(BaseModel):
    results: List[CrawlerResultItem]

#Response model for ml algorithm job status.
class MLAlgorithmJobResponse(BaseModel):
    job_id: str
    message: str
    status: str
    # TODO: Could add the percentage and other information to be passed.

# GraphQL Schema Definitions
@strawberry.type
class CrawlerResult:
    url: str
    title: str
    parent_url: Optional[str] = None
    word_count: int
    char_count: int
    links_found: int
    error: bool

@strawberry.type
class Query:
    @strawberry.field
    def get_crawler_results(self, job_id: str) -> List[CrawlerResult]:
        if job_id in job_results and os.path.exists(f'crawler_results_{job_id}.json'):
            try:
                with open(f'crawler_results_{job_id}.json') as file:
                    data = json.load(file)
                    return [
                        CrawlerResult(
                            url=item['url'],
                            title=item['title'],
                            parent_url=item['parentUrl'],
                            word_count=item['wordCount'],
                            char_count=item['charCount'],
                            links_found=item['linksFound'],
                            error=item['error'],
                        ) for item in data
                    ]
            except Exception as e:
                logger.error(f'Error reading crawler results: {e}')
                return []
        return []
    
    @strawberry.field
    def get_job_status(self, job_id: str) -> str:
        if job_id in running_jobs:
            return running_jobs[job_id]['status']
        if job_id in job_results:
            return 'completed'
        return 'not found!'


# Setup GraphQL Schema
schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema)

# Create FastAPI App
app = FastAPI(title="Team 7 API")

# Configure CORS to allow requests from SvelteKit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # Adjust as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(graphql_app, prefix="/graphql")

# TODO: Think about moving this to another file.
# Background task to run the crawler
async def run_crawler_task(job_id: str, config: CrawlerConfig):
    try:
        running_jobs[job_id]['status'] = 'running'

        # Start the crawler manager
        crawler = crawler_manager()
        crawler.configure_crawler(
            target_url=config.target_url,
            depth=config.depth,
            limit=config.limit,
            user_agent=config.user_agent,
            delay=config.delay,
            proxy=config.proxy,
            crawl_date=config.crawl_date or datetime.now().strftime("%m-%d-%Y"),
            crawl_time=config.crawl_time or datetime.now().strftime('%H:%M'),
            excluded_urls=config.excluded_urls or "",
        )

        results = await(crawler.start_crawl())

        # Save the results
        if os.path.exists('crawler_table_data.json'):
            with open('crawler_table_data.json', 'r') as file:
                table_data = json.load(file)
            
            # Add the job id to the results
            with open(f'crawler_resullts_{job_id}.json', 'w') as file:
                json.dump(table_data, file, indent=4)
            
            # Change the status
            job_results[job_id] = {
                "status": 'completed',
                'results_file': f'crawler_results_{job_id}.json',
                'urls_processed': len(table_data),
                'completed_at': datetime.now().isoformat()
            }

        # Remove from the running jobs list
        if job_id in running_jobs:
            del running_jobs[job_id]

        logger.info(f'Cralwer job {job_id} completed')
    
    except Exception as e:
        if job_id in running_jobs:
            running_jobs[job_id]['status'] = 'error'
            running_jobs[job_id]['error'] = str(e)

        logger.error(f'Error: crawler job id {job_id}: {e}')

# Crawler endpoints.
@app.post("/api/crawler", response_model=CrawlerJobResponse)
async def start_crawler(config: CrawlerConfig, background_tasks: BackgroundTasks):
    logger.info(f'Received Crawler configuration: {config}')

    # Create a new job id
    job_id = str(uuid.uuid4())

    running_jobs[job_id] = {
        'status': 'idle',
        'created_at': datetime.now().isoformat(),
        'config': config.model_dump()
    }

    # Start in background
    background_tasks.add_task(run_crawler_task, job_id, config)

    return CrawlerJobResponse(
        job_id=job_id,
        message='Crawler started successfully!',
        status='idle'
    )

@app.get('/api/crawler/{job_id}', response_model=CrawlerJobResponse)
async def get_crawler_status(job_id: str):
    # Check job
    if job_id in running_jobs:
        job = running_jobs[job_id]
        return CrawlerJobResponse(
            job_id=job_id,
            message='Crawler job is in progress',
            status=job['status'],
            urls_processed=job.get('urls_processed', 0),
            total_urls=job.get('total_urls', 0),
            progress=job.get('progress', 0)
        )
    
    # If not running check if complete
    if job_id in job_results:
        job = job_results[job_id]
        return CrawlerJobResponse(
            job_id=job_id,
            message='Crawler job is finished',
            status=job['status'],
            urls_processed=job.get('urls_processed', 0),
            total_urls=job.get('total_urls', 0),
            progress=job.get('progress', 0)
        )
    
    raise HTTPException(status_code=404, detail=f'Job {job_id} not found')

@app.get('/api/crawler/{job_id}/results', response_model=CrawlerResult)
async def get_crawler_results(job_id: str):
    # Check if ccompleted
    if job_id in job_results and os.path.exists(f'crawler_results_{job_id}.json'):
        try:
            with open(f'crawler_results_{job_id}.json', 'r') as file:
                data = json.load(file)
                return CrawlerResults(results=data)
        except Exception as e:
            logger.error(f'Error reading crawler results: {e}')
            raise HTTPException(status_code=500, detail="Error reading results for crawler")
        
    # Will raise if the file isn't found or if the job isn't completed
    raise HTTPException(status_code=404, detail=f'Results for job {job_id} not found')

# ML endpoints.
@app.post("/api/ml_algorithm")
async def receive_ml_data(config: MLAlgorithmConfig):
    logger.info(f"Received ML Algorithm configuration: {config}")
    
    # Scrape the target URL
    # TODO: Update to be the correct target url
    scraper = WebScraper(urls=[config.target_url])
    scraped_data = scraper.scrape_pages()

    # Save the Scraped data to database
    # TODO: Update to save it to the correct database, for now a csv file
    csv_path = "./src/database/scraped_data.csv"

    # Initialize and run credential generator
    # TODO: Update utilize the count that the user has passed.
    generator = Credential_Generator(csv_path=csv_path)
    credentials = generator.generate_credentials(count=10)
    
    return {
        "job_id": "ml_" + str(int(time.time())),
        "status": "success",
        "message": f"Generated {len(credentials)} credentials from {config.target_url}",
        "credentials": [
            {"username": u, "password": p} for u, p in credentials
        ]
    }

@app.get("/")
async def root():
    return {"message": "API is running. Access /docs for documentation."}

# For debugging - print raw request body
@app.post("/api/debug")
async def debug_endpoint(request: Request):
    body = await request.body()
    logger.info(f"Raw request body: {body}")
    try:
        json_body = await request.json()
        logger.info(f"JSON body: {json_body}")
        return {"received": json_body}
    except Exception as e:
        logger.error(f"Error parsing JSON: {e}")
        return {"error": str(e), "raw_body": body.decode()}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)