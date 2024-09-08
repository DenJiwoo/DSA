import tkinter as tk
from tkinter import ttk, messagebox

class Node: # Node class represents an exercise with linked list structure
    def __init__(self, workoutName, sets, reps, rest):
        self.data = {
            'workoutName': workoutName,
            'sets': sets,
            'reps': reps,
            'rest': rest
        }
        self.next = None
        self.prev = None

class DayNode: # DayNode class represents a day with its exercises (linked list)
    def __init__(self, dayName):
        self.dayName = dayName
        self.workoutList = None # Head of the doubly linked list for exercises
        self.next = None
        self.prev = None

class WorkoutRoutine: # WorkoutRoutine class handles operations on the workout routine
    def __init__(self):
        self.head = None
        self.tail = None
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

    def find_day(self, day_name):
        current = self.head
        while current:
            if current.dayName == day_name:
                return current
            current = current.next
        return None

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

    def delete_workout(self, day, workoutName):
        day_node = self.find_day(day)
        if not day_node or day_node.workoutList == 'Rest Day.':
            return f"No workouts to delete on {day} because it's a Rest Day."

        current = day_node.workoutList
        while current:
            if current.data['workoutName'] == workoutName:
                if current.prev:
                    current.prev.next = current.next
                if current.next:
                    current.next.prev = current.prev
                if current == day_node.workoutList:
                    day_node.workoutList = current.next
                return f"Workout '{workoutName}' deleted from {day}."
            current = current.next
        return f"Workout '{workoutName}' not found on {day}."

class WorkoutPlanner: # Class that represents as the UI for the program
    def __init__(self, root):
        self.root = root
        self.root.title("Workout Planner")
        self.root.geometry("500x600")
        self.routine = WorkoutRoutine()

        self.create_widgets()

    def create_widgets(self): # Day selection
        self.day_label = tk.Label(self.root, text="Select Day: ")
        self.day_label.pack(pady=10)
        self.day_var = tk.StringVar(value="Monday")
        self.day_menu = ttk.Combobox(self.root, textvariable=self.day_var, value=self.get_days(), state='readonly')
        self.day_menu.pack(pady=10)

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

        # Display Routine in a new window
        self.display_button = tk.Button(self.root, text="Display Weekly Routine", command=self.show_display_window)
        self.display_button.pack(pady=10)

        # Delete Workout
        self.delete_button = tk.Button(self.root, text="Delete Workout", command=self.delete_workout)
        self.delete_button.pack(pady=10)

    def get_days(self): # Implements the logic/function into the UI
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
            messagebox.showerror("Input Error", "Please fill in all fields correctly.")
            return

        self.routine.add_Workouts(day, workout_name, int(sets), int(reps), int(rest))
        messagebox.showinfo("Success", f"Workout added to {day}!")

    def show_display_window(self):
        # Create a new window for displaying the weekly routine
        display_window = tk.Toplevel(self.root)
        display_window.title("Weekly Workout Routine")
        display_window.geometry("600x400")

        # Add a Text widget to display the routine
        routine_text = tk.Text(display_window, height=20, width=70)
        routine_text.pack(pady=10)

        # Fetch and display the routine
        routines = self.routine.display_routine()
        for day, routine in routines.items():
            routine_text.insert(tk.END, f"{day}:\n{routine}\n\n")

    def delete_workout(self):
        day = self.day_var.get()
        workout_name = self.workout_entry.get()
        if not workout_name:
            messagebox.showerror("Input Error", "Please enter a workout name to delete.")
            return

        result = self.routine.delete_workout(day, workout_name)
        messagebox.showinfo("Deleted Workout", result)

# Running the Application
if __name__ == "__main__":
    root = tk.Tk()
    app = WorkoutPlanner(root)
    root.mainloop()
