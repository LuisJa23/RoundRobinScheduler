# src/services/scheduler_service.py
from src.models.process import Process
from src.models.scheduler import RoundRobinScheduler


class SchedulerService:
    def __init__(self):
        self.scheduler = None

    def create_scheduler(self, quantum):
        self.scheduler = RoundRobinScheduler(quantum)
        return self.scheduler

    def add_process(self, process_id, arrival_time, duration):
        if not self.scheduler:
            raise ValueError("Scheduler must be created first")

        process = Process(process_id, arrival_time, duration)
        self.scheduler.add_process(process)

    def run_simulation(self):
        if not self.scheduler:
            raise ValueError("Scheduler must be created first")

        self.scheduler.run()

    def get_results(self):
        if not self.scheduler:
            raise ValueError("Scheduler must be created first")

        return self.scheduler.get_results()

    def get_execution_sequence(self):
        if not self.scheduler:
            raise ValueError("Scheduler must be created first")

        return self.scheduler.get_execution_sequence()