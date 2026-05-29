"""
Print Scheduler Module
Author: Eng. Justo Torres
Company: Lagudis Fresh Food Group
"""

import schedule
import threading
import time
from datetime import datetime
from typing import List, Callable, Optional
import json
from pathlib import Path


class ScheduledJob:
    """Represents a scheduled print job"""

    def __init__(self,
                 job_id: str,
                 name: str,
                 filepaths: List[str],
                 printer: str,
                 scheduled_time: datetime,
                 status: str = "Pending"):
        self.job_id = job_id
        self.name = name
        self.filepaths = filepaths
        self.printer = printer
        self.scheduled_time = scheduled_time
        self.status = status  # Pending, Completed, Cancelled, Error
        self.error_message = ""
        self.executed_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization"""
        return {
            'job_id': self.job_id,
            'name': self.name,
            'filepaths': self.filepaths,
            'printer': self.printer,
            'scheduled_time': self.scheduled_time.isoformat(),
            'status': self.status,
            'error_message': self.error_message,
            'executed_at': self.executed_at.isoformat() if self.executed_at else None
        }

    @staticmethod
    def from_dict(data: dict) -> 'ScheduledJob':
        """Create from dictionary"""
        job = ScheduledJob(
            job_id=data['job_id'],
            name=data['name'],
            filepaths=data['filepaths'],
            printer=data['printer'],
            scheduled_time=datetime.fromisoformat(data['scheduled_time']),
            status=data['status']
        )
        job.error_message = data.get('error_message', '')
        if data.get('executed_at'):
            job.executed_at = datetime.fromisoformat(data['executed_at'])
        return job

    def __repr__(self):
        return f"ScheduledJob({self.name}, {self.scheduled_time}, {self.status})"


class PrintScheduler:
    """Manages scheduled print jobs"""

    def __init__(self, printer_manager=None):
        self.jobs: List[ScheduledJob] = []
        self.printer_manager = printer_manager
        self.running = False
        self.thread: Optional[threading.Thread] = None

        # Load saved jobs
        self.jobs_file = Path.home() / '.pdf_print_manager' / 'scheduled_jobs.json'
        self.jobs_file.parent.mkdir(parents=True, exist_ok=True)
        self._load_jobs()

    def _load_jobs(self) -> None:
        """Load scheduled jobs from file"""
        try:
            if self.jobs_file.exists():
                with open(self.jobs_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.jobs = [ScheduledJob.from_dict(job_data) for job_data in data]

                # Remove old completed/cancelled jobs
                self.jobs = [
                    job for job in self.jobs
                    if job.status == "Pending" and job.scheduled_time > datetime.now()
                ]

                self._save_jobs()

        except Exception as e:
            print(f"Error loading scheduled jobs: {e}")
            self.jobs = []

    def _save_jobs(self) -> None:
        """Save scheduled jobs to file"""
        try:
            data = [job.to_dict() for job in self.jobs]
            with open(self.jobs_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving scheduled jobs: {e}")

    def add_job(self,
                name: str,
                filepaths: List[str],
                printer: str,
                scheduled_time: datetime) -> ScheduledJob:
        """
        Add a new scheduled job

        Args:
            name: Job name/description
            filepaths: List of PDF file paths to print
            printer: Target printer name
            scheduled_time: When to execute the job

        Returns:
            The created ScheduledJob
        """
        # Generate unique job ID
        job_id = f"job_{int(time.time())}_{len(self.jobs)}"

        job = ScheduledJob(
            job_id=job_id,
            name=name,
            filepaths=filepaths,
            printer=printer,
            scheduled_time=scheduled_time
        )

        self.jobs.append(job)
        self._save_jobs()

        return job

    def cancel_job(self, job_id: str) -> bool:
        """Cancel a scheduled job"""
        for job in self.jobs:
            if job.job_id == job_id and job.status == "Pending":
                job.status = "Cancelled"
                self._save_jobs()
                return True
        return False

    def get_pending_jobs(self) -> List[ScheduledJob]:
        """Get all pending jobs"""
        return [job for job in self.jobs if job.status == "Pending"]

    def get_all_jobs(self) -> List[ScheduledJob]:
        """Get all jobs"""
        return self.jobs

    def clear_completed_jobs(self) -> None:
        """Remove completed and cancelled jobs"""
        self.jobs = [job for job in self.jobs if job.status == "Pending"]
        self._save_jobs()

    def start(self) -> None:
        """Start the scheduler in a background thread"""
        if self.running:
            return

        self.running = True
        self.thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        self.thread.start()

    def stop(self) -> None:
        """Stop the scheduler"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)

    def _scheduler_loop(self) -> None:
        """Main scheduler loop (runs in background thread)"""
        while self.running:
            try:
                # Check for jobs that need to be executed
                now = datetime.now()

                for job in self.get_pending_jobs():
                    if job.scheduled_time <= now:
                        self._execute_job(job)

                # Sleep for 30 seconds before checking again
                time.sleep(30)

            except Exception as e:
                print(f"Error in scheduler loop: {e}")
                time.sleep(30)

    def _execute_job(self, job: ScheduledJob) -> None:
        """Execute a scheduled job"""
        try:
            print(f"Executing scheduled job: {job.name}")

            job.status = "Executing"
            job.executed_at = datetime.now()

            if not self.printer_manager:
                raise Exception("PrinterManager not available")

            # Print all files in the job
            for filepath in job.filepaths:
                success, message = self.printer_manager.print_pdf(filepath, job.printer)

                if not success:
                    raise Exception(f"Failed to print {filepath}: {message}")

                # Small delay between files
                time.sleep(2)

            # Mark as completed
            job.status = "Completed"
            print(f"Scheduled job completed: {job.name}")

        except Exception as e:
            job.status = "Error"
            job.error_message = str(e)
            print(f"Error executing scheduled job: {e}")

        finally:
            self._save_jobs()
