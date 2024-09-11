import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import PhotoImage
from PIL import Image, ImageTk
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
        self.root.resizable(False, False)
        self.routine = WorkoutRoutine()
        self.create_widgets()      

    def create_widgets(self):
        self.root.config(background="#4D4D4D")
    
        # Create the day label
        self.day_label = tk.Label(self.root, text="Select Day: ", font=("Lato", 15, "bold italic"), 
                                  bg='#222222', foreground="white")
        self.day_label.pack(pady=10)
    
        # Create the day menu
        self.day_var = tk.StringVar(value="Sunday")
        self.day_menu = ttk.Combobox(self.root, textvariable=self.day_var, value=self.get_days(), state='readonly')
        self.day_menu.pack(pady=20)

        # Create navigation frame and buttons
        self.navigation_frame1 = tk.Frame(self.root, bg='#292929')
        self.navigation_frame1.pack(pady=10)
    
        self.previous_day_button = tk.Button(self.navigation_frame1, text="Previous Day", 
                                             command=self.show_previous_day_workouts, font=self.custom_font, 
                                             relief="raised", bd=5, cursor="hand2")
        self.previous_day_button.grid(row=0, column=0, padx=5)
        self.previous_day_button.bind("<Enter>", lambda e: self.on_hover(self.previous_day_button))
        self.previous_day_button.bind("<Leave>", lambda e: self.off_hover(self.previous_day_button))

        self.next_day_button = tk.Button(self.navigation_frame1, text="Next Day", 
                                         command=self.show_next_day_workouts, font=self.custom_font, 
                                         relief="raised", bd=5, cursor="hand2")
        self.next_day_button.grid(row=0, column=1, padx=5)
        self.next_day_button.bind("<Enter>", lambda e: self.on_hover(self.next_day_button))
        self.next_day_button.bind("<Leave>", lambda e: self.off_hover(self.next_day_button))


        # Create navigation frame 2 for rest day and workout day buttons
        self.navigation_frame2 = tk.Frame(self.root, bg='#303030')
        self.navigation_frame2.pack(pady=15)
        
        self.rest_day_button = tk.Button(self.navigation_frame2, text="Set as Rest Day", 
                                         command=self.set_rest_day, font=self.custom_font, 
                                         relief="raised", bd=5, cursor="hand2")
        self.rest_day_button.grid(row=0, column=0, padx=5)
        self.rest_day_button.bind("<Enter>", lambda e: self.on_hover(self.rest_day_button))
        self.rest_day_button.bind("<Leave>", lambda e: self.off_hover(self.rest_day_button))

        self.workout_day_button = tk.Button(self.navigation_frame2, text="Set as Workout Day", 
                                            command=self.set_workout_day, font=self.custom_font, 
                                            relief="raised", bd=5, cursor="hand2")
        self.workout_day_button.grid(row=0, column=1, padx=5)
        self.workout_day_button.bind("<Enter>", lambda e: self.on_hover(self.workout_day_button))
        self.workout_day_button.bind("<Leave>", lambda e: self.off_hover(self.workout_day_button))

        # WORKOUT name entry box
        self.workout_label = tk.Label(self.root, text="Workout Name:", font=("Lato", 15, "bold italic"), 
                                      bg='#343434', foreground="white")
        self.workout_label.pack(pady=5)
        self.workout_entry = tk.Entry(self.root, font=('Arial', 12, "bold"))
        self.workout_entry.pack(pady=5)

        # Number of SETS entry box
        self.Sets_label = tk.Label(self.root, text="Sets:", font=("Lato", 15, "bold italic"), 
                                   bg='#323232', foreground="white")
        self.Sets_label.pack(pady=5)
        self.Sets_entry = tk.Entry(self.root, font=('Arial', 12, "bold"))
        self.Sets_entry.pack(pady=5)

        # Number of REPS entry box
        self.Reps_label = tk.Label(self.root, text="Reps:", font=("Lato", 15, "bold italic"), 
                                   bg='#373737', foreground="white")
        self.Reps_label.pack(pady=5)
        self.Reps_entry = tk.Entry(self.root, font=('Arial', 12, "bold"))
        self.Reps_entry.pack(pady=5)

        # SECONDS OF REST entry box
        self.Rest_label = tk.Label(self.root, text="Rest (Secs):", font=("Lato", 15, "bold italic"), 
                                    bg='#404040', foreground="white")
        self.Rest_label.pack(pady=5)
        self.Rest_entry = tk.Entry(self.root, font=('Arial', 12, "bold"))
        self.Rest_entry.pack(pady=10)
    
    
        # Create navigation frame 3 for add and delete buttons
        self.navigation_frame3 = tk.Frame(self.root, bg='#4D4D4D')
        self.navigation_frame3.pack(pady=15)

        self.add_button = tk.Button(self.navigation_frame3, text="Add Workout", 
                                    command=self.add_workout, font=self.custom_font, 
                                    relief="raised", bd=5, cursor="hand2")
        self.add_button.grid(row=0, column=1, padx=5)
        self.add_button.bind("<Enter>", lambda e: self.on_hover(self.add_button))
        self.add_button.bind("<Leave>", lambda e: self.off_hover(self.add_button))

        self.delete_button = tk.Button(self.navigation_frame3, text="Delete Workout", 
                                       command=self.delete_workout, font=self.custom_font, 
                                       relief="raised", bd=5, cursor="hand2")
        self.delete_button.grid(row=0, column=0, padx=5)
        self.delete_button.bind("<Enter>", lambda e: self.on_hover(self.delete_button))
        self.delete_button.bind("<Leave>", lambda e: self.off_hover(self.delete_button))

        # Displays the overall WEEKLY ROUTINE
        self.display_button = tk.Button(self.root, text="Display Weekly Routine", 
                                        command=self.show_display_window, font=self.custom_font, 
                                        relief="raised", bd=5, cursor="hand2")
        self.display_button.pack(pady=10)
        self.display_button.bind("<Enter>", lambda e: self.on_hover(self.display_button))
        self.display_button.bind("<Leave>", lambda e: self.off_hover(self.display_button))

        # CreateS the SINGLE workout display
        self.workout_display = tk.Text(self.root, height=10, width=50, 
                                       state=tk.DISABLED, font=('Arial', 12, "bold"))
        self.workout_display.pack(pady=10)

    def on_hover(self, button):
        button.config(bg="lightgray")  # Change background color on hover

    def off_hover(self, button):
        button.config(bg="SystemButtonFace")  # Reset background color when not hovering

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
            messagebox.showerror("Input Error", "Sets, Reps, and Rest must be in numbers.")
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
        display_window.resizable(False, False)

        frame = tk.Frame(display_window, bg='#343434')
        frame.pack(fill=tk.BOTH, expand=True)

        # Create the Text widget with the background color
        routine_text = tk.Text(frame, height=20, width=70, 
                               wrap=tk.WORD, bg='#343434', fg='white',
                               font=("Lato", 15, "bold italic"))
        routine_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=routine_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        routine_text.config(yscrollcommand=scrollbar.set)

        routines = self.routine.display_routine()
        for day, routine in routines.items():
            routine_text.insert(tk.END, f"{day}:\n{routine}\n\n")
        routine_text.config(state=tk.DISABLED) # Disable the Text widget to make it read-only

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
