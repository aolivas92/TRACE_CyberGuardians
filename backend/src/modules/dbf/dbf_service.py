# dbf_service.py

import logging
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
import asyncio
import os

from src.modules.dbf.dbf_manager import DirectoryBruteForceManager

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Job tracking dictionaries
running_dbf_jobs = {}
dbf_job_results = {}

class DBFConfig(BaseModel):
    target_url: str
    wordlist: List[str]
    top_dir: Optional[str] = ''
    hide_status: Optional[List[int]] = []
    show_only_status: Optional[List[int]] = [200]
    length_filter: Optional[int] = None
    headers: Optional[Dict[str, str]] = {}
    attempt_limit: Optional[int] = -1

class DBFJobResponse(BaseModel):
    job_id: str
    message: str
    status: str
    urls_processed: Optional[int] = 0

class DBFResults(BaseModel):
    results: List[Dict[str, Any]]

async def run_dbf_task(job_id: str, config: DBFConfig):
    logger.info(f"[DBF] Starting job {job_id} with config: {config.model_dump()}")
    manager = DirectoryBruteForceManager()

    running_dbf_jobs[job_id] = {
        'status': 'running',
        'created_at': datetime.now().isoformat(),
        'urls_processed': 0,
        'logs': []
    }

    try:
        manager.configure_scan(
            target_url=config.target_url,
            wordlist=config.wordlist,
            top_dir=config.top_dir,
            hide_status=config.hide_status,
            show_only_status=config.show_only_status,
            length_filter=config.length_filter,
            headers=config.headers,
            attempt_limit=config.attempt_limit
        )

        await manager.start_scan()

        metrics = manager.get_metrics()
        results = manager.get_filtered_results()
        filename = f"dbf_results_{job_id}.txt"
        manager.save_results_to_txt(filename)

        dbf_job_results[job_id] = {
            'status': 'completed',
            'results_file': filename,
            'urls_processed': metrics['processed_requests'],
            'completed_at': datetime.now().isoformat(),
            'metrics': metrics,
            'results': results
        }

        del running_dbf_jobs[job_id]
        logger.info(f"[DBF] Job {job_id} completed")

    except Exception as e:
        logger.error(f"[DBF] Error in job {job_id}: {e}")
        dbf_job_results[job_id] = {
            'status': 'error',
            'error': str(e),
            'completed_at': datetime.now().isoformat(),
        }
        if job_id in running_dbf_jobs:
            del running_dbf_jobs[job_id]
