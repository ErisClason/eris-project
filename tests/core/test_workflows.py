import pytest
from core.workflows import Workflow

def test_workflow_creation():
    workflow = Workflow("TestWorkflow")
    assert workflow.name == "TestWorkflow"
    assert len(workflow.states) == 0

def test_workflow_transitions():
    workflow = Workflow("TestWorkflow")
    workflow.add_state("Pending")
    workflow.add_state("Completed")
    workflow.add_transition("Pending", "Completed")
    assert workflow.can_transition("Pending", "Completed") is True
    assert workflow.can_transition("Completed", "Pending") is False

def test_add_state():
    workflow = Workflow("TestWorkflow")
    workflow.add_state("Pending")
    workflow.add_state("Completed")
    assert "Pending" in workflow.states
    assert "Completed" in workflow.states

def test_add_transition():
    workflow = Workflow("TestWorkflow")
    workflow.add_state("Pending")
    workflow.add_state("Completed")
    workflow.add_transition("Pending", "Completed")
    assert workflow.can_transition("Pending", "Completed") is True

def test_invalid_transition():
    workflow = Workflow("TestWorkflow")
    workflow.add_state("Pending")
    workflow.add_state("Completed")
    with pytest.raises(ValueError):
        workflow.add_transition("Pending", "NonExistent")

def test_transition_with_condition():
    workflow = Workflow("TestWorkflow")
    workflow.add_state("Pending")
    workflow.add_state("Completed")
    workflow.add_transition("Pending", "Completed", lambda: False)
    assert workflow.can_transition("Pending", "Completed") is False
