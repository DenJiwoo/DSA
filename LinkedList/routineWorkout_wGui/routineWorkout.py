import tkinter as tk
from tkinter import ttk, messagebox

class Node:  # Node class represents an exercise with linked list structure
    def __init__(self, workoutName, sets, reps, rest):
        self.data = {
            'workoutName': workoutName,
            'sets': sets,
            'reps': reps,
            'rest': rest
        }
        self.next = None
        self.prev = None

class DayNode:  # DayNode class represents a day with its exercises (linked list)
    def __init__(self, dayName):
        self.dayName = dayName
        self.workoutList = None  # Head of the doubly linked list for exercises
        self.next = None
        self.prev = None

class WorkoutRoutine:  # WorkoutRoutine class handles operations on the workout routine
    def __init__(self):
        self.head = None
        self.tail = None
        self.current_day = None  # Track the current day for navigation
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
        self.current_day = self.head  # Start with the head (Sunday)

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
                if day_node.workoutList == 'Rest Day.' or day_node.workoutList is None:
                    day_node.workoutList = Node('Start of Workout', 0, 0, 0)

    def add_Workouts(self, day, workoutName, sets, reps, rest):
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

class WorkoutPlanner:  # Class that represents the UI for the program
    def __init__(self, root):
        self.root = root
        self.root.title("Workout Planner")
        self.root.geometry("500x600")
        self.routine = WorkoutRoutine()

        self.create_widgets()

    def create_widgets(self):  # Day selection
        self.day_label = tk.Label(self.root, text="Select Day: ")
        self.day_label.pack(pady=10)
        self.day_var = tk.StringVar(value="Monday")
        self.day_menu = ttk.Combobox(self.root, textvariable=self.day_var, value=self.get_days(), state='readonly')
        self.day_menu.pack(pady=10)
        
        # Navigation Buttons for Viewing Day
        self.next_day_button = tk.Button(self.root, text="Next Day", command=self.show_next_day_workouts)
        self.next_day_button.pack(pady=5)

        self.previous_day_button = tk.Button(self.root, text="Previous Day", command=self.show_previous_day_workouts)
        self.previous_day_button.pack(pady=5)

        # Set Day as Rest Day
        self.rest_day_button = tk.Button(self.root, text="Set as Rest Day", command=self.set_rest_day)
        self.rest_day_button.pack(pady=10)

        # Set Day as Workout Day
        self.workout_day_button = tk.Button(self.root, text="Set as Workout Day", command=self.set_workout_day)
        self.workout_day_button.pack(pady=10)

        # Add Workout
        self.workout_label = tk.Label(self.root, text="Workout Name:")
        self.workout_label.pack(pady=5)
        self.workout_entry = tk.Entry(self.root)
        self.workout_entry.pack(pady=5)

        self.Sets_label = tk.Label(self.root, text="Sets:")
        self.Sets_label.pack(pady=5)
        self.Sets_entry = tk.Entry(self.root)
        self.Sets_entry.pack(pady=5)

        self.Reps_label = tk.Label(self.root, text="Reps:")
        self.Reps_label.pack(pady=5)
        self.Reps_entry = tk.Entry(self.root)
        self.Reps_entry.pack(pady=5)

        self.Rest_label = tk.Label(self.root, text="Rest (Secs):")
        self.Rest_label.pack(pady=5)
        self.Rest_entry = tk.Entry(self.root)
        self.Rest_entry.pack(pady=5)
                            
        self.add_button = tk.Button(self.root, text="Add Workout", command=self.add_workout)
        self.add_button.pack(pady=10)

        self.display_button = tk.Button(self.root, text="Display Weekly Routine", command=self.show_display_window)
        self.display_button.pack(pady=10)

        self.delete_button = tk.Button(self.root, text="Delete Workout", command=self.delete_workout)
        self.delete_button.pack(pady=10)

        # Text box to display the current day's workouts
        self.workout_display = tk.Text(self.root, height=10, width=50, state=tk.DISABLED)
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

    def set_workout_day(self):
        day = self.day_var.get()
        self.routine.set_day(day, rest_day=False)
        messagebox.showinfo("Workout Day", f"{day} has been set as a Workout Day!")

    def add_workout(self):
        day = self.day_var.get()
        workout_name = self.workout_entry.get()
        sets = self.Sets_entry.get()
        reps = self.Reps_entry.get()
        rest = self.Rest_entry.get()
       
        if not (workout_name and sets.isdigit() and reps.isdigit() and rest.isdigit()):
            messagebox.showerror("Input Error", "Please fill in all the blanks correctly.")
            return
       
        result = self.routine.add_Workouts(day, workout_name, int(sets), int(reps), int(rest))
        if result == "Rest Day":
            messagebox.showerror("Error", f"{day} is set as a Rest Day.")
        else:
            messagebox.showinfo("Success", f"Workout added to {day}!")

    def show_display_window(self):
        # Create a new window for displaying the weekly routine
        display_window = tk.Toplevel(self.root)
        display_window.title("Weekly Workout Routine")
        display_window.geometry("600x400")

        # Create a frame to hold the Text widget and Scrollbar
        frame = tk.Frame(display_window)
        frame.pack(fill=tk.BOTH, expand=True)

        # Add a Text widget to display the routine
        routine_text = tk.Text(frame, height=20, width=70, wrap=tk.WORD)
        routine_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add a Scrollbar to the Text widget
        scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=routine_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        routine_text.config(yscrollcommand=scrollbar.set)

        # Fetch and display the routine
        routines = self.routine.display_routine()
        for day, routine in routines.items():
            routine_text.insert(tk.END, f"{day}:\n{routine}\n\n")

        # Make the Text widget read-only
        routine_text.config(state=tk.DISABLED)

    def delete_workout(self):
        day = self.day_var.get()
        workout_name = self.workout_entry.get()
        if not workout_name:
            messagebox.showerror("Input Error", "Please enter a workout name to delete.")
            return
        
        result = self.routine.delete_workout(day, workout_name)
        messagebox.showinfo("Deleted Workout", result)

    def view_day(self):
        day = self.day_var.get()
        day_workouts = self.routine.display_day_workouts(day)
    
    # Temporarily enable the text box to insert new text
        self.workout_display.config(state=tk.NORMAL)
        self.workout_display.delete(1.0, tk.END)  # Clear the current display
        self.workout_display.insert(tk.END, day_workouts)
        self.workout_display.config(state=tk.DISABLED)  # Disable it again to prevent typing

    def show_next_day_workouts(self):
        day_node = self.routine.next_day()
        if day_node:
            self.day_var.set(day_node.dayName)  # Update combobox
        day_workouts = self.routine.display_day_workouts(day_node.dayName)
        
        # Temporarily enable the text box to insert new text
        self.workout_display.config(state=tk.NORMAL)
        self.workout_display.delete(1.0, tk.END)  # Clear the current display
        self.workout_display.insert(tk.END, day_workouts)
        self.workout_display.config(state=tk.DISABLED)  # Disable it again to prevent typing

    def show_previous_day_workouts(self):
        day_node = self.routine.previous_day()
        if day_node:
            self.day_var.set(day_node.dayName)  # Update combobox
        day_workouts = self.routine.display_day_workouts(day_node.dayName)
        
        # Temporarily enable the text box to insert new text
        self.workout_display.config(state=tk.NORMAL)
        self.workout_display.delete(1.0, tk.END)  # Clear the current display
        self.workout_display.insert(tk.END, day_workouts)
        self.workout_display.config(state=tk.DISABLED)  # Disable it again to prevent typing

# Running the Application
if __name__ == "__main__":
    root = tk.Tk()
    app = WorkoutPlanner(root)
    root.mainloop()
