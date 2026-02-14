from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class FieldValidation(BaseModel):
    min_length: Optional[int] = Field(None, description="Minimum length for STRING/TEXT")
    max_length: Optional[int] = Field(None, description="Maximum length for STRING/TEXT")
    min_value: Optional[float] = Field(None, description="Minimum value for NUMBER")
    max_value: Optional[float] = Field(None, description="Maximum value for NUMBER")
    pattern: Optional[str] = Field(None, description="Regex pattern for validation")

class FieldSchema(BaseModel):
    field_id: str = Field(..., description="Unique field identifier (e.g., 'f1', 'f2')")
    title: str = Field(..., min_length=1, max_length=200, description="Display label for the field")
    type: str = Field(..., description="Field type: STRING, TEXT, NUMBER, DATE, BOOLEAN, OPTION, EMAIL, FILE")
    required: bool = Field(default=True, description="Whether this field is required")
    options: Optional[List[str]] = Field(None, description="Available options for OPTION type")
    validation: Optional[FieldValidation] = Field(None, description="Validation rules for the field")
    placeholder: Optional[str] = Field(None, description="Placeholder text for input fields")
    help_text: Optional[str] = Field(None, description="Help text shown below the field")

class CustomSurveyTemplateCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, description="Survey name")
    description: Optional[str] = Field(None, max_length=1000, description="Survey description")
    schema: List[FieldSchema] = Field(..., min_items=1, description="List of fields in the survey")
    created_by: Optional[str] = Field(None, description="User ID or email of creator")
    is_active: bool = Field(default=True, description="Whether this template is active")

class CustomSurveyTemplateResponse(BaseModel):
    id: str = Field(..., alias="_id", description="Template ID")
    name: str
    description: Optional[str]
    schema: List[FieldSchema]
    created_by: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    response_count: Optional[int] = Field(default=0, description="Number of responses received")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": " ",
                "name": " ",
                "description": " ",
                "schema": [
                    {
                        "field_id": "f1",
                        "title": "First Name",
                        "type": "STRING",
                        "required": True,
                        "placeholder": "Enter your first name"
                    },
                    {
                        "field_id": "f2",
                        "title": "Rating",
                        "type": "NUMBER",
                        "required": True,
                        "validation": {
                            "min_value": 1,
                            "max_value": 5
                        }
                    }
                ],
                "created_by": " ",
                "is_active": True,
                "created_at": " ",
                "updated_at": " ",
                "response_count": 25
            }
        }

class CustomSurveyTemplateUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    schema: Optional[List[FieldSchema]] = None
    is_active: Optional[bool] = None