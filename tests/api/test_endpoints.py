from fastapi.testclient import TestClient
from api.endpoints import app

client = TestClient(app)


def test_create_workflow():
    response = client.post("/workflows", json={"name": "TestWorkflow", "states": ["Pending", "Completed"]})
    assert response.status_code == 201
    assert response.json()["message"] == "Workflow created successfully"
    assert response.json()["id"] == 1


def test_list_workflows():
    client.post("/workflows", json={"name": "TestWorkflow", "states": ["Pending", "Completed"]})
    response = client.get("/workflows")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]["name"] == "TestWorkflow"


def test_get_workflow():
    client.post("/workflows", json={"name": "TestWorkflow", "states": ["Pending", "Completed"]})
    response = client.get("/workflows/1")
    assert response.status_code == 200
    assert response.json()["name"] == "TestWorkflow"
    assert "Pending" in response.json()["states"]


def test_create_task():
    client.post("/workflows", json={"name": "TestWorkflow", "states": ["Pending", "Completed"]})
    response = client.post("/tasks", json={"name": "TestTask", "workflow_id": 1, "initial_state": "Pending"})
    assert response.status_code == 201
    assert response.json()["name"] == "TestTask"
    assert response.json()["current_state"] == "Pending"


def test_list_tasks():
    client.post("/workflows", json={"name": "TestWorkflow", "states": ["Pending", "Completed"]})
    client.post("/tasks", json={"name": "TestTask", "workflow_id": 1, "initial_state": "Pending"})
    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]["name"] == "TestTask"


def test_task_transition():
    client.post("/workflows", json={"name": "TestWorkflow", "states": ["Pending", "Completed"]})
    client.post("/tasks", json={"name": "TestTask", "workflow_id": 1, "initial_state": "Pending"})

    response = client.patch("/tasks/1/transition", json={"next_state": "Completed"})
    assert response.status_code == 200
    assert response.json()["current_state"] == "Completed"
