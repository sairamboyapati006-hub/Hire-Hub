from sqlalchemy import Column,Integer,String,Boolean,ForeignKey,DateTime,Text
from sqlalchemy.orm import relationship 
from datetime import datetime
from database import Base

#user TAble
class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String(100),nullable=False)
    email=Column(String(100),unique=True,index=True,nullable=False)
    hashed_password=Column(String(250),nullable=False)
    role=Column(String(20),default="job_seeker")

#job table
class Job(Base):
    __tablename__="jobs"
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String(150),nullable=False)
    description=Column(Text,nullable=False)
    company=Column(String(100),nullable=False)
    location=Column(String(100),nullable=False)
    salary=Column(String(50))
    is_active=Column(Boolean,default=True)
    recruiter_id=Column(Integer,ForeignKey("users.id"))

#aplication table
class Application (Base):
    __tablename__="applications"
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    applicant_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    resume = Column(String(255))
    status = Column(String(30), default="pending")
    applied_at = Column(DateTime, default=datetime.utcnow)
            