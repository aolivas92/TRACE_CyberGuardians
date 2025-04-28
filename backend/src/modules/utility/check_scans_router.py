from fastapi import APIRouter
import os

router = APIRouter()

@router.get("/api/check-scans")
async def check_scans():
    crawler_path = "./database/crawler"
    fuzzer_path = "./database/fuzzer"
    dbf_path = "./database/dbf"

    crawler_files = os.listdir(crawler_path) if os.path.exists(crawler_path) else []
    fuzzer_files = os.listdir(fuzzer_path) if os.path.exists(fuzzer_path) else []
    dbf_files = os.listdir(dbf_path) if os.path.exists(dbf_path) else []

    has_scans = bool(crawler_files or fuzzer_files or dbf_files)

    return {"hasScans": has_scans}