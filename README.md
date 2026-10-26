# DAYWISE — Personal Task Management System
#### Video Demo: https://youtu.be/aHjdT_teoEg
#### Description:

**Daywise** is a menu-driven command-line task management application built in Python for the CS50P Final Project. People generally manage two distinct categories of responsibilities: recurring daily habits (such as studying Python, reading, or exercising) and date-specific future commitments (such as submitting an assignment or attending an appointment). Many simple to-do lists treat all tasks the same, cluttering daily routines with distant deadlines or forcing users to re-enter daily habits. Daywise solves this problem by unifying daily routines and scheduled future responsibilities into one organized, persistent interface.

### Core Features

1. **Today's Dashboard:** Acts as a personalized daily briefing screen. It greets the user dynamically based on the current hour of the day (`Good morning!`, `Good afternoon!`, or `Good evening!`), displays the formatted current date, and filters the task database to show all recurring daily tasks alongside any future tasks due today. It also calculates real-time completion progress as both a fraction and a percentage, previews tasks scheduled for tomorrow, and integrates with the Wikimedia "On This Day" REST API to display three historical events that occurred on the current calendar date.
2. **Add a Task:** Allows users to create either a repeating daily task or a date-specific future task. Future tasks are validated using Python's `datetime` module to ensure they follow the `DD-MM-YYYY` input format, represent real calendar dates, and are not scheduled in the past before converting them into ISO 8601 format (`YYYY-MM-DD`) for reliable chronological sorting.
3. **View Upcoming Tasks:** Filters the task list for scheduled future tasks and sorts them chronologically using a `lambda` key function so the user can see upcoming deadlines in order.
4. **Manage Tasks:** Provides an interactive submenu loop where users can toggle any task's completion status (`[✓]` or `[ ]`), edit a task's description or reschedule its due date, or permanently delete tasks with a confirmation prompt.

### Project File Structure

- `project.py`: Contains the main entry point (`main()`) and all core application logic, menu controllers, JSON file operations, API integration, and helper functions (`get_greeting()`, `parse_future_date()`, and `get_sorted_upcoming_tasks()`).
- `test_project.py`: Contains unit tests written for `pytest` that verify `get_greeting()`, `parse_future_date()`, and `get_sorted_upcoming_tasks()`, including edge cases and expected `ValueError` exceptions.
- `tasks.json`: Automatically generated JSON storage file that persists the user's list of task dictionaries across sessions using UTF-8 encoding.
- `requirements.txt`: Lists the external `pip`-installable dependencies (`requests` and `pytest`) required to run and test the project.

### Design Choices

During development, several important design decisions were made:

- **JSON vs. CSV/SQLite Storage:** I chose JSON over CSV because each task has varied attributes (for example, `"daily"` tasks do not require a `"date"` key, whereas `"future"` tasks do). JSON maps directly to Python lists and dictionaries, making serialization with `json.load()` and `json.dump()` clean and readable.
- **ISO 8601 Date Storage (`YYYY-MM-DD`) vs. User Input Format (`DD-MM-YYYY`):** While users in many regions prefer typing dates as `DD-MM-YYYY`, sorting strings in `DD-MM-YYYY` format does not sort chronologically. By validating user input in `DD-MM-YYYY` and storing the result via `.isoformat()` (`YYYY-MM-DD`), Python can sort tasks chronologically with standard string comparison.
- **Decoupling Validation Logic from `input()`:** Initially, date validation and user prompts were combined inside a single `while True` loop. To support unit testing, I separated date processing (`parse_future_date()` and `get_sorted_upcoming_tasks()`) from interactive CLI prompts (`valid_date()`), making the core logic testable with `pytest`.
