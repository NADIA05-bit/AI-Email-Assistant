import tkinter as tk
import random

root = tk.Tk()
root.title("Mission Control Dashboard")
root.geometry("600x400")

title = tk.Label(root, text="Mission Control", font=("Arial", 20))
title.pack(pady=10)

team = ["Alice", "Bob", "Charlie", "Dana"]

for member in team:
    overdue = random.randint(0, 5)
    label = tk.Label(root, text=f"{member} - Overdue Tasks: {overdue}", font=("Arial", 12))
    label.pack()

root.mainloop()