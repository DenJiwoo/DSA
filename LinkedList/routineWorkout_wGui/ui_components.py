import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import PhotoImage
from PIL import Image, ImageTk
from PIL import Image, ImageTk, ImageDraw
import tkinter.font as tkFont
from workout_logic import WorkoutRoutine


class WorkoutPlanner:
    def __init__(self, root):
        self.root = root
        image_path = r'E:\CODE PROJECTS\PYTHON\Python\Linked list act\img\Dumbell.png'
        try:
            self.icon = PhotoImage(file=image_path)
            self.root.iconphoto(True, self.icon)
        except Exception as e:
            print(f"Error loading icon: {e}")
        self.root.title("Workout Planner")
        self.root.geometry("500x850")      
        self.bg_image = PhotoImage(file=r'E:\CODE PROJECTS\PYTHON\Python\Linked list act\img\bgimg1.png')
        self.bg_label = tk.Label(self.root, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.custom_font = tkFont.Font(family="Lato", size=12, weight="normal", slant="italic") if "Lato" in tkFont.families() else tkFont.Font(family="Arial", size=12, slant="italic")
        self.routine = WorkoutRoutine()
        self.create_widgets()

    def create_widgets(self):
        self.root.config(background="#4D4D4D")
        self.day_label = tk.Label(self.root, text="Select Day: ", font=self.custom_font)
        self.day_label.pack(pady=10)
        self.day_var = tk.StringVar(value="Sunday")

        self.day_menu = ttk.Combobox(self.root, textvariable=self.day_var, value=self.get_days(), state='readonly')
        self.day_menu.pack(pady=10)

        self.navigation_frame1 = tk.Frame(self.root, bg='#292929')
        self.navigation_frame1.pack(pady=10)

        self.previous_day_button = tk.Button(self.navigation_frame1, text="Previous Day", command=self.show_previous_day_workouts, font=self.custom_font, relief="raised", bd=5)
        self.previous_day_button.grid(row=0, column=0, padx=5)

        self.next_day_button = tk.Button(self.navigation_frame1, text="Next Day", command=self.show_next_day_workouts, font=self.custom_font, relief="raised", bd=5)
        self.next_day_button.grid(row=0, column=1, padx=5)

        self.rest_day_button = tk.Button(self.root, text="Set as Rest Day", command=self.set_rest_day, font=self.custom_font, relief="raised", bd=5)
        self.rest_day_button.pack(pady=10)

        self.workout_day_button = tk.Button(self.root, text="Set as Workout Day", command=self.set_workout_day, font=self.custom_font, relief="raised", bd=5)
        self.workout_day_button.pack(pady=10)

        self.workout_label = tk.Label(self.root, text="Workout Name:", font=self.custom_font)
        self.workout_label.pack(pady=5)
        self.workout_entry = tk.Entry(self.root, font=('Arial', 12))
        self.workout_entry.pack(pady=5)

        self.Sets_label = tk.Label(self.root, text="Sets:", font=self.custom_font)
        self.Sets_label.pack(pady=5)
        self.Sets_entry = tk.Entry(self.root, font=('Arial', 12))
        self.Sets_entry.pack(pady=5)

        self.Reps_label = tk.Label(self.root, text="Reps:", font=self.custom_font)
        self.Reps_label.pack(pady=5)
        self.Reps_entry = tk.Entry(self.root, font=('Arial', 12))
        self.Reps_entry.pack(pady=5)

        self.Rest_label = tk.Label(self.root, text="Rest (Secs):", font=self.custom_font)
        self.Rest_label.pack(pady=5)
        self.Rest_entry = tk.Entry(self.root, font=('Arial', 12))
        self.Rest_entry.pack(pady=5)
        
        self.navigation_frame2 = tk.Frame(self.root, bg='#4D4D4D')
        self.navigation_frame2.pack(pady=10)

        self.add_button = tk.Button(self.navigation_frame2, text="Add Workout", command=self.add_workout, font=self.custom_font, relief="raised", bd=5)
        self.add_button.grid(row=0, column=1, padx=5)

        self.delete_button = tk.Button(self.navigation_frame2, text="Delete Workout", command=self.delete_workout, font=self.custom_font, relief="raised", bd=5)
        self.delete_button.grid(row=0, column=0, padx=5)

        self.display_button = tk.Button(self.root, text="Display Weekly Routine", command=self.show_display_window, font=self.custom_font, relief="raised", bd=5)
        self.display_button.pack(pady=10)

        self.workout_display = tk.Text(self.root, height=10, width=50, state=tk.DISABLED, font=self.custom_font)
        self.workout_display.pack(pady=10)

    def get_days(self):
        days = []
        current = self.routine.head
        while current:
            days.append(current.dayName)
            current = current.next
        return days

    def set_rest_day(self):
        day = self.day_var.get()
        self.routine.set_day(day, rest_day=True)
        messagebox.showinfo("Rest Day", f"{day} has been set as a REST DAY!")
        self.display_workouts(day)

    def set_workout_day(self):
        day = self.day_var.get()
        self.routine.set_day(day, rest_day=False)
        messagebox.showinfo("Workout Day", f"{day} has been set as a Workout Day!")
        self.display_workouts(day)

    def add_workout(self):
        day = self.day_var.get()
        workout_name = self.workout_entry.get()
        sets = self.Sets_entry.get()
        reps = self.Reps_entry.get()
        rest = self.Rest_entry.get()

        if not workout_name or not sets or not reps or not rest:
            messagebox.showerror("Input Error", "Please enter valid values for all workout fields.")
            return
        
        try:
            sets = int(sets)
            reps = int(reps)
            rest = int(rest)
        except ValueError:
            messagebox.showerror("Input Error", "Sets, Reps, and Rest must be numbers.")
            return

        result = self.routine.add_workout(day, workout_name, sets, reps, rest)
        if result:
            messagebox.showinfo("Success", f"Added workout to {day}.")
            self.display_workouts(day)
        else:
            messagebox.showerror("Error", "Cannot add workout to a rest day.")

    def delete_workout(self):
        day = self.day_var.get()
        workout_name = self.workout_entry.get()
        if not workout_name:
            messagebox.showerror("Input Error", "Please enter a workout name to delete.")
            return
        
        result = self.routine.delete_workout(day, workout_name)
        messagebox.showinfo("Deleted Workout", result)
        self.display_workouts(day)

    def show_display_window(self):
        display_window = tk.Toplevel(self.root)
        display_window.title("Weekly Workout Routine")
        display_window.geometry("600x400")

        frame = tk.Frame(display_window)
        frame.pack(fill=tk.BOTH, expand=True)

        routine_text = tk.Text(frame, height=20, width=70, wrap=tk.WORD)
        routine_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=routine_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        routine_text.config(yscrollcommand=scrollbar.set)

        routines = self.routine.display_routine()
        for day, routine in routines.items():
            routine_text.insert(tk.END, f"{day}:\n{routine}\n\n")

    def show_next_day_workouts(self):
        next_day = self.routine.next_day()
        if next_day:
            self.day_var.set(next_day.dayName)
            self.display_workouts(next_day.dayName)

    def show_previous_day_workouts(self):
        prev_day = self.routine.previous_day()
        if prev_day:
            self.day_var.set(prev_day.dayName)
            self.display_workouts(prev_day.dayName)

    def display_workouts(self, day):
        workout_list = self.routine.display_day_workouts(day)
        self.workout_display.configure(state=tk.NORMAL)
        self.workout_display.delete(1.0, tk.END)
        self.workout_display.insert(tk.END, workout_list)
        self.workout_display.configure(state=tk.DISABLED)
