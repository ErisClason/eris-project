from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel
from typing import List, Optional, Dict
from core.workflows import Workflow
from core.tasks import Task

app = FastAPI()

# Temporary in-memory storage
workflows: Dict[int, Workflow] = {}
tasks: Dict[int, Task] = {}
workflow_id_counter = 1
task_id_counter = 1


# Pydantic models for validation
class WorkflowCreateRequest(BaseModel):
    name: str
    states: List[str]


class WorkflowResponse(BaseModel):
    id: int
    name: str
    states: List[str]


class TaskCreateRequest(BaseModel):
    name: str
    workflow_id: int
    initial_state: str


class TaskResponse(BaseModel):
    id: int
    name: str
    workflow_id: int
    current_state: str


class TransitionRequest(BaseModel):
    next_state: str


@app.post("/workflows", status_code=201)
def create_workflow(workflow: WorkflowCreateRequest):
    global workflow_id_counter
    if any(wf.name == workflow.name for wf in workflows.values()):
        raise HTTPException(status_code=400, detail="Workflow already exists.")
    new_workflow = Workflow(name=workflow.name)
    for state in workflow.states:
        new_workflow.add_state(state)
    for from_state in workflow.states:
        for to_state in workflow.states:
            if from_state != to_state:
                new_workflow.add_transition(from_state, to_state)
    workflows[workflow_id_counter] = new_workflow
    workflow_id_counter += 1
    return {"message": "Workflow created successfully", "id": workflow_id_counter - 1}



@app.get("/workflows", response_model=List[WorkflowResponse])
def list_workflows():
    return [
        WorkflowResponse(id=wf_id, name=wf.name, states=list(wf.states))
        for wf_id, wf in workflows.items()
    ]


@app.get("/workflows/{workflow_id}", response_model=WorkflowResponse)
def get_workflow(workflow_id: int = Path(..., description="ID of the workflow")):
    workflow = workflows.get(workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found.")
    return WorkflowResponse(
        id=workflow_id,
        name=workflow.name,
        states=list(workflow.states)
    )


@app.post("/tasks", status_code=201, response_model=TaskResponse)
def create_task(task_request: TaskCreateRequest):
    global task_id_counter
    workflow = workflows.get(task_request.workflow_id)
    if not workflow:
        raise HTTPException(status_code=400, detail="Workflow not found.")
    if task_request.initial_state not in workflow.states:
        raise HTTPException(status_code=400, detail="Invalid initial state for the workflow.")
    
    new_task = Task(
        id=task_id_counter,
        name=task_request.name,
        workflow_id=task_request.workflow_id,
        current_state=task_request.initial_state
    )
    tasks[task_id_counter] = new_task
    response = TaskResponse(
        id=task_id_counter,
        name=new_task.name,
        workflow_id=new_task.workflow_id,
        current_state=new_task.current_state
    )
    task_id_counter += 1
    return response


@app.get("/tasks", response_model=List[TaskResponse])
def list_tasks():
    return [
        TaskResponse(
            id=task.id,
            name=task.name,
            workflow_id=task.workflow_id,
            current_state=task.current_state
        )
        for task in tasks.values()
    ]


@app.patch("/tasks/{task_id}/transition", response_model=TaskResponse)
def transition_task(task_id: int, transition_request: TransitionRequest):
    task = tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found.")
    
    workflow = workflows.get(task.workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found.")
    
    if not workflow.can_transition(task.current_state, transition_request.next_state):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid state transition from {task.current_state} to {transition_request.next_state}."
        )
    
    task.current_state = transition_request.next_state
    return TaskResponse(
        id=task.id,
        name=task.name,
        workflow_id=task.workflow_id,
        current_state=task.current_state
    )
