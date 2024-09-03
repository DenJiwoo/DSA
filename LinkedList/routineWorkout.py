class Node:
    def __init__(self, exerciseName, sets, reps, rest): 
        self.data = {
            'exerciseName': exerciseName,
            'sets': sets,
            'reps': reps,
            'rest': rest
        }
        self.next = None
        self.prev = None

class WorkoutRoutine:
    def __init__(self):
        self.days = {
            'Sunday': None,
            'Monday': None,
            'Tuesday': None,
            'Wednesday': None,
            'Thursday': None,
            'Friday': None,
            'Saturday': None,
        }

    def set_day(self, day, rest_day): #Gives placeholder for workout nodes and initializes whether said day will be a rest day or not.
        if rest_day:
            self.days[day] = 'Rest Day'
            print(f"{day} is set as a Rest Day. SO PLEASE GO TAKE REST A KING/QUEEN!!!")
        else:
            if self.days[day] == 'Rest Day':
                self.days[day] = Node('Start of Workout', 0, 0, 0)  # Placeholder to start the workout routine
            elif self.days[day] is None:
                self.days[day] = Node('Start of Workout', 0, 0, 0)  # Placeholder to start the workout routine

    def add_exercises(self, day, exerciseName, sets, reps, rest):
        if self.days[day] == 'Rest Day':
            print(f"{day} is set as a REST DAY.")
            return

        new_node = Node(exerciseName, sets, reps, rest)
        if self.days[day] is not None and self.days[day].data['exerciseName'] == 'Start of Workout':
            self.days[day] = new_node
        else:
            last = self.days[day]
            while last.next:
                last = last.next
            last.next = new_node
            new_node.prev = last

    def display_routine(self):
        for day, head in self.days.items():
            print(f"\n{day}:")
            if head == 'Rest Day':
                print(" It's a Rest Day!!!")
            elif head is None:
                print(" No exercises scheduled.")
            else:
                node = head
                while node:
                    data = node.data
                    print(f" {data['exerciseName']} - {data['sets']} sets of {data['reps']} reps with {data['rest']} seconds rest")
                    node = node.next

    def delete_exercise(self, day, exerciseName):
        if day not in self.days:
            print(f"Invalid day: {day}")
            return

        if self.days[day] == 'Rest Day':
            print(f"No exercises to delete on {day} because it's a Rest Day.")
            return

        if self.days[day] is None:
            print(f"No exercises scheduled for {day}.")
            return

        current = self.days[day]
        while current:
            if current.data['exerciseName'] == exerciseName:
                if current.prev:
                    current.prev.next = current.next
                if current.next:
                    current.next.prev = current.prev
                if current == self.days[day]:
                    self.days[day] = current.next
                print(f"Exercise '{exerciseName}' deleted from {day}.")
                return
            current = current.next

        print(f"Exercise '{exerciseName}' not found on {day}.")

def menu():
    routine = WorkoutRoutine()

    while True:
        print("\n + Fitness Planner +")
        print("1. Set Day as a Workout/Rest Day")
        print("2. Add Workout")
        print("3. Display Weekly Routine")
        print("4. Delete Workout")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            day = input("Enter the day (Monday to Sunday): ").capitalize()
            if day not in routine.days:
                print(f"{day} is not a valid day!")
                continue
            is_rest = input(f"Do you want to set {day} as a Rest Day? (yes/no): ").lower()
            routine.set_day(day, is_rest == 'yes')

        elif choice == '2':
            day = input("Enter the day (Monday to Sunday): ").capitalize()
            if day not in routine.days or routine.days[day] == 'Rest Day':
                print(f"{day} is not set as a Workout Day.")
                continue
            workout_name = input("Enter workout name: ")
            sets = int(input("Enter number of sets: "))
            reps = int(input("Enter number of reps per set: "))
            rest = int(input("Enter rest time between sets (in seconds): "))
            routine.add_exercises(day, workout_name, sets, reps, rest)
        
        elif choice == '3':
            routine.display_routine()
        
        elif choice == '4':
            day = input("Enter the day (Monday to Sunday): ").capitalize()
            if day not in routine.days or routine.days[day] == 'Rest Day':
                print(f"{day} is not set as a workout Day.")
                continue
            workout_name = input("Enter the name of the exercise to delete: ")
            routine.delete_exercise(day, workout_name)
        
        elif choice == '5':
            print("Babyeeee!!!")
            break
        else:
            print("Invalid choice, try again")

menu()
