from fastapi import APIRouter, BackgroundTasks, HTTPException, WebSocket, WebSocketDisconnect
import logging
import json
import uuid
from datetime import datetime
import os

# Import the service modules
from src.modules.scanning.crawler_service import (
    CrawlerConfig,
    CrawlerJobResponse,
    CrawlerResults,
    running_jobs,
    crawler_instances,
    job_results,
    active_connections,
    run_crawler_task,
    get_job_status_message,
    get_job_logs
)

# Set up log
logger = logging.getLogger(__name__)

# Create the routes for the different services
crawler_router = APIRouter(prefix='/api/crawler', tags=['crawler'])

# Websocket handler for the crawler service
async def handle_crawler_websocket(websocket: WebSocket, job_id: str):
    print(f'[Backend] Websocket connection opened for job: {job_id}')

    await websocket.accept()

    print('Active jobs after accept:', list(running_jobs.keys()))

    # Register the connection
    if job_id not in active_connections:
        active_connections[job_id] = []
    active_connections[job_id].append(websocket)

    try:
        #Send a status message
        initial_status = get_job_status_message(job_id)
        await websocket.send_json(initial_status)

        while True:
            message = await websocket.receive_text()
            try: 
                data = json.loads(message)

                if data.get('type') == 'command':
                    command = data.get('command')
                    
                    if command == 'get_logs':
                        logs = get_job_logs(job_id)
                        await websocket.send_json({
                            'type': 'logs',
                            'job_id': job_id,
                            'data': {'logs': logs}
                        })
            
            except json.JSONDecodeError:
                logger.error(f'Received invalid JSON from client: {message}')
    
    except WebSocketDisconnect:
        # If disconnected remove the connection from list
        if job_id in active_connections and websocket in active_connections[job_id]:
            active_connections[job_id].remove(websocket)
            if not active_connections[job_id]:
                del active_connections[job_id]

        logger.info(f'Websocket disconnect for job: {job_id}, job stopped')

    except Exception as e:
        logger.error(f'Error in Websocket connection for job {job_id}: {str(e)}')

        if job_id in active_connections and websocket in active_connections[job_id]:
            active_connections[job_id].remove(websocket)
            if not active_connections[job_id]:
                del active_connections[job_id]

# Crawler API endpoints
@crawler_router.post('', response_model=CrawlerJobResponse)
async def start_crawler(config: CrawlerConfig, background_tasks: BackgroundTasks):
    logger.info(f'Received crawler configuration: {config}')

    # Generate a uniques job ID
    job_id = str(uuid.uuid4())

    # Register the job
    running_jobs[job_id] = {
        'status': 'initializing',
        'created_at': datetime.now().isoformat(),
        'progress': 0,
        'urls_processed': 0,
        'total_urls': config.limit or 0,
        'logs': []
    }

    # Start crawler in background
    background_tasks.add_task(run_crawler_task, job_id, config)

    return CrawlerJobResponse(
        job_id=job_id,
        message='Crawler started successfully!',
        status='initializing',
        progress=0,
        urls_processed=0,
        total_urls=config.limit or 0
    )

@crawler_router.get('/{job_id}', response_model=CrawlerJobResponse)
async def get_crawler_status(job_id: str):
    # Check if the job is running
    if job_id in running_jobs:
        job = running_jobs[job_id]
        return CrawlerJobResponse(
            job_id=job_id,
            message=f'Crawler job is {job['status']}',
            status=job['status'],
            progress=job.get('progress', 0),
            urls_processed=job.get('urls_processed', 0),
            total_urls=job.get('total_urls', 0),
        )
    
    # Check if the job is completed
    if job_id in job_results:
        job = job_results[job_id]
        return CrawlerJobResponse(
            job_id=job_id,
            message='Crawler job completed',
            status=job.get('status', 'completed'),
            progress=100 if job.get('status') == 'completed' else 0,
            urls_processed=job.get('urls_processed', 0),
            total_urls=job.get('total_urls', job.get('urls_processed', 0))
        )
    
    # Job isn't found
    raise HTTPException(status_code=404, detail=f'Job {job_id} not found')

@crawler_router.get('/{job_id}/results', response_model=CrawlerResults)
async def get_crawler_results(job_id: str):
    # Check if job is completed
    if job_id in job_results:
        result_file = job_results[job_id].get('result_file')

        if result_file and os.path.exists(result_file):
            try:
                with open(result_file, 'r') as f:
                    data = json.load(f)
                    return CrawlerResults(results=data)
            except Exception as e:
                logger.error(f'Error reading crawler results: {e}')
                raise HTTPException(status_code=500, detail='Error reading crawler results')
        else:
            # Return empty results if the file isn't found.
            return CrawlerResults(results=[])
                
    # If job is still running, return current results
    if job_id in running_jobs:
        raise HTTPException(status_code=202, detail="Job is still running, no results available yet.")
    
    # Job not found or no results
    raise HTTPException(status_code=404, detail=f"Results for job {job_id} not found.")

