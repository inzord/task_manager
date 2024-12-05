from typing import List, Optional

from task_manager.models import Task, TaskStatus, TaskPriority
from task_manager.repositories.repositories import JsonTaskRepository


class TaskService:
    def __init__(self, repositories: JsonTaskRepository):
        self.repositories = repositories
        self.tasks = self.repositories.load_tasks()
        self.task_dict = {task.id: task for task in self.tasks}  # Используем словарь для быстрого доступа

    def add_task(self, title: str, description: str, category: str, due_date: str, priority: TaskPriority) -> None:
        task_id = max(self.task_dict.keys(), default=0) + 1
        new_task = Task(task_id, title, description, category, due_date, priority)
        self.tasks.append(new_task)
        self.task_dict[task_id] = new_task  # Обновляем словарь
        self.repositories.save_tasks(self.tasks)

    def complete_task(self, task_id: int) -> None:
        task = self.task_dict.get(task_id)
        if task:
            task.status = TaskStatus.COMPLETED
            self.repositories.save_tasks(self.tasks)
            print("Задача успешно изменена.")
        else:
            print("Задача не найдена.")

    def delete_task(self, task_id: Optional[int] = None, category: Optional[str] = None) -> None:
        if task_id is not None:
            if task_id in self.task_dict:
                del self.task_dict[task_id]
                self.tasks = [task for task in self.tasks if task.id != task_id]
                self.repositories.save_tasks(self.tasks)
            else:
                print("Задача не найдена.")
        elif category is not None:
            self.tasks = [task for task in self.tasks if task.category != category]
            self.task_dict = {task.id: task for task in self.tasks}  # Обновляем словарь
            self.repositories.save_tasks(self.tasks)
        else:
            print("Не указаны идентификатор или категория для удаления.")

    def search_tasks(self, keyword: str) -> List[Task]:
        return [task for task in self.tasks if
                keyword.lower() in task.title.lower() or keyword.lower() in task.description.lower()]

    def view_tasks(self, category: Optional[str] = None) -> None:
        tasks_to_view = self.tasks if category is None else [task for task in self.tasks if task.category == category]
        for task in tasks_to_view:
            print(
                f"{task.id}: {task.title} - {task.status.value} (Срок: {task.due_date}, Приоритет: {task.priority.value})")
