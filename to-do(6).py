import streamlit as st
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
    """Displays the menu options and returns the selected choice."""
    menu_options = ["View All Tasks", "View Tasks Sorted by Priority", "View Pending Tasks", "View Completed Tasks", "Add Task", "Mark Task as Complete", "Remove Task", "Exit"]
    selected_option = st.selectbox("Select an option:", menu_options)
    return selected_option

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
        st.write("\nYour to-do list is empty!")
        return

    if option == "all":
        tasks_to_view = todo_list
        title = "All Tasks"
    elif option == "priority":
        tasks_to_view = sorted(
            todo_list,
            key=lambda x: (
                x['priority'],
                datetime.strptime(x['deadline'], "%d/%m/%Y") if x['deadline'] else datetime.max
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
        st.error("Invalid viewing option.")
        return

    if not tasks_to_view:
        st.write(f"\nNo tasks found for the selected option: {title}.")
    else:
        st.write(f"\n{title}:")
        for idx, task in enumerate(tasks_to_view, 1):
            status = "✓" if task['completed'] else "✗"
            deadline = task.get('deadline', "No deadline")
            st.write(f"{idx}. {task['name']} [Priority: {task['priority']}] [Deadline: {deadline}] [{status}]")

def add_task():
    """Prompts the user for task details, validates input, and adds the task to the list."""
    task_name = st.text_input("Enter the task you want to add:")
    if task_name:
        try:
            priority = st.number_input("Enter the priority of the task (1 = highest priority):", min_value=1)

            # Validate and get deadline input in DD/MM/YYYY format
            while True:
                deadline = st.text_input("Enter the deadline (DD/MM/YYYY) or leave blank for no deadline:")
                if not deadline:  # Allow blank input for no deadline
                    deadline = None
                    break
                try:
                    # Parse and format date as DD/MM/YYYY
                    deadline_date = datetime.strptime(deadline, "%d/%m/%Y") 
                    today = datetime.now()
                    if deadline_date < today
