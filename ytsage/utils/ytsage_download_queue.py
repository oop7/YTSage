"""Persistent queue for configured downloads."""

import json
import threading
import time
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

from .ytsage_constants import APP_QUEUE_FILE
from .ytsage_logger import logger


class DownloadQueue:
    """Thread-safe persistence for queued download snapshots."""

    _lock = threading.RLock()
    _file = APP_QUEUE_FILE

    @classmethod
    def _read(cls) -> List[Dict[str, Any]]:
        try:
            if not cls._file.exists():
                return []
            with cls._file.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
            return data if isinstance(data, list) else []
        except (OSError, json.JSONDecodeError) as error:
            logger.error(f"Could not read download queue: {error}")
            return []

    @classmethod
    def _write(cls, jobs: List[Dict[str, Any]]) -> None:
        try:
            cls._file.parent.mkdir(parents=True, exist_ok=True)
            temporary_file = cls._file.with_suffix(".json.tmp")
            with temporary_file.open("w", encoding="utf-8") as handle:
                json.dump(jobs, handle, ensure_ascii=False, indent=2)
            temporary_file.replace(cls._file)
        except OSError as error:
            logger.error(f"Could not save download queue: {error}")

    @classmethod
    def get_all(cls) -> List[Dict[str, Any]]:
        with cls._lock:
            return cls._read()

    @classmethod
    def add(cls, job: Dict[str, Any]) -> Dict[str, Any]:
        queued_job = dict(job)
        queued_job.setdefault("id", uuid.uuid4().hex)
        queued_job.setdefault("queued_at", time.time())
        queued_job["status"] = "queued"
        with cls._lock:
            jobs = cls._read()
            jobs.append(queued_job)
            cls._write(jobs)
        return queued_job

    @classmethod
    def remove(cls, job_id: str) -> bool:
        with cls._lock:
            jobs = cls._read()
            remaining = [job for job in jobs if job.get("id") != job_id]
            if len(remaining) == len(jobs):
                return False
            cls._write(remaining)
            return True

    @classmethod
    def update(cls, job_id: str, **changes: Any) -> Optional[Dict[str, Any]]:
        with cls._lock:
            jobs = cls._read()
            for job in jobs:
                if job.get("id") == job_id:
                    job.update(changes)
                    cls._write(jobs)
                    return dict(job)
        return None

    @classmethod
    def clear_finished(cls) -> None:
        with cls._lock:
            jobs = [job for job in cls._read() if job.get("status") not in {"completed", "failed"}]
            cls._write(jobs)
