# src/main.py
import tkinter as tk
from src.ui.main_window import MainWindow

def main():
    root = tk.Tk()
    app = MainWindow(root)
    root.geometry("600x500")
    root.mainloop()

if __name__ == "__main__":
    main()