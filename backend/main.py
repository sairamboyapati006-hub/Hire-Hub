from fastapi import FastAPI

from database import engine, Base
from routers import auth, jobs, applications

import models
from fastapi.middleware.cors import CORSMiddleware


# Create database tables
Base.metadata.create_all(bind=engine)


# Create FastAPI application
app = FastAPI(
    title="HireHub - Job Portal",
    description="Job Portal and Recruitment Management System",
    version="1.0.0"
)


 #Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# Connect routers
app.include_router(auth.router)
app.include_router(jobs.router)
app.include_router(applications.router)


# Home 
@app.get("/")
def home():
    return {
        "message": "Welcome to HireHub API"
    }