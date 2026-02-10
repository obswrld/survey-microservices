from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class GeneralInfo(BaseModel):
    organization_name: str = Field(..., min_legth=1, max_length=200, description="Name of the organization conducting the survey")
    event_name: str = Field(..., min_legth=1, max_length=200, description="Name of the event for which the survey is being conducted")
    event_date: Optional[str] = Field(None, description="Date of the event (YYYY-MM-DD)")
    event_location: Optional[str] = Field(None, max_length=250, description="Location of the event")
    organization_logo: Optional[str] = Field(None, description="Path to Upload the organization logo file.")
    organization_email: EmailStr = Field(..., description="The Contact Email")
    organization_phone: Optional[str] = Field(None, description="The Contact Phone Number")
    organization_social_media: Optional[dict] = Field(
        default_factory=dict,
        description="Social media handles (X, Instagram, Facebook, LinkedIn) for the organization"
    )
    event_type: Optional[str] = Field(None, max_length=100, description="Type of the event (Conference, Workshop, Webinar)")
    event_attendees: Optional[int] = Field(None, ge=0, description="Number of attendees at the event")