import pytest
from core.tasks import Task
from core.workflows import Workflow

def test_add_task_to_workflow():
    workflow = Workflow("TestWorkflow")
    workflow.add_state("Pending")
    workflow.add_state("InProgress")
    workflow.add_state("Completed")

    task = Task("SampleTask", "Pending")
    workflow.add_task(task)

    assert task in workflow.tasks
    assert task.workflow == workflow

def test_valid_task_transition():
    workflow = Workflow("TestWorkflow")
    workflow.add_state("Pending")
    workflow.add_state("InProgress")
    workflow.add_transition("Pending", "InProgress")

    task = Task(id=1, name="SampleTask", workflow_id=1, current_state="Pending")
    
    assert workflow.can_transition(task.current_state, "InProgress")
    task.set_state("InProgress")
    assert task.current_state == "InProgress"

def test_invalid_task_transition():
    workflow = Workflow("TestWorkflow")
    workflow.add_state("Pending")
    workflow.add_state("Completed")

    task = Task("SampleTask", "Pending")
    workflow.add_task(task)

    with pytest.raises(ValueError):
        task.set_state("Completed")
