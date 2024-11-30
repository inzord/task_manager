import json
import os

import pytest

from task_manager import TaskManager, TaskStatus, TaskPriority

TEST_FILE = 'test_tasks.json'


@pytest.fixture(scope='module', autouse=True)
def setup_module():
    # Создаем тестовый файл перед запуском тестов
    with open(TEST_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f)  # Инициализируем пустой список задач
    yield

    # Удаляем тестовый файл после завершения тестов
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)


@pytest.fixture
def task_manager():
    # Каждый тест получает новый экземпляр TaskManager
    return TaskManager(TEST_FILE)


def test_load_from_empty_file():
    empty_manager = TaskManager(TEST_FILE)
    assert len(empty_manager.tasks) == 0  # Ожидаем, что задачи не загружены


def test_load_tasks(task_manager):
    task_manager.add_task("Задача 1", "Описание 1", "Общие", "2023-12-31", TaskPriority.MEDIUM)
    task_manager.add_task("Задача 2", "Описание 2", "Общие", "2023-12-31", TaskPriority.LOW)

    # Создаем новый экземпляр TaskManager для загрузки задач
    new_manager = TaskManager(TEST_FILE)
    assert len(new_manager.tasks) == 2
    assert new_manager.tasks[0].title == "Задача 1"
    assert new_manager.tasks[1].title == "Задача 2"


def test_add_task(task_manager):
    task_manager.add_task("Тестовая задача", "Описание задачи", "Общие", "2023-12-31", TaskPriority.HIGH)
    assert len(task_manager.tasks) == 3
    assert task_manager.tasks[2].title == "Тестовая задача"


def test_delete_task(task_manager):
    task_manager.add_task("Задача для удаления", "Описание", "Общие", "2023-12-31", TaskPriority.LOW)
    task_manager.delete_task(4)
    assert len(task_manager.tasks) == 3  # Проверяем, что список задач пуст


def test_complete_task(task_manager):
    task_manager.add_task("Задача для проверки измениея статуса на Выполена", "Описание", "Общие", "2023-12-31",
                          TaskPriority.LOW)
    task_manager.complete_task(4)
    assert task_manager.tasks[3].status == TaskStatus.COMPLETED


def test_search_tasks(task_manager):
    task_manager.add_task("Задача поиска", "Описание поиска", "Общие", "2023-12-31", TaskPriority.LOW)
    found_tasks = task_manager.search_tasks("поиск")
    assert len(found_tasks) == 1
    assert found_tasks[0].title == "Задача поиска"


def test_get_priority_invalid():
    with pytest.raises(ValueError, match="Некорректный приоритет."):
        TaskManager.get_priority("Неверный приоритет")


def test_get_status_invalid():
    with pytest.raises(ValueError, match="Некорректный статус: неверный статус"):
        TaskManager.get_status("неверный статус")


def test_delete_nonexistent_task(task_manager):
    task_manager.add_task("Задача 1", "Описание 1", "Общие", "2023-12-31", TaskPriority.LOW)
    initial_length = len(task_manager.tasks)
    task_manager.delete_task(999)  # Попытка удалить несуществующую задачу
    assert len(task_manager.tasks) == initial_length


def test_change_task_status(task_manager):
    task_manager.add_task("Задача для статуса", "Описание", "Общие", "2023-12-31", TaskPriority.LOW)
    task_manager.complete_task(1)  # Завершаем задачу
    assert task_manager.tasks[0].status == TaskStatus.COMPLETED  # Проверяем статус


def test_search_by_title(task_manager):
    task_manager.add_task("Уникальная задача", "Описание", "Общие", "2023-12-31", TaskPriority.LOW)
    task_manager.add_task("Другая задача", "Описание", "Общие", "2023-12-31", TaskPriority.LOW)
    found_tasks = task_manager.search_tasks("Уникальная")
    assert len(found_tasks) == 1
    assert found_tasks[0].title == "Уникальная задача"


def test_save_tasks_to_file(task_manager):
    task_manager.add_task("Задача для сохранения", "Описание", "Общие", "2023-12-31", TaskPriority.LOW)
    task_manager.save_tasks()
    with open(TEST_FILE, 'r', encoding='utf-8') as f:
        tasks = json.load(f)
    assert len(tasks) == 10
    assert tasks[9]['title'] == "Задача для сохранения"
