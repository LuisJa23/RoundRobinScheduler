# src/models/process.py
class Process:
    def __init__(self, process_id, arrival_time, duration):
        self.process_id = process_id
        self.arrival_time = arrival_time
        self.duration = duration
        self.remaining_time = duration
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0
        self.response_time = -1  # -1 indica que aún no ha sido atendido

    def __str__(self):
        return f"Process {self.process_id}: Arrival={self.arrival_time}, Duration={self.duration}, Remaining={self.remaining_time}"