@crawler_router.get('/{job_id}/logs')
async def get_crawler_logs(job_id:str):
    return {'logs': get_job_logs(job_id)}

@crawler_router.post('/{job_id}/stop')
async def stop_crawler_job(job_id: str):
    if job_id in running_jobs:
        # Log the request
        if 'logs' in running_jobs[job_id]:
            running_jobs[job_id]['logs'].append(f'[{datetime.now().isoformat()}] Stop requested by user')

        # Update the status to stop the loop
        running_jobs[job_id]['status'] = 'stopped'

        # Stop the crawler or task instance
        if job_id in crawler_instances:
            try:
                crawler_instances[job_id].stop()
                logger.info(f"Successfully called stop() on crawler for job {job_id}")
            except Exception as e:
                logger.error(f"Error stopping crawler for job {job_id}: {str(e)}")

        # Move the job from running to results with an updated state
        job_results[job_id] = {
            'status': 'stopped',
            'urls_processed': running_jobs[job_id].get('urls_processed', 0),
            'completed_at': datetime.now().isoformat(),
            'stopped_by_user': True
        }

        # Copy the logs over
        if 'logs' in running_jobs[job_id]:
            job_results[job_id]['logs'] = running_jobs[job_id]['logs']

        # Broadcast the stop message to the connected clients
        if job_id in active_connections:
            stop_message = {
                'type': 'status',
                'job_id': job_id,
                'data': {'status': 'stopped'}
            }
            for websocket in active_connections[job_id]:
                try:
                    await websocket.send_json(stop_message)
                except Exception as e:
                    logger.error(f'Error sending stop message to Websocekt: {str(e)}')

        # Remove from the running jobs list
        del running_jobs[job_id]

        return {'success': True, 'message': 'Job stopped successfully'}
    
    # if the job isn't in the running_jobs but is already finished.
    if job_id in job_results:
        return {'success': True, 'message': 'Job was already completed.'}
    
    # If no job was found in either
    raise HTTPException(status_code=404, detail=f'Job {job_id} not found')

@crawler_router.post('/{job_id}/pause')
async def pause_crawler_job(job_id: str):
    if job_id in running_jobs:
        running_jobs[job_id]['status'] = 'paused'
        if 'logs' in running_jobs[job_id]:
            running_jobs[job_id]['logs'].append(f'[{datetime.now().isoformat()}] Pause requested by user')

        # Pause the crawler
        if job_id in crawler_instances:
            crawler_instances[job_id].pause()

        # Broadcast that the job has been paused
        if job_id in active_connections:
            pause_message = {
                'type': 'status',
                'job_id': job_id,
                'data': {'status': 'paused'}
            }
            for websocket in active_connections[job_id]:
                try:
                    await websocket.send_json(pause_message)
                except Exception as e:
                    logger.error(f'Error sending pause message to Websocekt: {str(e)}')
        
        return {'success': True, 'message': 'Job paused successfully'}

    raise HTTPException(status_code=404, detail=f'Job {job_id} not found')

@crawler_router.post("/{job_id}/resume")
async def resume_crawler_job(job_id: str):
    if job_id in running_jobs:
        running_jobs[job_id]["status"] = "running"
        if "logs" in running_jobs[job_id]:
            running_jobs[job_id]["logs"].append(f"[{datetime.now().isoformat()}] Job resumed by user")

        # Resume the crawler
        if job_id in crawler_instances:
            crawler_instances[job_id].resume()
            
        # Broadcast resume message to all connected clients
        if job_id in active_connections:
            resume_message = {
                "type": "status", 
                "job_id": job_id, 
                "data": {"status": "running"}
            }
            for websocket in active_connections[job_id]:
                try:
                    await websocket.send_json(resume_message)
                except Exception as e:
                    logger.error(f"Error sending resume message to WebSocket: {str(e)}")
                    
        return {"success": True, "message": "Job resumed successfully"}
    
    raise HTTPException(status_code=404, detail=f"Job {job_id} not found")

# Function to get all the routers for main.py
def get_service_routers():
    return [crawler_router]

# Function to register websocket handlers
def get_websocket_handlers():
    return {
        'crawler': handle_crawler_websocket
    }