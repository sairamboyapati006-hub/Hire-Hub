from pydantic import BaseModel,EmailStr
from typing import Optional

# user registration schema 
class UserCreate(BaseModel):
    name:str
    email:EmailStr
    password:str
    role:Optional[str]="job_seeker"


# user login schema
class UserLogin(BaseModel):
    email:EmailStr
    password:str

#user response
# 
class UserResponse(BaseModel):
    id:int
    name:str
    email:EmailStr
    role:str

    class config:
        from_attributes=True        

#job creation
class JobCreate(BaseModel):
    title:str
    description:str
    company:str
    location:str
    salary:Optional[str]=None 

#job response
class JobResponse(BaseModel):
    id:int
    title:str
    description:str
    company:str
    location:str
    salary:Optional[str]=None
    is_active:bool

    class config:
        from_attributes=True

#aplication createion
class ApplicationCreate(BaseModel):
    job_id:int
    resume:Optional[str]=None

#application response
class ApplicationResponse(BaseModel):
    id:int
    job_id:int
    applicant_id:int
    resume:Optional[str]=None
    status:str

    class config:
        from_attributes=True     