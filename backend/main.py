from fastapi import FastAPI
from backend.api.v1.api import api_router  # Import the API router

# Create the FastAPI app instance
app = FastAPI(
    title="Eris Project",
    description="An API for managing users and tasks",
    version="1.0.0",
)

# Include the versioned API router
app.include_router(api_router, prefix="/api/v1")

# Define the root endpoint
@app.get("/")
def read_root():
    """
    Root endpoint for health checks or welcome messages.
    """
    return {"message": "Hello, Eris!"}
