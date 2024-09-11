import tkinter as tk
from ui_components import WorkoutPlanner

def main():
    root = tk.Tk()
    app = WorkoutPlanner(root)
    root.mainloop()

if __name__ == "__main__":
    main()
