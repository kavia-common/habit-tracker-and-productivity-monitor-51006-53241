from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine

from .auth import router as auth_router
from .habits import router as habits_router
from .analytics import router as analytics_router

app = FastAPI(
    title="Habit Tracker API",
    description="Backend for a mobile habit tracker & productivity app. Provides authentication, habit CRUD, completion, and habit analytics.",
    version="0.1.0",
    openapi_tags=[
        {"name": "Authentication", "description": "Register, login, logout"},
        {"name": "Habits", "description": "CRUD and completion endpoints for habits"},
        {"name": "Analytics", "description": "Aggregated analytics endpoints"}
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict as needed for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create DB tables on startup (dev only - in prod use migrations)
Base.metadata.create_all(bind=engine)

@app.get("/", tags=["Health"], summary="Health Check", description="Check if backend is alive.")
def health_check():
    """Simple health check endpoint."""
    return {"message": "Healthy"}

# Mount routers
app.include_router(auth_router)
app.include_router(habits_router)
app.include_router(analytics_router)
