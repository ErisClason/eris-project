from typing import Optional, Callable

class Workflow:
    def __init__(self, name: str):
        self.name = name
        self.states = set()
        self.transitions = {}

    def add_state(self, state: str):
        self.states.add(state)

    def add_transition(self, from_state: str, to_state: str, condition: Optional[Callable] = None):
        if from_state not in self.states or to_state not in self.states:
            raise ValueError("Both states must exist in the workflow.")
        if from_state not in self.transitions:
            self.transitions[from_state] = {}
        self.transitions[from_state][to_state] = condition

    def can_transition(self, from_state: str, to_state: str) -> bool:
        if from_state in self.transitions and to_state in self.transitions[from_state]:
            condition = self.transitions[from_state][to_state]
            if condition is None or condition():  # Check the condition if it exists
                return True
        return False
