from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr

class TimestampMixin(BaseModel):
    created_at: datetime = Field(..., description="The date and time the survey was created")
    updated_at: datetime = Field(..., description="The date and time the survey was updated")

class SurveyMetadata(BaseModel):
    submitted_by: Optional[str] = Field(None, description="Use Id or email of the person submitting this survey")
    status: str = Field(default="pending", description="The status of the survey to be submitted")
    notes: Optional[str] = Field(None, description="Notes about the submitted survey")
    priority: Optional[str] = Field(default="Normal", description="The priority of the survey (low, normal, high or urgent)")

class ContactInfo(BaseModel):
    name: str = Field(..., min_length=3, max_length=200, description="The name of the person who submitted the survey")
    email: EmailStr = Field(..., description="The email address of the person who submitted the survey")
    phone_number: Optional[str] = Field(None, description="The phone number of the person submitted the survey")
    organization: str = Field(..., description="The name of the organization the person submitted the survey")