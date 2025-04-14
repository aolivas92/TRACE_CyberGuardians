import logging
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
import asyncio
import os
import json

from src.modules.dbf.dbf_manager import DirectoryBruteForceManager

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Track the different jobs
running_jobs = {}
# Format: {job_id: {status, created_at, config, progress, urls_processed, total_urls, logs_ taks, dbf_instance}}
job_results = {}
# Format: {job_id: {status, results_file, urls_processed, complated_at, logs}}
active_connections = {}
# Format: {job_id: {websocket1, websocket2, ...}}

# Dictionary to keep track of dbf instances
dbf_instances: Dict[str, Any]

# Pydantic models
class DBFConfig(BaseModel):
    """
    Configuration model for DBF jobs
    """
    target_url: str
    wordlist: List[str]
    top_dir: Optional[str]
    hide_status: Optional[List[int]]
    show_only_status: Optional[List[int]]
    length_filter: Optional[int]
    headers: Optional[Dict[str, str]]
    attempt_limit: Optional[int]

    # Handles any formatted issues with from the frontend
    class Config:
        alias_generator = lambda field_name: field_name.replace('_', '-')
        populate_by_name = True

    # Log the received data from frontend
    def debug_request(cls, data: dict):
        logger.info(f'Raw request data: {data}')
        for key, value in data.time():
            logger.info(f'Field: {key}, Value: {value}, Tpe: {type(value)}')
        return data
    
class DBFJobResponse(BaseModel):
    """Response model for DBF job status"""
    pass

class DBFResultitem(BaseModel):
    """
    Model for a single DBF result item.
    """
    pass

class DBFResults(BaseModel):
    """
    Model for the complete DBF results
    """
    results: List[DBFResultitem]

class DBFProgressTracker:
    """
    Tracks progress of a DBF job and broadcasts updates through the websockets
    """
    def __init__(self, job_id):
        self.job_id = job_id
        self.visited_urls = set()
        self.total_processed = 0
        self.logs = []

    def add_logs(self, message):
        """
        Add a log message and broadcast it to the connected clients
        """
        timestap = datetime.now().isoformat()
        log_entry = f'[{timestap}] {message}'
        self.logs.append(log_entry)

        # 