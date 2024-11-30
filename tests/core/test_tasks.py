import pytest
from datetime import datetime, timedelta
from core.tasks import Task


def test_task_creation():
    """
    Test task creation with name and optional due date.
    """
    task = Task("Test Task")
    assert task.name == "Test Task"
    assert task.status == "Pending"
    assert task.assigned_to is None
    assert task.due_date is None

    due_date = datetime.now() + timedelta(days=1)
    task_with_due_date = Task("Task with Due Date", due_date)
    assert task_with_due_date.due_date == due_date


def test_task_assignment():
    """
    Test assigning a task to a user.
    """
    task = Task("Test Task")
    task.assign_to("Alice")
    assert task.assigned_to == "Alice"


def test_status_update():
    """
    Test updating the status of a task with valid inputs.
    """
    task = Task("Test Task")
    task.update_status("In Progress")
    assert task.status == "In Progress"

    task.update_status("Completed")
    assert task.status == "Completed"


def test_invalid_status_update():
    """
    Test updating the status of a task with invalid inputs.
    """
    task = Task("Test Task")
    with pytest.raises(ValueError):
        task.update_status("Invalid Status")


def test_task_overdue():
    """
    Test checking if a task is overdue.
    """
    due_date = datetime.now() - timedelta(days=1)
    task = Task("Overdue Task", due_date)
    assert task.is_overdue() is True

    future_date = datetime.now() + timedelta(days=1)
    not_overdue_task = Task("Not Overdue Task", future_date)
    assert not_overdue_task.is_overdue() is False
