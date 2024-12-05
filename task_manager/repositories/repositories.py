import json
from abc import ABC, abstractmethod
from typing import List
from task_manager.models import Task, get_priority, get_status


class TaskRepository(ABC):
    @abstractmethod
    def load_tasks(self) -> List[Task]:
        pass

    @abstractmethod
    def save_tasks(self, tasks: List[Task]) -> None:
        pass


class JsonTaskRepository(TaskRepository):
    def __init__(self, file_name: str):
        self.file_name = file_name

    def load_tasks(self) -> List[Task]:
        try:
            with open(self.file_name, 'r', encoding='utf-8') as file:
                task_data = json.load(file)
                return [Task(
                    id=task_dict['id'],
                    title=task_dict['title'],
                    description=task_dict['description'],
                    category=task_dict['category'],
                    due_date=task_dict['due_date'],
                    priority=get_priority(task_dict['priority'].upper()),
                    status=get_status(task_dict['status'].upper())
                ) for task_dict in task_data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_tasks(self, tasks: List[Task]) -> None:
        with open(self.file_name, 'w', encoding='utf-8') as file:
            json.dump([task.to_dict() for task in tasks], file, ensure_ascii=False, indent=4)
