from typing import Optional

class Task:
    def __init__(self, id: int, name: str, workflow_id: int, current_state: str):
        self.id = id
        self.name = name
        self.workflow_id = workflow_id
        self.current_state = current_state

    def set_state(self, to_state: str):
        self.current_state = to_state

    def __repr__(self):
        return f"<Task(id={self.id}, name={self.name}, state={self.current_state})>"
