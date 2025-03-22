# src/ui/main_window.py
import tkinter as tk
from tkinter import ttk, messagebox
from src.services.scheduler_service import SchedulerService


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Round Robin Scheduler")
        self.scheduler_service = SchedulerService()
        self.process_counter = 1
        self.processes = []

        self.create_widgets()

    def create_widgets(self):
        # Frame para la configuración
        config_frame = ttk.LabelFrame(self.root, text="Configuración")
        config_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(config_frame, text="Quantum:").grid(row=0, column=0, padx=5, pady=5)
        self.quantum_entry = ttk.Entry(config_frame, width=10)
        self.quantum_entry.grid(row=0, column=1, padx=5, pady=5)
        self.quantum_entry.insert(0, "2")  # Valor predeterminado

        # Frame para agregar procesos
        process_frame = ttk.LabelFrame(self.root, text="Agregar Proceso")
        process_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(process_frame, text="Tiempo de llegada:").grid(row=0, column=0, padx=5, pady=5)
        self.arrival_entry = ttk.Entry(process_frame, width=10)
        self.arrival_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(process_frame, text="Duración:").grid(row=0, column=2, padx=5, pady=5)
        self.duration_entry = ttk.Entry(process_frame, width=10)
        self.duration_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Button(process_frame, text="Agregar Proceso", command=self.add_process).grid(row=0, column=4, padx=5,
                                                                                         pady=5)

        # Lista de procesos
        list_frame = ttk.LabelFrame(self.root, text="Lista de Procesos")
        list_frame.pack(padx=10, pady=10, fill="both", expand=True)

        columns = ("ID", "Tiempo de llegada", "Duración")
        self.process_tree = ttk.Treeview(list_frame, columns=columns, show="headings")

        for col in columns:
            self.process_tree.heading(col, text=col)
            self.process_tree.column(col, width=100)

        self.process_tree.pack(padx=5, pady=5, fill="both", expand=True)

        # Botones de control
        control_frame = ttk.Frame(self.root)
        control_frame.pack(padx=10, pady=10, fill="x")

        ttk.Button(control_frame, text="Ejecutar Simulación", command=self.run_simulation).pack(side="left", padx=5)
        ttk.Button(control_frame, text="Limpiar Todo", command=self.clear_all).pack(side="right", padx=5)

    def add_process(self):
        try:
            arrival_time = int(self.arrival_entry.get())
            duration = int(self.duration_entry.get())

            if arrival_time < 0 or duration <= 0:
                messagebox.showerror("Error", "Los valores deben ser positivos y la duración mayor que cero")
                return

            process_id = f"P{self.process_counter}"
            self.process_counter += 1

            self.processes.append({
                'id': process_id,
                'arrival': arrival_time,
                'duration': duration
            })

            self.process_tree.insert("", "end", values=(process_id, arrival_time, duration))

            # Limpiar entradas
            self.arrival_entry.delete(0, tk.END)
            self.duration_entry.delete(0, tk.END)

        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores numéricos")

    def run_simulation(self):
        if not self.processes:
            messagebox.showwarning("Advertencia", "No hay procesos para simular")
            return

        try:
            quantum = int(self.quantum_entry.get())
            if quantum <= 0:
                messagebox.showerror("Error", "El quantum debe ser un número positivo")
                return

            # Crear y configurar el scheduler
            self.scheduler_service.create_scheduler(quantum)

            for process in self.processes:
                self.scheduler_service.add_process(
                    process['id'],
                    process['arrival'],
                    process['duration']
                )

            # Ejecutar la simulación
            self.scheduler_service.run_simulation()

            # Mostrar resultados
            self.show_results()

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def show_results(self):
        results = self.scheduler_service.get_results()
        sequence = self.scheduler_service.get_execution_sequence()

        # Crear una nueva ventana para mostrar resultados
        result_window = tk.Toplevel(self.root)
        result_window.title("Resultados de la Simulación")
        result_window.geometry("800x600")

        # Tabla de resultados
        ttk.Label(result_window, text="Resultados por proceso:", font=("Arial", 12, "bold")).pack(pady=10)

        columns = (
        "ID", "Llegada", "Duración", "Completado", "Tiempo de Retorno", "Tiempo de Espera", "Tiempo de Respuesta")
        result_tree = ttk.Treeview(result_window, columns=columns, show="headings")

        for col in columns:
            result_tree.heading(col, text=col)
            result_tree.column(col, width=100)

        for result in results:
            result_tree.insert("", "end", values=(
                result['process_id'],
                result['arrival_time'],
                result['duration'],
                result['completion_time'],
                result['turnaround_time'],
                result['waiting_time'],
                result['response_time']
            ))

        result_tree.pack(padx=10, pady=10, fill="both")

        # Diagrama de Gantt simplificado
        ttk.Label(result_window, text="Diagrama de Gantt:", font=("Arial", 12, "bold")).pack(pady=10)

        gantt_frame = ttk.Frame(result_window)
        gantt_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Canvas para dibujar el diagrama
        canvas = tk.Canvas(gantt_frame, bg="white")
        canvas.pack(fill="both", expand=True)

        # Dibujar el diagrama de Gantt
        time_unit_width = 30
        row_height = 30
        margin = 50

        # Dibujar las líneas de tiempo
        max_time = max(seq['end_time'] for seq in sequence)

        for i in range(max_time + 1):
            x = margin + i * time_unit_width
            canvas.create_line(x, margin - 10, x, margin + len(self.processes) * row_height + 10)
            canvas.create_text(x, margin - 20, text=str(i))

        # Dibujar los procesos
        process_colors = {}
        colors = ["#FF9999", "#99FF99", "#9999FF", "#FFFF99", "#FF99FF", "#99FFFF"]

        for i, process in enumerate(self.processes):
            process_id = process['id']
            y = margin + i * row_height
            canvas.create_text(margin - 30, y + row_height / 2, text=process_id)

            # Asignar un color a cada proceso
            if process_id not in process_colors:
                process_colors[process_id] = colors[i % len(colors)]

        # Dibujar la ejecución
        for seq in sequence:
            process_id = seq['process_id']
            start = seq['start_time']
            end = seq['end_time']

            # Encontrar la fila del proceso
            process_index = next(i for i, p in enumerate(self.processes) if p['id'] == process_id)
            y = margin + process_index * row_height

            # Dibujar el bloque
            canvas.create_rectangle(
                margin + start * time_unit_width,
                y,
                margin + end * time_unit_width,
                y + row_height,
                fill=process_colors[process_id],
                outline="black"
            )
            canvas.create_text(
                margin + (start + end) * time_unit_width / 2,
                y + row_height / 2,
                text=process_id
            )

    def clear_all(self):
        self.quantum_entry.delete(0, tk.END)
        self.quantum_entry.insert(0, "2")
        self.arrival_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)

        for item in self.process_tree.get_children():
            self.process_tree.delete(item)

        self.processes = []
        self.process_counter = 1