import json
import uuid
import datetime

import data


class Task:
    def __init__(self,description,status="todo"):
        self.id = str(uuid.uuid4())
        self.description = description
        self.status = status
        self.created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    def updateTask(self,description=None,status=None):
        if description:
            self.description = description
        if status:
            self.status = status
        self.updated_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    def dic(self):
        return {
            "id":self.id,
            "description":self.description,
            "status":self.status,
            "created_at":self.created_at,
            "updated_at":self.updated_at
        }
    @staticmethod
    def get_dic(data):
        task=Task(data["description"],data["status"])
        task.id=data['id']
        task.created_at=data['created_at']
        task.updated_at=data['updated_at']
        return task
class manage:
    def __init__(self,file_name="tasks.json"):
        self.tasks=[]
        self.file_name = file_name
        self.load_tasks()

    def load_tasks(self):
        try:
            with open(self.file_name, 'r') as f:
                # Check if the file is empty
                file_content = f.read().strip()
                if not file_content:
                    self.tasks = []
                    return

                task_data = json.loads(file_content)
                self.tasks = [Task.get_dic(task) for task in task_data]
        except (FileNotFoundError, json.JSONDecodeError):
            # Handle cases where the file does not exist or contains invalid JSON
            self.tasks = []

    def add_task(self,task):
        self.tasks.append(task)
        with open(self.file_name,"w") as file:
            json.dump([task.dic() for task in self.tasks], file, indent=4)
    def delete_task(self,task_id):
        self.tasks.remove(task_id)
        with open(self.file_name,"w") as file:
            json.dump([task.dic() for task in self.tasks], file, indent=4)

    def update_task(self,task_id,**kwargs):
        for task in self.tasks:
            if task.id == task_id:
                task.updateTask(**kwargs)
                break
        with open(self.file_name,"w") as file:
            json.dump([task.dic() for task in self.tasks], file, indent=4)


    def list_tasks(self,status=None):
        if status:
            return [task for task in self.tasks if task.status==status]
        return self.tasks

import sys

def print_menu():
    print("Task Tracker")
    print("1. Add Task")
    print("2. View All Tasks")
    print("3. View Completed Tasks")
    print("4. View Tasks In Progress")
    print("5. View Pending Tasks (Not Done)")
    print("6. Update Task")
    print("7. Delete Task")
    print("8. Exit")

def get_task_details():
    description = input("Description: ")
    return description

def main():
    manager = manage()

    while True:
        print_menu()
        choice = input("Choose an option: ")

        if choice == '1':
            description = get_task_details()
            task = Task(description)
            manager.add_task(task)
            print("Task added successfully.")

        elif choice == '2':
            tasks = manager.list_tasks()
            print("All Tasks:")
            for task in tasks:
                print(f"[{task.status}] ID: {task.id}, Description: {task.description}, Created At: {task.created_at}")

        elif choice == '3':
            tasks = manager.list_tasks(status="done")
            print("Completed Tasks:")
            for task in tasks:
                print(f"ID: {task.id}, Description: {task.description}, Completed At: {task.updated_at}")

        elif choice == '4':
            tasks = manager.list_tasks(status="in-progress")
            print("Tasks In Progress:")
            for task in tasks:
                print(f"ID: {task.id}, Description: {task.description}, Last Updated: {task.updated_at}")

        elif choice == '5':
            tasks = [task for task in manager.list_tasks() if task.status != "done"]
            print("Pending Tasks (Not Done):")
            for task in tasks:
                print(f"[{task.status}] ID: {task.id}, Description: {task.description}, Created At: {task.created_at}")

        elif choice == '6':
            task_id = input("Enter the task ID to update: ")
            description = input("New Description (Leave blank to keep current): ")
            status = input("New Status (todo, in-progress, done): ")
            manager.update_task(task_id, description=description, status=status)
            print("Task updated.")

        elif choice == '7':
            task_id = input("Enter the task ID to delete: ")
            manager.delete_task(task_id)
            print("Task deleted.")

        elif choice == '8':
            print("Exiting Task Tracker.")
            sys.exit()

        else:
            print("Invalid choice, please try again.")

if __name__ == '__main__':
    main()


