import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkFont
import os

class Node:
    def __init__(self, workoutName, sets, reps, rest):
        self.data = {
            'workoutName': workoutName,
            'sets': sets,
            'reps': reps,
            'rest': rest
        }
        self.next = None
        self.prev = None

class DayNode:
    def __init__(self, dayName):
        self.dayName = dayName
        self.workoutList = None
        self.next = None
        self.prev = None

class WorkoutRoutine:
    def __init__(self):
        self.head = None
        self.tail = None
        self.current_day = None
        self.initialize_days()

    def initialize_days(self):
        days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        previous_day = None
        for day in days:
            new_day = DayNode(day)
            if self.head is None:
                self.head = new_day
            if previous_day is not None:
                previous_day.next = new_day
                new_day.prev = previous_day
            previous_day = new_day
        self.tail = previous_day
        self.current_day = self.head

    def find_day(self, day_name):
        current = self.head
        while current:
            if current.dayName == day_name:
                return current
            current = current.next
        return None

    def next_day(self):
        if self.current_day and self.current_day.next:
            self.current_day = self.current_day.next
        return self.current_day

    def previous_day(self):
        if self.current_day and self.current_day.prev:
            self.current_day = self.current_day.prev
        return self.current_day

    def set_day(self, day, rest_day):
        day_node = self.find_day(day)
        if day_node:
            if rest_day:
                day_node.workoutList = 'Rest Day.'
            else:
                if day_node.workoutList == 'Rest Day.':
                    day_node.workoutList = None
                if day_node.workoutList is None:
                    day_node.workoutList = Node('Start of Workout', 0, 0, 0)

    def add_workout(self, day, workoutName, sets, reps, rest):
        day_node = self.find_day(day)
        if day_node and day_node.workoutList != 'Rest Day.':
            new_node = Node(workoutName, sets, reps, rest)
            if day_node.workoutList.data['workoutName'] == 'Start of Workout':
                day_node.workoutList = new_node
            else:
                last = day_node.workoutList
                while last.next:
                    last = last.next
                last.next = new_node
                new_node.prev = last
            return True
        return False

    def delete_workout(self, day, workout_name):
        day_node = self.find_day(day)
        if day_node and day_node.workoutList != 'Rest Day.':
            current = day_node.workoutList
            prev_node = None
            while current:
                if current.data['workoutName'] == workout_name:
                    if prev_node:
                        prev_node.next = current.next
                        if current.next:
                            current.next.prev = prev_node
                    else:
                        day_node.workoutList = current.next
                        if day_node.workoutList:
                            day_node.workoutList.prev = None
                    return f"{workout_name} deleted from {day}."
                prev_node = current
                current = current.next
            return f"Workout '{workout_name}' not found in {day}."
        return f"Cannot delete from rest day or invalid day."

    def display_day_workouts(self, day_name):
        day_node = self.find_day(day_name)
        if day_node.workoutList == 'Rest Day.':
            return f"{day_node.dayName}: Rest Day."
        elif day_node.workoutList is None:
            return f"{day_node.dayName}: No workout scheduled."
        else:
            workouts = []
            current = day_node.workoutList
            while current:
                workouts.append(f"{current.data['workoutName']} - {current.data['sets']} sets of {current.data['reps']} reps with {current.data['rest']} seconds rest")
                current = current.next
            return f"{day_node.dayName}:\n" + "\n".join(workouts)

    def display_routine(self):
        routines = {}
        day_node = self.head
        while day_node:
            if day_node.workoutList == 'Rest Day.':
                routines[day_node.dayName] = 'Rest Day.'
            elif day_node.workoutList is None:
                routines[day_node.dayName] = 'No workout scheduled.'
            else:
                routine_list = []
                node = day_node.workoutList
                while node:
                    data = node.data
                    routine_list.append(f"{data['workoutName']} - {data['sets']} sets of {data['reps']} reps with {data['rest']} seconds of rest")
                    node = node.next
                routines[day_node.dayName] = "\n".join(routine_list)
            day_node = day_node.next
        return routines

class WorkoutPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Workout Planner")
        self.root.geometry("500x850")
        self.custom_font = tkFont.Font(family="Lato", size=12, weight="normal", slant="italic") if "Lato" in tkFont.families() else tkFont.Font(family="Arial", size=12, slant="italic")

        self.routine = WorkoutRoutine()
        self.create_widgets()

    def create_widgets(self):
        self.day_label = tk.Label(self.root, text="Select Day: ", font=self.custom_font)
        self.day_label.pack(pady=10)
        self.day_var = tk.StringVar(value="Monday")

        self.day_menu = ttk.Combobox(self.root, textvariable=self.day_var, value=self.get_days(), state='readonly')
        self.day_menu.pack(pady=10)

        self.navigation_frame = tk.Frame(self.root)
        self.navigation_frame.pack(pady=10)

        self.previous_day_button = tk.Button(self.navigation_frame, text="Previous Day", command=self.show_previous_day_workouts, font=self.custom_font)
        self.previous_day_button.grid(row=0, column=0, padx=5)

        self.next_day_button = tk.Button(self.navigation_frame, text="Next Day", command=self.show_next_day_workouts, font=self.custom_font)
        self.next_day_button.grid(row=0, column=1, padx=5)

        self.rest_day_button = tk.Button(self.root, text="Set as Rest Day", command=self.set_rest_day, font=self.custom_font)
        self.rest_day_button.pack(pady=10)

        self.workout_day_button = tk.Button(self.root, text="Set as Workout Day", command=self.set_workout_day, font=self.custom_font)
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

        self.add_button = tk.Button(self.root, text="Add Workout", command=self.add_workout, font=self.custom_font)
        self.add_button.pack(pady=10)

        self.delete_button = tk.Button(self.root, text="Delete Workout", command=self.delete_workout, font=self.custom_font)
        self.delete_button.pack(pady=10)

        self.display_button = tk.Button(self.root, text="Display Weekly Routine", command=self.show_display_window, font=self.custom_font)
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


# Running the Application
if __name__ == "__main__":
    root = tk.Tk()
    app = WorkoutPlanner(root)
    root.mainloop()
