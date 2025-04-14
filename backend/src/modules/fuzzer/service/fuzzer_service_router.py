from fastapi import APIRouter, BackgroundTasks, HTTPException, WebSocket, WebSocketDisconnect
import logging
import json
import uuid
from datetime import datetime
import os

# Import the service modules
from src.modules.fuzzer.service.fuzzer_service import (
    FuzzerConfig,
    FuzzerJobResponse,
    FuzzerResults,
    running_jobs,
    fuzzer_instances,
    job_results,
    active_connections,
    run_fuzzer_task,
    get_job_status_message,
    get_job_logs
)

# Set up log
logger = logging.getLogger(__name__)

# Create the routes prefix
fuzzer_router = APIRouter(prefix='/api/fuzzer', tags=['fuzzer'])

# Websocekt handler for the fuzzer service
async def handle_fuzzer_websocket(websocket: WebSocket, job_id: str):
    print(f'[Backend] Websocket connection opened for fuzzer job: {job_id}')

    await websocket.accept()

    print('Active fuzzer jobs after accept:', list(running_jobs.keys()))

    # Register the connection
    if job_id not in active_connections:
        active_connections[job_id] = []
    active_connections[job_id].append(websocket)

    try:
        # Send an inistial status message
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
        # If disconnected websocket remove it from the list
        if job_id in active_connections and websocket in active_connections[job_id]:
            active_connections[job_id].remove(websocket)
            if not active_connections[job_id]:
                del active_connections[job_id]

    except Exception as e:
        logger.error(f'Error in Websocket connection for fuzzer job {job_id}: {str(e)}')

        if job_id in active_connections and websocket in active_connections[job_id]:
            active_connections[job_id].remove(websocket)
            if not active_connections[job_id]:
                del active_connections[job_id]

# Log Helper Functions
def add_log_entry(job_id: str, message: str):
    """
    Add a log entry to the job's log
    """
    timestamp = datetime.now().isoformat()
    log_entry = f'[{timestamp}] {message}'

    if job_id in running_jobs:
        if 'logs' not in running_jobs[job_id]:
            running_jobs[job_id]['logs'] = []
        running_jobs[job_id]['logs'].append(log_entry)
        logger.info(f'Added log to running job {job_id}: {message}')

    elif job_id in job_results:
        if 'logs' not in job_results[job_id]:
            job_id[job_id]['logs'] = []
        job_results[job_id]['logs'].append(log_entry)
        logger.info(f'Added log to completed job {job_id}: {message}')

    else:
        logger.warning(f'Cannot add log for job {job_id}, job not found: {message}')

# Fuzzer API endpoints
@fuzzer_router.post('', response_model=FuzzerJobResponse)
async def start_fuzzer(config: FuzzerConfig, background_tasks: BackgroundTasks):
    logger.info(f'Received Fuzzer configuration: {config}')

    job_id = str(uuid.uuid4())

    # Register the job
    running_jobs[job_id] = {
        'status': 'initializing',
        'created_at': datetime.now().isoformat(),
        'progress': 0,
        'urls_processed': 0,
        'total_urls': len(config.parameters) * (len(config.payloads or []) + (1 if config.payload_file else 0)),
    }

    add_log_entry(job_id, f'Job created with configuration: {config.model_dump()}')

    # Start the fuzzer in the background
    background_tasks.add_task(run_fuzzer_task, job_id, config)

    return FuzzerJobResponse(
        job_id=job_id,
        message='Fuzzer started successfully!',
        status='initializing',
        progress=0,
        urls_processed=0,
        total_urls=running_jobs[job_id]['total_urls']
    )

@fuzzer_router.get('/{job_id}', response_model=FuzzerJobResponse)
async def get_fuzzer_status(job_id: str):
    # Job is running
    if job_id in running_jobs:
        job = running_jobs[job_id]
        return FuzzerJobResponse(
            job_id=job_id,
            message=f'Fuzzer job is {job['status']}',
            status=job['status'],
            progress=job.get('progress', 0),
            urls_processed=job.get('urls_processed', 0),
            total_urls=job.get('total_urls', 0)
        )
    
    # Job is complete
    if job_id in job_results:
        job = job_results[job_id]
        return FuzzerJobResponse(
            job_id=job_id,
            message='Fuzzer job completed',
            status=job.get('status', 'completed'),
            progress=100 if job.get('status') == 'completed' else 0,
            urls_processed=job.get('urls_processed', 0),
            total_urls=job.get('total_urls', job.get('urls_processed', 0))
        )
    
    # Job not found
    raise HTTPException(status_code=404, detail=f'Job {job_id} not found')

