from fastapi import APIRouter, BackgroundTasks, HTTPException, WebSocket, WebSocketDisconnect
import logging
import uuid
import os
import json
from datetime import datetime
from typing import Dict, List, Any

# Import service module
from src.modules.ai.ml_service import (
    MLConfig,
    MLJobResponse,
    CredentialResults,
    running_jobs,
    job_results,
    active_connections,
    run_ml_task,
    get_job_status_message,
    get_job_logs
)

# Setup logging
logger = logging.getLogger(__name__)

# Create router for ML service
ml_router = APIRouter(prefix="/api/ml", tags=["ml"])

# WebSocket handler for ML service
async def handle_ml_websocket(websocket: WebSocket, job_id: str):
    print(f'[Backend] WebSocket connection opened for ML job: {job_id}') 

    await websocket.accept()

    print('Active ML jobs after accept:', list(running_jobs.keys()))

    # Register the connection
    if job_id not in active_connections:
        active_connections[job_id] = []
    active_connections[job_id].append(websocket)

    try:
        # Send an initial status message
        initial_status = get_job_status_message(job_id)
        await websocket.send_json(initial_status)

        # Listen for client responses
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

# ML API endpoints
@ml_router.post("", response_model=MLJobResponse)
async def start_ml_job(config: MLConfig, background_tasks: BackgroundTasks):
    logger.info(f"Received ML configuration: {config}")
    
    # Generate a unique job ID
    job_id = str(uuid.uuid4())
    
    # Register job
    running_jobs[job_id] = {
        'status': 'initializing',
        'created_at': datetime.now().isoformat(),
        'config': config.model_dump(),
        'progress': 0,
        'step': 'initializing',
        'logs': []
    }
    
    # Start ML job in background
    background_tasks.add_task(run_ml_task, job_id, config)
    
    return MLJobResponse(
        job_id=job_id,
        message='ML job started successfully!',
        status='initializing',
        progress=0,
        step='initializing',
        total_steps=3
    )

@ml_router.get("/{job_id}", response_model=MLJobResponse)
async def get_ml_job_status(job_id: str):
    # Check if job is running
    if job_id in running_jobs:
        job = running_jobs[job_id]
        return MLJobResponse(
            job_id=job_id,
            message=f"ML job is {job['status']}",
            status=job['status'],
            progress=job.get('progress', 0),
            step=job.get('step', 'initializing'),
            total_steps=3
        )
    
    # Check if job is completed
    if job_id in job_results:
        job = job_results[job_id]
        return MLJobResponse(
            job_id=job_id,
            message='ML job completed',
            status=job.get('status', 'completed'),
            progress=100 if job.get('status') == 'completed' else 0,
            step='completed' if job.get('status') == 'completed' else 'error',
            total_steps=3
        )
    
    # Job not found
    raise HTTPException(status_code=404, detail=f"Job {job_id} not found")

@ml_router.get("/{job_id}/results", response_model=CredentialResults)
async def get_ml_results(job_id: str):
    # Check if job is completed
    if job_id in job_results:
        result_file = job_results[job_id].get('results_file')
        
        if result_file and os.path.exists(result_file):
            try:
                with open(result_file, 'r') as f:
                    data = json.load(f)
                    return CredentialResults(results=data)
            except Exception as e:
                logger.error(f"Error reading ML results: {e}")
                raise HTTPException(status_code=500, detail="Error reading ML results")
        else:
            # Return empty results if file doesn't exist
            return CredentialResults(results=[])
    
    # If job is still running, return current results
    if job_id in running_jobs:
        raise HTTPException(status_code=202, detail="Job is still running, no results available yet")
    
    # Job not found or no results
    raise HTTPException(status_code=404, detail=f"Results for job {job_id} not found")

@ml_router.get("/{job_id}/logs")
async def get_ml_logs(job_id: str):
    return {"logs": get_job_logs(job_id)}

@ml_router.post('/{job_id}/stop')
async def stop_ml_job(job_id: str):
    if job_id in running_jobs:
        # Log the request
        if 'logs' in running_jobs[job_id]:
            running_jobs[job_id]['logs'].append(f'[{datetime.now().isoformat()}] Stop requested by user')

        # Update the status to stop the loop
        running_jobs[job_id]['status'] = 'stopped'

        # Move the job from running to results with an updated state
        job_results[job_id] = {
            'status': 'stopped',
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
                    logger.error(f'Error sending stop message to WebSocket: {str(e)}')

        # Remove from the running jobs list
        del running_jobs[job_id]

        return {'success': True, 'message': 'Job stopped successfully'}
    
    # if the job isn't in the running_jobs but is already finished.
    if job_id in job_results:
        return {'success': True, 'message': 'Job was already completed.'}
    
    # If no job was found in either
    raise HTTPException(status_code=404, detail=f'Job {job_id} not found')

# Function to get ML router for main.py
def get_service_routers():
    return [ml_router]

# Function to register websocket handlers
def get_websocket_handlers():
    return {
        "ml": handle_ml_websocket
    }