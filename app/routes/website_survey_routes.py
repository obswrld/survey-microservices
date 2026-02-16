from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List
from app.models.website_survey import (
    SurveyCreate,
    SurveyUpdate,
    SurveyResponse
)
from app.services.website_survey_service import WebsiteSurveyService
from app.database.connection import get_db

router = APIRouter(
    prefix="/website-survey",
    tags=["website-survey"]
)

def get_website_survey_service(db=Depends(get_db)) -> WebsiteSurveyService:
    return WebsiteSurveyService(db)

@router.post("/", status_code=201, response_model=dict)
async def create_website_survey(
        survey_data: SurveyCreate,
        service: WebsiteSurveyService = Depends(get_website_survey_service)
):
    try:
        survey_id = service.create_survey(survey_data)
        return {
            "message": "Website Survey Created successfully",
            "survey_id": survey_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(f"Error creating survey: {str(e)}"))

@router.get("/", response_model=dict)
async def get_all_website_surveys(
        skip: int = Query(0, ge=0, description="Number of records to skip"),
        limit: int = Query(10, ge=1, description="Maximum number of records to return"),
        service: WebsiteSurveyService = Depends(get_website_survey_service)
):
   surveys = service.get_all_surveys(skip=skip, limit=limit)
   total = service.count_surveys()
   return {
       "total": total,
       "skip": skip,
       "limit": limit,
       "surveys": surveys
   }

@router.get("/{survey_id}", response_model=dict)
async def get_website_survey(
        survey_id: str,
        service: WebsiteSurveyService = Depends(get_website_survey_service)
):
    survey = service.get_survey_by_id(survey_id)
    if not survey:
        raise HTTPException(status_code=404, detail=f"Survey with ID {survey_id} not found")
    return survey

@router.put("/{survey_id}", response_model=dict)
async def update_website_survey(
        survey_id: str,
        survey_data: SurveyUpdate,
        service: WebsiteSurveyService = Depends(get_website_survey_service)
):
    success = service.update_survey(survey_id, survey_data)
    if not success:
        raise HTTPException(status_code=404, detail="Survey not found or no changes made")
    return {
        "message": "Survey updated successfully",
        "survey_id": survey_id
    }

@router.delete("/{survey_id}", response_model=dict)
async def delete_website_survey(
        survey_id: str,
        service: WebsiteSurveyService = Depends(get_website_survey_service)
):
    status = service.delete_survey(survey_id)
    if not status:
        raise HTTPException(status_code=404, detail=f"Survey with {survey_id} not found")
    return {
        "message": "Survey deleted successfully",
        "survey_id": survey_id
    }