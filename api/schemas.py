from pydantic import BaseModel

class TaskCreateRequest(BaseModel):
    name: str
    workflow_id: int
    initial_state: str

class TransitionRequest(BaseModel):
    next_state: str
