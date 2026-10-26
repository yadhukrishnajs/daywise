import os
import sys
import json
from pathlib import Path
from datetime import date, datetime, timedelta
import requests

FILE = Path("tasks.json")


def main():
    while True:
        clear_screen()
        print("""
====================================
              DAYWISE
====================================
1. Today's Dashboard
2. Add a Task
3. View Upcoming Tasks
4. Manage Tasks
5. Exit
====================================
""")
        try:
            choice = int(input("Choose an option: "))
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 5.")
            pause()
            continue
        except (KeyboardInterrupt, EOFError):
            clear_screen()
            print("Goodbye! Stay productive.")
            sys.exit()

        if choice == 1:
            clear_screen()
            todays_dashboard()
            pause()
        elif choice == 2:
            add_task_menu()
        elif choice == 3:
            clear_screen()
            view_upcoming_tasks()
            pause()
        elif choice == 4:
            manage_task_menu()
        elif choice == 5:
            clear_screen()
            print("Goodbye! Stay productive.")
            sys.exit()
        else:
            print("Invalid option. Please choose between 1 and 5.")
            pause()




def clear_screen():
    """Clear the terminal window on Windows, macOS, or Linux."""
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    """Wait for the user to press Enter before clearing the screen."""
    input("\nPress Enter to continue...")


# ==========================================================
# 3 TESTABLE TOP-LEVEL FUNCTIONS FOR test_project.py
# ==========================================================

def get_greeting(hour):
    """Return a time-appropriate greeting based on the hour (0-23)."""
    if not isinstance(hour, int) or hour < 0 or hour > 23:
        raise ValueError("Hour must be an integer between 0 and 23.")
    if hour < 12:
        return "Good morning! ☀️"
    elif hour < 18:
        return "Good afternoon! 🌤"
    else:
        return "Good evening! 🌙"


def parse_future_date(user_date, today=None):
    """
    Validate a DD-MM-YYYY date string and return ISO format (YYYY-MM-DD).
    Raises ValueError if the format is invalid or the date is in the past.
    """
    if today is None:
        today = date.today()

    task_date = datetime.strptime(user_date.strip(), "%d-%m-%Y").date()
    if task_date < today:
        raise ValueError("Error: You cannot select a past date.")
    return task_date.isoformat()


def get_sorted_upcoming_tasks(tasks):
    """Filter for valid future tasks and return them sorted chronologically."""
    future_tasks = [
        task for task in tasks
        if task.get("type") == "future" and task.get("date")
    ]
    return sorted(future_tasks, key=lambda task: task["date"])



def todays_dashboard():
    tasks = load_task()
    today_obj = date.today()
    today_str = today_obj.isoformat()
    tomorrow_str = (today_obj + timedelta(days=1)).isoformat()

    todays_tasks = [
        task for task in tasks
        if task.get("type") == "daily"
        or (task.get("type") == "future" and task.get("date") == today_str)
    ]

    completed_count = sum(1 for task in todays_tasks if task.get("completed", False))
    total_tasks = len(todays_tasks)
    remaining = total_tasks - completed_count
    hour = datetime.now().hour

    # 1. Header with Greeting & Date
    print(f"""
====================================
         TODAY'S DASHBOARD
         {get_greeting(hour)}
     {today_obj.strftime("%A, %B %d, %Y")}
====================================""")

    # 2. Today's Tasks & Progress
    print(f"\n📋 TODAY'S TASKS ({remaining} remaining)")
    print("------------------------------------")

    if not todays_tasks:
        print("No tasks scheduled for today!")
    else:
        for index, task in enumerate(todays_tasks, start=1):
            status = "✓" if task.get("completed", False) else " "
            category = "Daily" if task["type"] == "daily" else "Due Today"
            print(f'{index}. [{status}] {task["description"]} ({category})')

        percentage = round((completed_count / total_tasks) * 100)
        print("------------------------------------")
        print(f"Progress: {completed_count}/{total_tasks} completed ({percentage}%)")

    # 3. Upcoming Tomorrow Section
    tomorrow_tasks = [
        task for task in tasks
        if task.get("type") == "future" and task.get("date") == tomorrow_str
    ]
    print("\n────────────────────────")
    print("📅 UPCOMING (TOMORROW)")
    print("────────────────────────")
    if not tomorrow_tasks:
        print("- Nothing scheduled for tomorrow")
    else:
        for task in tomorrow_tasks:
            print(f'- {task["description"]}')

    # 4. On This Day Section
    events = get_on_this_day()
    print("\n────────────────────────")
    print("📜 ON THIS DAY")
    print("────────────────────────")
    if events:
        print(f"{len(events)} interesting events:")
        for event in events:
            print(f"• {event}")
    else:
        print("Could not load historical events.")

    print("====================================")


