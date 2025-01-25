import json
import streamlit as st
from datetime import datetime

# File and data initialization
filename = "todo_list.json"
todo_list = []

# Load and save data functions
def load_data():
    """Loads the to-do list from a JSON file."""
    global todo_list
    try:
        with open(filename, "r") as f:
            todo_list = json.load(f)
    except FileNotFoundError:
        todo_list = []  # Start with an empty list if no file exists

def save_data():
    """Saves the to-do list to a JSON file."""
    with open(filename, "w") as f:
        json.dump(todo_list, f, indent=2)

# Task viewing functions
def get_sorted_tasks(option="all"):
    if option == "all":
        return todo_list
    elif option == "priority":
        return sorted(
            todo_list,
            key=lambda x: (
                x["priority"],
                datetime.strptime(x["deadline"], "%d/%m/%Y") if x["deadline"] else datetime.max,
            ),
        )
    elif option == "pending":
        return sorted(
            [task for task in todo_list if not task["completed"]],
            key=lambda x: (
                x["priority"],
                datetime.strptime(x["deadline"], "%d/%m/%Y") if x["deadline"] else datetime.max,
            ),
        )
    elif option == "completed":
        return sorted(
            [task for task in todo_list if task["completed"]],
            key=lambda x: (
                x["priority"],
                datetime.strptime(x["deadline"], "%d/%m/%Y") if x["deadline"] else datetime.max,
            ),
        )

# Main application
def main():
    st.title("To-Do List Manager")
    load_data()  # Load data at the start

    # Sidebar menu
    menu = [
        "View All Tasks",
        "View Tasks Sorted by Priority and Deadline",
        "View Pending Tasks",
        "View Completed Tasks",
        "Add Task",
        "Mark Task Complete",
        "Remove Task",
    ]
    choice = st.sidebar.selectbox("Menu", menu)

    # Display tasks
    if choice == "View All Tasks":
        st.header("All Tasks")
        tasks = get_sorted_tasks("all")
        if tasks:
            for idx, task in enumerate(tasks, 1):
                status = "✓" if task["completed"] else "✗"
                deadline = task["deadline"] or "No deadline"
                st.write(f"{idx}. {task['name']} [Priority: {task['priority']}] [Deadline: {deadline}] [{status}]")
        else:
            st.write("No tasks to display.")

    elif choice == "View Tasks Sorted by Priority and Deadline":
        st.header("Tasks Sorted by Priority and Deadline")
        tasks = get_sorted_tasks("priority")
        if tasks:
            for idx, task in enumerate(tasks, 1):
                status = "✓" if task["completed"] else "✗"
                deadline = task["deadline"] or "No deadline"
                st.write(f"{idx}. {task['name']} [Priority: {task['priority']}] [Deadline: {deadline}] [{status}]")
        else:
            st.write("No tasks to display.")

    elif choice == "View Pending Tasks":
        st.header("Pending Tasks")
        tasks = get_sorted_tasks("pending")
        if tasks:
            for idx, task in enumerate(tasks, 1):
                deadline = task["deadline"] or "No deadline"
                st.write(f"{idx}. {task['name']} [Priority: {task['priority']}] [Deadline: {deadline}] [✗]")
        else:
            st.write("No pending tasks.")

    elif choice == "View Completed Tasks":
        st.header("Completed Tasks")
        tasks = get_sorted_tasks("completed")
        if tasks:
            for idx, task in enumerate(tasks, 1):
                deadline = task["deadline"] or "No deadline"
                st.write(f"{idx}. {task['name']} [Priority: {task['priority']}] [Deadline: {deadline}] [✓]")
        else:
            st.write("No completed tasks.")

    # Add a task
    elif choice == "Add Task":
        st.header("Add a New Task")
        task_name = st.text_input("Task Name")
        priority = st.number_input("Priority (1 = highest)", min_value=1, step=1)
        deadline = st.date_input("Deadline (optional)", value=None)
        if st.button("Add Task"):
            if task_name.strip():
                if deadline and deadline < datetime.today().date():
                    st.error("The deadline cannot be in the past.")
                else:
                    todo_list.append(
                        {
                            "name": task_name.strip(),
                            "priority": int(priority),
                            "deadline": deadline.strftime("%d/%m/%Y") if deadline else None,
                            "completed": False,
                        }
                    )
                    save_data()
                    st.success(f"Task '{task_name}' added.")
            else:
                st.error("Task name cannot be empty.")

    # Mark a task as complete
    elif choice == "Mark Task Complete":
        st.header("Mark a Task as Complete")
        tasks = get_sorted_tasks("pending")  # Sort tasks by priority and deadline
        if tasks:
            task_to_complete = st.selectbox(
                "Select Task",
                [
                    f"{idx + 1}. {task['name']} [Priority: {task['priority']}] [Deadline: {task['deadline'] or 'No deadline'}]"
                    for idx, task in enumerate(tasks)
                ],
            )
            if st.button("Mark Complete"):
                task_index = int(task_to_complete.split(".")[0]) - 1
                selected_task = tasks[task_index]
                for task in todo_list:
                    if task == selected_task:
                        task["completed"] = True
                        break
                save_data()
                st.success(f"Task '{selected_task['name']}' marked as complete.")
        else:
            st.write("No pending tasks to complete.")

    # Remove a task
    elif choice == "Remove Task":
        st.header("Remove a Task")
        tasks = get_sorted_tasks("priority")  # Ensure tasks are sorted by priority and deadline
        if tasks:
            task_to_remove = st.selectbox(
                "Select Task",
                [
                    f"{idx + 1}. {task['name']} [Priority: {task['priority']}] [Deadline: {task['deadline'] or 'No deadline'}]"
                    for idx, task in enumerate(tasks)
                ],
            )
            if st.button("Remove Task"):
                task_index = int(task_to_remove.split(".")[0]) - 1
                selected_task = tasks[task_index]
                todo_list.remove(selected_task)
                save_data()
                st.success(f"Task '{selected_task['name']}' removed.")
        else:
            st.write("No tasks to remove.")

    st.sidebar.write("© To-Do List Manager")

# Run the app
if __name__ == "__main__":
    main()
