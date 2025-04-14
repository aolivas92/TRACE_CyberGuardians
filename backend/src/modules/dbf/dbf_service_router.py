# dbf_service_router.py

from fastapi import APIRouter, BackgroundTasks, HTTPException
import uuid
import os
import json
import logging

from src.modules.dbf.dbf_service import (
    DBFConfig,
    DBFJobResponse,
    DBFResults,
    run_dbf_task,
    running_dbf_jobs,
    dbf_job_results
)

logger = logging.getLogger(__name__)
dbf_router = APIRouter(prefix='/api/dbf', tags=['directory-brute-force'])

@dbf_router.post('', response_model=DBFJobResponse)
async def start_dbf_scan(config: DBFConfig, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())

    running_dbf_jobs[job_id] = {
        'status': 'initializing',
        'created_at': str(uuid.uuid4()),
        'urls_processed': 0,
        'logs': []
    }

    background_tasks.add_task(run_dbf_task, job_id, config)

    return DBFJobResponse(
        job_id=job_id,
        message="DBF scan started successfully",
        status='initializing',
        urls_processed=0
    )

@dbf_router.get('/{job_id}', response_model=DBFJobResponse)
async def get_dbf_status(job_id: str):
    if job_id in running_dbf_jobs:
        job = running_dbf_jobs[job_id]
        return DBFJobResponse(
            job_id=job_id,
            message="Running",
            status=job.get('status', 'running'),
            urls_processed=job.get('urls_processed', 0)
        )
    elif job_id in dbf_job_results:
        job = dbf_job_results[job_id]
        return DBFJobResponse(
            job_id=job_id,
            message="Completed",
            status=job.get('status', 'completed'),
            urls_processed=job.get('urls_processed', 0)
        )
    else:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")

@dbf_router.get('/{job_id}/results', response_model=DBFResults)
async def get_dbf_results(job_id: str):
    if job_id not in dbf_job_results:
        raise HTTPException(status_code=404, detail="Results not found")
    return DBFResults(results=dbf_job_results[job_id].get('results', []))

# Function to register

def get_service_routers():
    return [dbf_router]
