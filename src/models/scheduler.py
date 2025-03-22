# src/models/scheduler.py
class RoundRobinScheduler:
    def __init__(self, quantum):
        self.quantum = quantum
        self.processes = []
        self.current_time = 0
        self.execution_sequence = []

    def add_process(self, process):
        self.processes.append(process)

    def run(self):
        # Ordenar procesos por tiempo de llegada
        self.processes.sort(key=lambda x: x.arrival_time)

        # Cola de procesos listos
        ready_queue = []
        remaining_processes = len(self.processes)

        # Mientras queden procesos por completar
        while remaining_processes > 0:
            # Verificar si hay nuevos procesos que llegan en este momento
            for process in self.processes:
                if process.arrival_time <= self.current_time and process.remaining_time > 0:
                    if process not in ready_queue:
                        ready_queue.append(process)

            # Si no hay procesos en la cola, avanzar el tiempo
            if not ready_queue:
                self.current_time += 1
                continue

            # Obtener el siguiente proceso
            current_process = ready_queue.pop(0)

            # Si es la primera vez que el proceso se ejecuta, registrar su tiempo de respuesta
            if current_process.response_time == -1:
                current_process.response_time = self.current_time - current_process.arrival_time

            # Determinar cuánto tiempo se ejecutará
            execution_time = min(self.quantum, current_process.remaining_time)

            # Actualizar el tiempo actual
            self.current_time += execution_time

            # Actualizar el tiempo restante del proceso
            current_process.remaining_time -= execution_time

            # Registrar esta ejecución en la secuencia
            self.execution_sequence.append({
                'process_id': current_process.process_id,
                'start_time': self.current_time - execution_time,
                'end_time': self.current_time
            })

            # Si el proceso ha terminado
            if current_process.remaining_time == 0:
                remaining_processes -= 1
                current_process.completion_time = self.current_time
                current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
                current_process.waiting_time = current_process.turnaround_time - current_process.duration
            else:
                # Si no ha terminado, volver a ponerlo en la cola
                ready_queue.append(current_process)

    def get_results(self):
        results = []
        for process in self.processes:
            results.append({
                'process_id': process.process_id,
                'arrival_time': process.arrival_time,
                'duration': process.duration,
                'completion_time': process.completion_time,
                'turnaround_time': process.turnaround_time,
                'waiting_time': process.waiting_time,
                'response_time': process.response_time
            })
        return results

    def get_execution_sequence(self):
        return self.execution_sequence