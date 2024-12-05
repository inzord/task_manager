from task_manager.repositories.repositories import JsonTaskRepository
from models import TaskPriority
from task_manager.services import TaskService


def main():
    task_repository = JsonTaskRepository('repositories/tasks.json')
    task_service = TaskService(task_repository)

    def view_tasks():
        category = input("Введите категорию для фильтрации (или оставьте пустым для всех): ")
        task_service.view_tasks(category if category else None)

    def add_task():
        title = input("Введите название задачи: ")
        description = input("Введите описание задачи: ")
        category = input("Введите категорию: ")
        due_date = input("Введите срок выполнения (YYYY-MM-DD): ")
        priority = input("Введите приоритет (Низкий, Средний, Высокий): ")
        try:
            priority_enum = TaskPriority[priority.upper()]
            task_service.add_task(title, description, category, due_date, priority_enum)
            print("Задача добавлена")
        except KeyError:
            print("Некорректный приоритет.")

    def complete_task():
        print("Существующие задачи:")
        task_service.view_tasks()
        try:
            task_id = int(input("Введите идентификатор задачи для изменения: "))
            task_service.complete_task(task_id)
        except ValueError:
            print("Пожалуйста, введите корректный идентификатор задачи.")

    def delete_task():
        task_id = input("Введите идентификатор задачи для удаления (или оставьте пустым для удаления по категории): ")
        if task_id:
            task_service.delete_task(int(task_id))
        else:
            category = input("Введите категорию для удаления: ")
            task_service.delete_task(category=category)

    def search_tasks():
        keyword = input("Введите ключевые слова для поиска: ")
        found_tasks = task_service.search_tasks(keyword)
        if found_tasks:
            for task in found_tasks:
                print(
                    f"{task.id}: {task.title} - {task.status.value} (Срок: {task.due_date},"
                    f" Приоритет: {task.priority.value})")
        else:
            print("Задачи не найдены.")

    def exit_program():
        print("Выход из программы.")
        return True

    # Словарь команд
    commands = {
        '1': view_tasks,
        '2': add_task,
        '3': complete_task,
        '4': delete_task,
        '5': search_tasks,
        '6': exit_program
    }

    while True:
        print("\n1. Просмотр задач")
        print("2. Добавление задачи")
        print("3. Изменение задачи")
        print("4. Удаление задачи")
        print("5. Поиск задач")
        print("6. Выход")

        choice = input("Выберите опцию: ")

        # Выполнение команды, если она существует
        if choice in commands:
            if commands[choice]() is True:  # Если функция возвращает True, выходим из цикла
                break
        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")


if __name__ == '__main__':
    main()
