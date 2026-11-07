from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import Job
from schemas import JobCreate, JobResponse
from dependencies import get_current_user


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)


# Get all active jobs
@router.get("/", response_model=list[JobResponse])
def get_jobs(db: Session = Depends(get_db)):
    jobs = db.query(Job).filter(
        Job.is_active == True
    ).all()

    return jobs


# Get a single job
@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(
        Job.id == job_id,
        Job.is_active == True
    ).first()

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )

    return job


# Create a new job
@router.post("/", response_model=JobResponse)
def create_job(
    job_data: JobCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.role != "recruiter":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only recruiters can post jobs"
        )

    new_job = Job(
        title=job_data.title,
        description=job_data.description,
        company=job_data.company,
        location=job_data.location,
        salary=job_data.salary,
        recruiter_id=current_user.id
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return new_job