from __future__ import annotations

import threading
import uuid
from datetime import datetime, timezone
from typing import Any, Callable


class JobManager:
    """Small in-process job registry used by the local CreatorOS API.

    This keeps long-running work out of request lifecycles while exposing
    deterministic status/progress information to the frontend. It is intended
    for the local MVP; a durable queue can replace it later without changing
    the API contract.
    """

    def __init__(self) -> None:
        self._jobs: dict[str, dict[str, Any]] = {}
        self._lock = threading.Lock()

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()

    def create(self, job_type: str, runner: Callable[[str], Any]) -> dict[str, Any]:
        with self._lock:
            running = next(
                (
                    job
                    for job in self._jobs.values()
                    if job["type"] == job_type and job["status"] in {"PENDING", "RUNNING"}
                ),
                None,
            )
            if running:
                return dict(running)

            job_id = str(uuid.uuid4())
            job = {
                "job_id": job_id,
                "type": job_type,
                "status": "PENDING",
                "stage": "Queued",
                "progress": 0,
                "result": None,
                "error": None,
                "started_at": None,
                "completed_at": None,
                "created_at": self._now(),
            }
            self._jobs[job_id] = job

        thread = threading.Thread(
            target=self._run,
            args=(job_id, runner),
            daemon=True,
            name=f"CreatorOS-{job_type}-{job_id[:8]}",
        )
        thread.start()
        return dict(job)

    def _run(self, job_id: str, runner: Callable[[str], Any]) -> None:
        with self._lock:
            job = self._jobs.get(job_id)
            if job is None:
                return
            job["status"] = "RUNNING"
            job["started_at"] = self._now()

        try:
            result = runner(job_id)
            with self._lock:
                job = self._jobs.get(job_id)
                if job is not None:
                    job["status"] = "COMPLETED"
                    job["progress"] = 100
                    job["stage"] = "Completed"
                    job["result"] = result
                    job["completed_at"] = self._now()
        except Exception as error:
            with self._lock:
                job = self._jobs.get(job_id)
                if job is not None:
                    job["status"] = "FAILED"
                    job["stage"] = "Failed"
                    job["error"] = str(error)[:1500]
                    job["completed_at"] = self._now()

    def update(self, job_id: str, *, stage: str, progress: int) -> None:
        with self._lock:
            job = self._jobs.get(job_id)
            if job is None:
                return
            job["stage"] = stage
            job["progress"] = max(0, min(100, int(progress)))

    def get(self, job_id: str) -> dict[str, Any] | None:
        with self._lock:
            job = self._jobs.get(job_id)
            return dict(job) if job else None

    def latest(self, job_type: str) -> dict[str, Any] | None:
        with self._lock:
            matching = [job for job in self._jobs.values() if job["type"] == job_type]
            if not matching:
                return None
            return dict(sorted(matching, key=lambda item: item["created_at"])[-1])
