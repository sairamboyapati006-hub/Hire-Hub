from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import Application, Job
from schemas import ApplicationCreate, ApplicationResponse
from dependencies import get_current_user


router = APIRouter(
    prefix="/applications",
    tags=["Applications"]
)


# Apply for a job
@router.post("/", response_model=ApplicationResponse)
def apply_for_job(
    application_data: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.role != "job_seeker":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only job seekers can apply"
        )

    job = db.query(Job).filter(
        Job.id == application_data.job_id,
        Job.is_active == True
    ).first()

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )

    existing_application = db.query(Application).filter(
        Application.job_id == application_data.job_id,
        Application.applicant_id == current_user.id
    ).first()

    if existing_application:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already applied for this job"
        )

    new_application = Application(
        job_id=application_data.job_id,
        applicant_id=current_user.id,
        resume=application_data.resume
    )

    db.add(new_application)
    db.commit()
    db.refresh(new_application)

    return new_application


# submitted by current user
@router.get("/my", response_model=list[ApplicationResponse])
def get_my_applications(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    applications = db.query(Application).filter(
        Application.applicant_id == current_user.id
    ).all()

    return applications