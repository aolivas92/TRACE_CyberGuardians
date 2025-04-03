from fastapi import FastAPI, Request, BackgroundTasks, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
import logging
import uvicorn
import strawberry
import uuid
import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Any

# Import the modules
from src.modules.scanning.crawler_service import (
    CrawlerConfig,
    CrawlerJobResponse,
    CrawlerResults,
    running_jobs,
    job_results,
    active_connections,
    run_crawler_task,
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
class JobStatus:
    job_id: str
    status: str
    progress: float
    urls_processed: int
    total_urls: int
    created_at: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    error: Optional[str] = None

@strawberry.type
class Query:
    @strawberry.field
    def get_crawler_results(self, job_id: str) -> List[CrawlerResult]:
        if job_id in job_results and 'result_file' in job_results[job_id]:
            result_file = job_results[job_id]['results_file']

            if os.path.exists(result_file):
                try:
                    with open(result_file, 'r') as file:
                        data = json.load(file)
                        return [
                            CrawlerResult(
                                url=item['url'],
                                title=item['title'],
                                parent_url=item.get('parentUrl'),
                                word_count=item['wordCount'],
                                char_count=item['charCount'],
                                links_found=item['linksFound'],  # Fixed index error here
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
        return 'not found'
    
schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema)

# Create FastAPI App
app = FastAPI(title='Trace API')

# config CORS to allow request from SveltKit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(graphql_app, prefix='/graphql')

# WebSocket endpoint for the real-time crawler updates
@app.websocket('/ws/crawler/{job_id}')
async def crawler_socket(websocket: WebSocket, job_id: str):
    await websocket.accept()

    # Register the connection
    if job_id not in active_connections:
        active_connections[job_id] = []
    active_connections[job_id].append(websocket)

    try:
        # Send an initial status message
        initial_status = get_job_status_messsage(job_id)
        await websocket.send_json(initial_status)

        # List for the clients response
        while True:
            message = await websocket.receive_text()
            try:
                data = json.loads(message)

                # Handle client commands
                if data.get('type') == 'command':
                    command = data.get('command')

                    if command == 'get_logs':
                        # Send all logs
                        logs = get_job_logs(job_id)
                        await websocket.send_json({
                            'type': 'logs',
                            'job_id': job_id,
                            'data': {'logs': logs}
                        })

            except json.JSONDecodeError:
                logger.error(f'Received invalid JSON from client: {message}')

    except WebSocketDisconnect:
        # Remove the connection from the list
        if job_id in active_connections and websocket in active_connections[job_id]:
            active_connections[job_id].remove(websocket)
            if not active_connections[job_id]:
                del active_connections[job_id]
        logger.info(f'WebSocket disconnected for job: {job_id}')

    except Exception as e:
        logger.error(f'Error in WebSocket connection for job {job_id}: {str(e)}')
        if job_id in active_connections and websocket in active_connections[job_id]:
            active_connections[job_id].remove(websocket)
            if not active_connections[job_id]:
                del active_connections[job_id]

def get_job_status_messsage(job_id: str) -> Dict[str, Any]:  # TODO: Fix typo in function name on next refactor
    if job_id in running_jobs:
        job = running_jobs[job_id]
        return {
            "type": "status",
            "job_id": job_id,
            "data": {
                "status": job.get("status", "unknown"),
                "progress": job.get("progress", 0),
                "urls_processed": job.get("urls_processed", 0),
                "total_urls": job.get("total_urls", 0),
                "created_at": job.get("created_at", ""),
                "started_at": job.get("started_at", "")
            }
        }
    elif job_id in job_results:
        job = job_results[job_id]
        return {
            "type": "status",
            "job_id": job_id,
            "data": {
                "status": job.get("status", "completed"),
                "progress": 100,
                "urls_processed": job.get("urls_processed", 0),
                "total_urls": job.get("total_urls", job.get("urls_processed", 0)),
                "completed_at": job.get("completed_at", ""),
                "error": job.get("error", None)
            }
        }
    else:
        return {
            "type": "error",
            "job_id": job_id,
            "data": {"message": f"Job {job_id} not found"}
        }
    
def get_job_logs(job_id: str) -> List[str]:
    if job_id in running_jobs and "logs" in running_jobs[job_id]:
        return running_jobs[job_id]["logs"]
    elif job_id in job_results and "logs" in job_results[job_id]:
        return job_results[job_id]["logs"]
    return []

# Crawler endpoints
@app.post("/api/crawler", response_model=CrawlerJobResponse)
async def start_crawler(config: CrawlerConfig, background_tasks: BackgroundTasks):
    logger.info(f"Received crawler configuration: {config}")
    
    # Generate a unique job ID
    job_id = str(uuid.uuid4())
    
    # Register job
    running_jobs[job_id] = {
        'status': 'initializing',
        'created_at': datetime.now().isoformat(),
        'config': config.model_dump(),
        'progress': 0,
        'urls_processed': 0,
        'total_urls': config.limit or 100,
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
        total_urls=config.limit or 100
    )

@app.get("/api/crawler/{job_id}", response_model=CrawlerJobResponse)
async def get_crawler_status(job_id: str):
    # Check if job is running
    if job_id in running_jobs:
        job = running_jobs[job_id]
        return CrawlerJobResponse(
            job_id=job_id,
            message=f"Crawler job is {job['status']}",
            status=job['status'],
            progress=job.get('progress', 0),
            urls_processed=job.get('urls_processed', 0),
            total_urls=job.get('total_urls', 100)
        )
    
    # Check if job is completed
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
    
    # Job not found
    raise HTTPException(status_code=404, detail=f"Job {job_id} not found")

@app.get("/api/crawler/{job_id}/results", response_model=CrawlerResults)
async def get_crawler_results(job_id: str):
    # Check if job is completed
    if job_id in job_results:
        result_file = job_results[job_id].get('results_file')
        
        if result_file and os.path.exists(result_file):
            try:
                with open(result_file, 'r') as f:
                    data = json.load(f)
                    return CrawlerResults(results=data)
            except Exception as e:
                logger.error(f"Error reading crawler results: {e}")
                raise HTTPException(status_code=500, detail="Error reading crawler results")
        else:
            # Return empty results if file doesn't exist
            return CrawlerResults(results=[])
    
    # If job is still running, return current results
    if job_id in running_jobs:
        raise HTTPException(status_code=202, detail="Job is still running, no results available yet")
    
    # Job not found or no results
    raise HTTPException(status_code=404, detail=f"Results for job {job_id} not found")

@app.get("/api/crawler/{job_id}/logs")
async def get_crawler_logs(job_id: str):
    return {"logs": get_job_logs(job_id)}

@app.get("/")
async def root():
    return {"message": "TRACE API is running."}

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