def get_on_this_day():
    today = date.today()
    url = (
        "https://api.wikimedia.org/feed/v1/wikipedia/en/onthisday/selected/"
        f"{today.month:02d}/{today.day:02d}"
    )
    headers = {"User-Agent": "DAYWISE/1.0"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()
        events = data.get("selected", [])[:3]
        return [f"{event['year']}: {event['text']}" for event in events]
    except (requests.RequestException, ValueError, KeyError, TypeError):
        return []


def add_task_menu():
    while True:
        clear_screen()
        print("""
====================================
           ADD A TASK
====================================
1. Add a Daily Task
2. Add a task for a future date
3. Back to Main Menu
====================================
""")
        while True:
            try:
                choice = int(input("Choose an option: "))
                if 0 < choice < 4:
                    break
                print("Invalid option. Please try again.")
            except ValueError:
                print("Invalid option. Please choose 1, 2, or 3.")

        if choice == 1:
            clear_screen()
            add_daily_task()
            pause()
        elif choice == 2:
            clear_screen()
            add_future_task()
            pause()
        elif choice == 3:
            return


def add_daily_task():
    print("========== ADD DAILY TASK ==========")
    tasks = load_task()
    task = input("Enter the daily task: ").strip()

    if not task:
        print("Task description cannot be empty.")
        return

    new_task = {
        "description": task,
        "type": "daily",
        "completed": False
    }

    tasks.append(new_task)
    save_task(tasks)
    print("\nDaily task added successfully!")


def add_future_task():
    print("========= ADD FUTURE TASK =========")
    tasks = load_task()
    task = input("Enter the future task: ").strip()

    if not task:
        print("Task description cannot be empty.")
        return

    task_date = valid_date()

    new_task = {
        "description": task,
        "type": "future",
        "date": task_date,
        "completed": False
    }

    tasks.append(new_task)
    save_task(tasks)
    print("\nFuture task added successfully!")


def view_upcoming_tasks():
    tasks = load_task()
    sorted_tasks = get_sorted_upcoming_tasks(tasks)

    print("========== UPCOMING TASKS ==========")
    if not sorted_tasks:
        print("No upcoming tasks scheduled.")
        return

    for i, task in enumerate(sorted_tasks, start=1):
        status = "✓" if task.get("completed", False) else " "
        print(f'{i}. [{status}] {task["date"]} - {task["description"]}')
    print("====================================")


def manage_task_menu():
    while True:
        clear_screen()
        print("""
====================================
            MANAGE TASKS
====================================
1. Mark Task as Complete
2. Edit a Task
3. Delete a Task
4. Back to Main Menu
====================================
""")
        while True:
            try:
                choice = int(input("Choose an option: "))
                if 0 < choice < 5:
                    break
                print("Invalid option. Please try again.")
            except ValueError:
                print("Invalid option. Please choose 1, 2, 3, or 4.")

        if choice == 1:
            clear_screen()
            mark_task_complete()
            pause()
        elif choice == 2:
            clear_screen()
            edit_task()
            pause()
        elif choice == 3:
            clear_screen()
            delete_task()
            pause()
        elif choice == 4:
            return


def show_all_tasks(tasks):
    print("\n------------ YOUR TASKS ------------")
    for i, task in enumerate(tasks, start=1):
        status = "✓" if task.get("completed", False) else " "
        if task["type"] == "daily":
            info = "Daily"
        else:
            info = f"Due: {task['date']}"
        print(f"{i}. [{status}] {task['description']} ({info})")
    print("------------------------------------")


def mark_task_complete():
    tasks = load_task()
    if not tasks:
        print("No task exist")
        return

    show_all_tasks(tasks)

    while True:
        try:
            task_number = int(input("Enter task number to toggle complete: "))
            if 0 < task_number <= len(tasks):
                break
            print("Invalid option. Please try again.")
        except ValueError:
            print("Invalid option. Please choose correct option")

    task_number -= 1
    selected_task = tasks[task_number]
    selected_task["completed"] = not selected_task.get("completed", False)

    tasks[task_number] = selected_task
    save_task(tasks)
    state = "completed" if selected_task["completed"] else "incomplete"
    print(f"\nTask '{selected_task['description']}' marked as {state}!")


def edit_task():
    tasks = load_task()
    if not tasks:
        print("No task exist")
        return

    show_all_tasks(tasks)

    while True:
        try:
            task_number = int(input("Enter task number to edit: "))
            if 0 < task_number <= len(tasks):
                break
            print("Invalid option. Please try again.")
        except ValueError:
            print("Invalid option. Please choose correct option")

    task_number -= 1
    selected_task = tasks[task_number]
    print("\nCurrent description:", selected_task["description"])

    description = input("Enter new description (press Enter to keep current): ").strip()
    if description:
        selected_task["description"] = description

    if selected_task["type"] == "future":
        answer = input(f"Current date is {selected_task['date']}. Change date? (y/n): ")
        if answer.lower() == "y":
            task_date = valid_date()
            selected_task["date"] = task_date

    tasks[task_number] = selected_task
    save_task(tasks)
    print("\nTask updated successfully!")


def delete_task():
    tasks = load_task()
    if not tasks:
        print("No task exist")
        return

    show_all_tasks(tasks)

    while True:
        try:
            task_number = int(input("Enter task number to delete: "))
            if 0 < task_number <= len(tasks):
                break
            print("Invalid option. Please try again.")
        except ValueError:
            print("Invalid option. Please choose correct option")

    task_number -= 1
    selected_task = tasks[task_number]

    answer = input(f"Are you sure you want to delete '{selected_task['description']}'? (y/n): ")
    if answer.lower() == "y":
        tasks.pop(task_number)
        save_task(tasks)
        print(f"\nTask '{selected_task['description']}' deleted successfully!")
    else:
        print("\nDeletion cancelled.")


def load_task():
    if not FILE.exists():
        return []
    try:
        with FILE.open("r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("Error: tasks.json contains invalid JSON.")
        return []


def save_task(tasks):
    with FILE.open("w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4, ensure_ascii=False)


def valid_date():
    while True:
        user_date = input("Enter date (DD-MM-YYYY): ")
        try:
            return parse_future_date(user_date)
        except ValueError as e:
            if "does not match format" in str(e) or "unconverted data" in str(e):
                print("Invalid date. Please use DD-MM-YYYY format.")
            else:
                print(e)


if __name__ == "__main__":
    main()
