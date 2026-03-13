from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routes import employees, attendance

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="HRMS Lite", version="1.0.0")

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(employees.router, tags=["Employees"])
app.include_router(attendance.router, tags=["Attendance"])


@app.get("/")
def root():
    return {"message": "HRMS Lite API is running"}
