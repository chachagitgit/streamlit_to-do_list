import json
from datetime import datetime

todo_list = []
filename = "todo_list.json"

def load_data():
    """Loads the to-do list from a JSON file."""
    try:
        with open(filename, 'r') as f:
            global todo_list
            todo_list = json.load(f)
    except FileNotFoundError:
        pass  # If the file doesn't exist, start with an empty list

def save_data():
    """Saves the to-do list to a JSON file."""
    with open(filename, 'w') as f:
        json.dump(todo_list, f, indent=2)

def display_menu():
    print("\nTo-Do List Menu:")
    print("1. View All Tasks")
    print("2. View Tasks Sorted by Priority")
    print("3. View Pending Tasks")
    print("4. View Completed Tasks")
    print("5. Add Task")
    print("6. Mark Task as Complete")
    print("7. Remove Task")
    print("8. Exit")

def view_tasks(option="all"):
    """
    Displays tasks based on the selected option.
    Options:
    - "all": View all tasks without sorting.
    - "priority": View tasks sorted by priority and then by deadline.
    - "pending": View only pending tasks, sorted by priority and deadline.
    - "completed": View only completed tasks, sorted by priority and deadline.
    """
    if not todo_list:
        print("\nYour to-do list is empty!")
        return

    if option == "all":
        tasks_to_view = todo_list
        title = "All Tasks"
    elif option == "priority":
        tasks_to_view = sorted(
            todo_list,
            key=lambda x: (
                x['priority'],  # Sort by priority
                datetime.strptime(x['deadline'], "%d/%m/%Y") if x['deadline'] else datetime.max  # Sort by deadline
            )
        )
        title = "Tasks Sorted by Priority and Deadline"
    elif option == "pending":
        tasks_to_view = sorted(
            [task for task in todo_list if not task['completed']],
            key=lambda x: (
                x['priority'], 
                datetime.strptime(x['deadline'], "%d/%m/%Y") if x['deadline'] else datetime.max
            )
        )
        title = "Pending Tasks"
    elif option == "completed":
        tasks_to_view = sorted(
            [task for task in todo_list if task['completed']],
            key=lambda x: (
                x['priority'], 
                datetime.strptime(x['deadline'], "%d/%m/%Y") if x['deadline'] else datetime.max
            )
        )
        title = "Completed Tasks"
    else:
        print("Invalid viewing option.")
        return

    if not tasks_to_view:
        print(f"\nNo tasks found for the selected option: {title}.")
    else:
        print(f"\n{title}:")
        for idx, task in enumerate(tasks_to_view, 1):
            status = "✓" if task['completed'] else "✗"
            deadline = task.get('deadline', "No deadline")
            print(f"{idx}. {task['name']} [Priority: {task['priority']}] [Deadline: {deadline}] [{status}]")


def add_task():
    task_name = input("\nEnter the task you want to add: ").strip()
    if task_name:
        try:
            priority = int(input("Enter the priority of the task (1 = highest priority): ").strip())

            # Validate and get deadline input in DD/MM/YYYY format
            while True:
                deadline = input("Enter the deadline (DD/MM/YYYY) or leave blank for no deadline: ").strip()
                if not deadline:  # Allow blank input for no deadline
                    deadline = None
                    break
                try:
                    # Parse and format date as DD/MM/YYYY
                    deadline_date = datetime.strptime(deadline, "%d/%m/%Y") 
                    today = datetime.now()
                    if deadline_date < today:
                        print("Error: Deadline cannot be in the past.")
                        continue  # Continue the loop to ask for input again
                    deadline = deadline_date.strftime("%d/%m/%Y") 
                    break  # Valid date entered
                except ValueError:
                    print("Invalid date format. Please try again (format: DD/MM/YYYY).")

            todo_list.append({'name': task_name, 'priority': priority, 'deadline': deadline, 'completed': False})
            print(f"Task '{task_name}' with priority {priority} added.")
            save_data()  # Save after adding a task
        except ValueError:
            print("Invalid priority. Please enter a number.")
    else:
        print("Task cannot be empty.")

def mark_complete():
    try:
        # Display pending tasks sorted by priority and deadline
        print("\nPending Tasks:")
        pending_tasks = sorted(
            [task for task in todo_list if not task['completed']],
            key=lambda x: (
                x['priority'],
                datetime.strptime(x['deadline'], "%d/%m/%Y") if x['deadline'] else datetime.max
            )
        )
        if not pending_tasks:
            print("No pending tasks to mark as complete.")
            return

        for idx, task in enumerate(pending_tasks, 1):
            status = "✓" if task['completed'] else "✗"
            deadline = task.get('deadline', "No deadline")
            print(f"{idx}. {task['name']} [Priority: {task['priority']}] [Deadline: {deadline}] [{status}]")

        # User selects task to mark as complete
        task_number = int(input("\nEnter the number of the task you want to mark as complete: ").strip())
        if 1 <= task_number <= len(pending_tasks):
            selected_task = pending_tasks[task_number - 1]
            # Find and update the corresponding task in the original todo_list
            for task in todo_list:
                if task == selected_task:
                    task['completed'] = True
                    break
            print(f"Task '{selected_task['name']}' marked as complete.")
            save_data()
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid task number.")



def remove_task():
    try:
        # Display all tasks sorted by priority and deadline
        print("\nAll Tasks:")
        sorted_tasks = sorted(
            todo_list,
            key=lambda x: (
                x['priority'],
                datetime.strptime(x['deadline'], "%d/%m/%Y") if x['deadline'] else datetime.max
            )
        )
        if not sorted_tasks:
            print("No tasks to remove.")
            return

        for idx, task in enumerate(sorted_tasks, 1):
            status = "✓" if task['completed'] else "✗"
            deadline = task.get('deadline', "No deadline")
            print(f"{idx}. {task['name']} [Priority: {task['priority']}] [Deadline: {deadline}] [{status}]")

        # User selects task to remove
        task_number = int(input("\nEnter the number of the task you want to remove: ").strip())
        if 1 <= task_number <= len(sorted_tasks):
            selected_task = sorted_tasks[task_number - 1]
            # Remove the corresponding task from the original todo_list
            todo_list.remove(selected_task)
            print(f"Task '{selected_task['name']}' removed.")
            save_data()
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid task number.")


def main():
    load_data()  # Load the to-do list from the file

    while True:
        display_menu()
        choice = input("\nEnter your choice (1-8): ").strip()
        if choice == "1":
            view_tasks(option="all")
        elif choice == "2":
            view_tasks(option="priority")
        elif choice == "3":
            view_tasks(option="pending")
        elif choice == "4":
            view_tasks(option="completed")
        elif choice == "5":
            add_task()
        elif choice == "6":
            mark_complete()
        elif choice == "7":
            remove_task()
        elif choice == "8":
            print("Exiting the To-Do List. Goodbye!")
            save_data()  # Save the to-do list before exiting
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()