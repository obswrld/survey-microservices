from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from app.models.custom_survey_template import FieldSchema

class CustomSurveyResponseCreate(BaseModel):
    template_id: str = Field(..., description="ID of the survey template")
    responses: Dict[str, Any] = Field(..., description="Field responses as key-value pairs (field_id: value)")
    submitted_by: Optional[str] = Field(None, description="User ID or email of submitter")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata (IP, user agent, etc.)")

class CustomSurveyResponseDetail(BaseModel):
    id: str = Field(..., alias="_id", description="Response ID")
    template_id: str = Field(..., description="Template/Schema ID")
    template_name: str = Field(..., description="Survey name")
    schema: List[FieldSchema] = Field(..., description="Survey field definitions")
    responses: Dict[str, Any] = Field(..., description="Submitted field values")
    submitted_by: Optional[str] = Field(None, description="Submitter ID/email")
    submitted_at: datetime = Field(..., description="Submission timestamp")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": " ",
                "template_id": " ",
                "template_name": " ",
                "schema": [
                    {
                        "field_id": "f1",
                        "title": "First Name",
                        "type": "STRING",
                        "required": True
                    },
                    {
                        "field_id": "f2",
                        "title": "Rating",
                        "type": "NUMBER",
                        "required": True,
                        "validation": {"min_value": 1, "max_value": 5}
                    }
                ],
                "responses": {
                    "f1": "John Doe",
                    "f2": 5
                },
                "submitted_by": "customer@email.com",
                "submitted_at": "2024-02-12T14:30:00Z",
                "metadata": {
                    "ip_address": "192.168.1.1",
                    "user_agent": "Mozilla/5.0..."
                }
            }
        }

class CustomSurveyResponseUpdate(BaseModel):
    responses: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None