@fuzzer_router.get('/{job_id}/results', response_model=FuzzerResults)
async def get_fuzzer_results(job_id: str):
    add_log_entry(job_id, f"Results requested via API")
    
    # Check if completed
    if job_id in job_results:
        results_file = job_results[job_id].get('results_file')

        if results_file and os.path.exists(results_file):
            try:
                with open(results_file, 'r') as file:
                    data = json.load(file)
                    add_log_entry(job_id, f"Results retrieved: {len(data)} records")
                    return FuzzerResults(results=data)
            except Exception as e:
                logger.error(f'Error reading fuzzer results: {e}')
                raise HTTPException(status_code=500, detail='Error reading fuzzer results')
        
        # File isn't found
        else:
            return FuzzerResults(results=[])
        
    # Job is running
    if job_id in running_jobs:
        add_log_entry(job_id, "Results requested but job is still running")
        raise HTTPException(status_code=202, detail='Job is still running, no results available yet.')
    
    # Job not found
    raise HTTPException(status_code=404, detail=f'Results for job {job_id} not found.')

@fuzzer_router.get('/{job_id}/logs')
async def get_fuzzer_logs(job_id: str):
    logs = get_job_logs(job_id)
    add_log_entry(job_id, f"Logs requested via API, returning {len(logs)} entries")
    return {'logs': get_job_logs(job_id)}

@fuzzer_router.post('/{job_id}/stop')
async def stop_fuzzer_job(job_id: str):
    if job_id in running_jobs:
        if 'logs' in running_jobs[job_id]:
            add_log_entry(job_id, "Stop requested by user")
            running_jobs[job_id]['logs'].append(f'[{datetime.now().isoformat()}] Stop requested by user')

        running_jobs[job_id]['status'] = 'stopped'

        if job_id in fuzzer_instances:
            try:
                fuzzer_instances[job_id].stop()
                logger.info(f'Successfully called stop() on fuzzer for job {job_id}')
            except Exception as e:
                logger.error(f'Error stopping fuzzer for job {job_id}: {str(e)}')
                add_log_entry()

        job_results[job_id] = {
            'status': 'stopped',
            'urls_processed': running_jobs[job_id].get('urls_processed', 0),
            'completed_at': datetime.now().isoformat(),
            'stopped_by_user': True,
        }

        if 'logs' in running_jobs[job_id]:
            job_results[job_id]['logs'] = running_jobs[job_id]['logs']

        # Broadcast the stop message
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

        del running_jobs[job_id]

        return {'success': True, 'message': 'Job stopped successfully'}
    
    # If job is already finished
    if job_id in job_results:
        return {'success': True, 'message': 'Job was already completed.'}
    
    # If no job was found
    raise HTTPException(status_code=404, detail=f'Job {job_id} not found.')

@fuzzer_router.post('/{job_id}/pause')
async def pause_fuzzer_job(job_id: str):
    if job_id in running_jobs:
        running_jobs[job_id]['status'] = 'paused'
        add_log_entry(job_id, "Pause requested by user")
        if 'logs' in running_jobs[job_id]:
            running_jobs[job_id]['logs'].append(f'[{datetime.now().isoformat()}] Pause requested by user')

        if job_id in fuzzer_instances:
            fuzzer_instances[job_id].pause()
            logger.info(f'Successfully paused fuzzer for job {job_id}')

        # Broadcast the pause
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
                    logger.error(f'Error sending pause message to WebSocket: {str(e)}')
        
        return {'success': True, 'message': 'Job paused successfully'}
    
    raise HTTPException(status_code=404, detail=f'Job {job_id} not found.')

@fuzzer_router.post('/{job_id}/resume')
async def resume_fuzzer_job(job_id: str):
    if job_id in running_jobs:
        running_jobs[job_id]['status'] = 'running'
        add_log_entry(job_id, "Resume requested by user")
        if 'logs' in running_jobs[job_id]:
            running_jobs[job_id]['logs'].append(f'[{datetime.now().isoformat()}] Job resumed by user')

        if job_id in fuzzer_instances:
            fuzzer_instances[job_id].resume()
            logger.info(f'Successfully resumed fuzzer for job {job_id}')

        # Broadcast resume message
        if job_id in active_connections:
            resume_message = {
                'type': 'status',
                'job_id': job_id,
                'data': {'status': 'running'}
            }
            for websocket in active_connections[job_id]:
                try: 
                    await websocket.send_json(resume_message)
                except Exception as e:
                    logger.error(f'Error sending resmue message to Websocket: {str(e)}')

        return {'success': True, 'message': 'Job resumed successfully'}
    
    raise HTTPException(status_code=404, detail=f'Job {job_id} not found')

def get_service_routers():
    return [fuzzer_router]

def get_websocket_handlers():
    return {
        'fuzzer': handle_fuzzer_websocket
    }