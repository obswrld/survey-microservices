from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr

class TagSurveyCreate(BaseModel):
    event_name: str = Field(..., min_length=1, max_length=300, description="Event name")
    event_date: str = Field(..., description="Date of event (YYYY-MM-DD)")
    event_location: str = Field(..., min_length=1, max_length=250, description="Location of event")
    event_description: Optional[str] = Field(None, description="Additional context regarding the event")
    requested_tags: List[str] = Field(..., min_items=1, description="List of requested tags (e.g), [music, outdoor, family friend]")
    tag_category: str = Field(..., description="Main Category: Entertainments, Business, Education, Sports etc.")
    reason_for_tags: Optional[str] = Field(None, description="Reason for tag creation, why these specific tags are created")
    organizer_name: str = Field(..., min_length=1, max_length=250, description="Organizer's name")
    organizer_email: EmailStr = Field(..., description="Email address of the organizer")
    organizer_phone_number: Optional[str] = Field(None, description="The phone number of the organizer")
    organization_name: str = Field(..., min_length=1, max_length=250, description="Name of the organization")
    target_audience: Optional[str] = Field(None, description="Audience of the events")
    expected_attendees: Optional[int] = Field(None, description="Number of attendees who attended the event")
    additional_notes: Optional[str] = Field(None, description="Additional notes about the event or information about the event")

class TagSurveyResponse(BaseModel):
    id: str = Field(..., alias="_id")
    event_name: str
    event_date: str
    event_location: str
    event_description: Optional[str]
    request_tags: List[str]
    tag_category: str
    reason_for_tags: Optional[str]
    organizer_name: str
    organizer_email: EmailStr
    organizer_phone_number: Optional[str]
    organization_name: str
    target_audience: Optional[str]
    expected_attendees: Optional[int]
    additional_notes: Optional[str]
    status: str = Field(default="pending", description="pending, approved and rejected")
    created_at: datetime
    updated_at: datetime

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": " ",
                "event_name": " ",
                "event_date": " ",
                "requested_tags": ["music", "outdoor", "family-friendly", "festival"],
                "tag_category": " ",
                "organizer_name": " ",
                "organizer_email": " ",
                "created_at": " ",
                "updated_at": " ",
                "status": " "
            }
        }

class TagSurveyUpdate(BaseModel):
    event_name: Optional[str] = None
    event_date: Optional[str] = None
    event_location: Optional[str] = None
    event_description: Optional[str] = None
    request_tags: Optional[List[str]] = None
    tag_category: Optional[str] = None
    reason_for_tags: Optional[str] = None
    organizer_name: Optional[str] = None
    organizer_email: Optional[str] = None
    organizer_phone_number: Optional[str] = None
    organization_name: Optional[str] = None
    target_audience: Optional[str] = None
    expected_attendees: Optional[int] = None
    additional_notes: Optional[str] = None
    status: Optional[str] = None