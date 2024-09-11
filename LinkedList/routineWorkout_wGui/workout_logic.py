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
                workouts.append(f"{current.data['workoutName']} - {current.data['sets']} sets of {current.data['reps']} reps with {current.data['rest']} seconds of rest")
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
