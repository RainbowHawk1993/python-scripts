import argparse
import logging
import datetime
from tinydb import TinyDB, Query

logging.basicConfig(filename='task_manager.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class TaskManager:
    def __init__(self, db_name='tasks.json'):
        self.db = TinyDB(db_name)
        self.Task = Query()

    def add_task(self, title, description, due_date, status='pending'):
        try:
            due_date = datetime.datetime.strptime(due_date, '%Y-%m-%d').date()
            self.db.insert({'title': title, 'description': description, 'due_date': str(due_date), 'status': status})
            logging.info(f"Task '{title}' added successfully.")
            return True
        except ValueError:
            logging.error("Invalid date format. Please use YYYY-MM-DD.")
            return False
        except Exception as e:
            logging.error(f"Error adding task: {e}")
            return False


    def update_status(self, title, status):
       try:
            self.db.update({'status': status}, self.Task.title == title)
            logging.info(f"Status of task '{title}' updated to '{status}'.")
            return True
       except Exception as e:
            logging.error(f"Error updating task status: {e}")
            return False

    def delete_task(self, title):
       try:
            self.db.remove(self.Task.title == title)
            logging.info(f"Task '{title}' deleted successfully.")
            return True
       except Exception as e:
            logging.error(f"Error deleting task: {e}")
            return False

    def list_tasks(self):
        try:
            tasks = self.db.all()
            sorted_tasks = sorted(tasks, key=lambda k: k['due_date'])
            for task in sorted_tasks:
                print(f"Title: {task['title']}")
                print(f"Description: {task['description']}")
                print(f"Due Date: {task['due_date']}")
                print(f"Status: {task['status']}")
                print("-" * 20)
            logging.info("Tasks listed successfully.")
            return True
        except Exception as e:
            logging.error(f"Error listing tasks: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(description="Simple Task Manager")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Task title")
    add_parser.add_argument("description", help="Task description")
    add_parser.add_argument("due_date", help="Due date (YYYY-MM-DD)")

    update_parser = subparsers.add_parser("update", help="Update task status")
    update_parser.add_argument("title", help="Task title")
    update_parser.add_argument("status", help="New status (pending, in_progress, completed)")

    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("title", help="Task title")

    list_parser = subparsers.add_parser("list", help="List all tasks")

    args = parser.parse_args()
    task_manager = TaskManager()

    if args.command == "add":
        task_manager.add_task(args.title, args.description, args.due_date)
    elif args.command == "update":
        task_manager.update_status(args.title, args.status)
    elif args.command == "delete":
        task_manager.delete_task(args.title)
    elif args.command == "list":
        task_manager.list_tasks()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
