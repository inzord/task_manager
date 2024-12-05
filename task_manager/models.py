from enum import Enum
from typing import Dict


class TaskStatus(Enum):
    NOT_COMPLETED = "Не выполнена"
    COMPLETED = "Выполнена"


class TaskPriority(Enum):
    LOW = "Низкий"
    MEDIUM = "Средний"
    HIGH = "Высокий"


class Task:
    def __init__(self, id: int, title: str, description: str, category: str, due_date: str, priority: TaskPriority,
                 status: TaskStatus = TaskStatus.NOT_COMPLETED):
        self.id = id
        self.title = title
        self.description = description
        self.category = category
        self.due_date = due_date
        self.priority = priority
        self.status = status

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "due_date": self.due_date,
            "priority": self.priority.value,
            "status": self.status.value
        }


def get_priority(priority_str: str) -> TaskPriority:
    priority_str = priority_str.strip().lower()
    if priority_str == "низкий":
        return TaskPriority.LOW
    elif priority_str == "средний":
        return TaskPriority.MEDIUM
    elif priority_str == "высокий":
        return TaskPriority.HIGH
    else:
        raise ValueError(f"Некорректный приоритет: {priority_str}")


def get_status(status_str: str) -> TaskStatus:
    status_str = status_str.strip().lower()
    if status_str == "не выполнена":
        return TaskStatus.NOT_COMPLETED
    elif status_str == "выполнена":
        return TaskStatus.COMPLETED
    else:
        raise ValueError(f"Некорректный статус: {status_str}")
