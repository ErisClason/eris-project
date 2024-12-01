from pydantic import BaseModel

class User(BaseModel):
    """
    Represents a user in the system.

    Attributes:
        id (int): The unique identifier for the user.
        name (str): The name of the user.
    """
    id: int
    name: str
