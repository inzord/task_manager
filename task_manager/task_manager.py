import json
from typing import List, Dict, Optional
from enum import Enum


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


class TaskManager:
    def __init__(self, file_name: str):
        self.file_name = file_name
        self.tasks = self.load_tasks()
        self.task_dict = {task.id: task for task in self.tasks}  # Используем словарь для быстрого доступа

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
                    priority=self.get_priority(task_dict['priority']),
                    status=self.get_status(task_dict['status'])
                ) for task_dict in task_data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_tasks(self):
        with open(self.file_name, 'w', encoding='utf-8') as file:
            json.dump([task.to_dict() for task in self.tasks], file, ensure_ascii=False, indent=4)

    def add_task(self, title: str, description: str, category: str, due_date: str, priority: TaskPriority) -> None:
        task_id = max(self.task_dict.keys(), default=0) + 1
        new_task = Task(task_id, title, description, category, due_date, priority)
        self.tasks.append(new_task)
        self.task_dict[task_id] = new_task  # Обновляем словарь
        self.save_tasks()

    def complete_task(self, task_id: int) -> None:
        task = self.task_dict.get(task_id)
        if task:
            task.status = TaskStatus.COMPLETED
            self.save_tasks()
            print("Задача успешно изменена.")
        else:
            print("Задача не найдена.")

    def delete_task(self, task_id: Optional[int] = None, category: Optional[str] = None) -> None:
        if task_id is not None:
            if task_id in self.task_dict:
                del self.task_dict[task_id]
                self.tasks = [task for task in self.tasks if task.id != task_id]
                self.save_tasks()
            else:
                print("Задача не найдена.")
        elif category is not None:
            self.tasks = [task for task in self.tasks if task.category != category]
            self.task_dict = {task.id: task for task in self.tasks}  # Обновляем словарь
            self.save_tasks()
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

    @staticmethod
    def get_priority(priority_str: str) -> TaskPriority:
        priority_str = priority_str.strip().lower()
        if priority_str == "низкий":
            return TaskPriority.LOW
        elif priority_str == "средний":
            return TaskPriority.MEDIUM
        elif priority_str == "высокий":
            return TaskPriority.HIGH
        else:
            raise ValueError("Некорректный приоритет.")

    @staticmethod
    def get_status(status_str: str) -> TaskStatus:
        status_str = status_str.strip().lower()
        if status_str == "не выполнена":
            return TaskStatus.NOT_COMPLETED
        elif status_str == "выполнена":
            return TaskStatus.COMPLETED
        else:
            raise ValueError(f"Некорректный статус: {status_str}")


def main():
    task_manager = TaskManager('tasks.json')

    while True:
        print("\n1. Просмотр задач")
        print("2. Добавление задачи")
        print("3. Изменение задачи")
        print("4. Удаление задачи")
        print("5. Поиск задач")
        print("6. Выход")

        choice = input("Выберите опцию: ")

        if choice == '1':
            category = input("Введите категорию для фильтрации (или оставьте пустым для всех): ")
            task_manager.view_tasks(category if category else None)

        elif choice == '2':
            title = input("Введите название задачи: ")
            description = input("Введите описание задачи: ")
            category = input("Введите категорию: ")
            due_date = input("Введите срок выполнения (YYYY-MM-DD): ")
            priority = input("Введите приоритет (Низкий, Средний, Высокий): ")
            try:
                priority_enum = task_manager.get_priority(priority)  # Используем метод для получения приоритета
                task_manager.add_task(title, description, category, due_date, priority_enum)
                print("Задача добавлена")
            except ValueError as e:
                print(e)

        elif choice == '3':
            print("Существующие задачи:")
            task_manager.view_tasks()  # Выводим все задачи
            try:
                task_id = int(input("Введите идентификатор задачи для изменения: "))
                task_manager.complete_task(task_id)
            except ValueError:
                print("Пожалуйста, введите корректный идентификатор задачи.")

        elif choice == '4':
            task_id = input(
                "Введите идентификатор задачи для удаления (или оставьте пустым для удаления по категории): ")
            if task_id:
                task_manager.delete_task(int(task_id))
            else:
                category = input("Введите категорию для удаления: ")
                task_manager.delete_task(category=category)

        elif choice == '5':
            keyword = input("Введите ключевые слова для поиска: ")
            found_tasks = task_manager.search_tasks(keyword)
            if found_tasks:
                for task in found_tasks:
                    print(
                        f"{task.id}: {task.title} - {task.status.value} (Срок: {task.due_date}, Приоритет: {task.priority.value})")
            else:
                print("Задачи не найдены.")

        elif choice == '6':
            break

        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")


if __name__ == '__main__':
    main()
