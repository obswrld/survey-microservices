from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List
from app.models.tag_survey import (
    TagSurveyCreate,
    TagSurveyResponse,
    TagSurveyUpdate
)
from app.services.tag_survey_service import TagSurveyService
from app.database.connection import get_db

router = APIRouter(
    prefix="/tag-survey",
    tags=["Tag Survey"]
)

def get_tag_survey_service(db=Depends(get_db)) -> TagSurveyService:
    return TagSurveyService(db)

@router.post("/", status_code=201, response_model=dict)
async def create_tag_survey(
        survey_data: TagSurveyCreate,
        service: TagSurveyService = Depends(get_tag_survey_service)
):
    try:
        survey_id = service.create_survey(survey_data)
        return {
            "message": "Tag Survey created successfully",
            "survey_id": survey_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(f"Error creating survey: {str(e)}"))

@router.get("/", response_model=dict)
async def get_all_tag_surveys(
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=100),
        service: TagSurveyService = Depends(get_tag_survey_service)
):
    surveys = service.get_all_surveys(skip=skip, limit=limit)
    total = service.count_surveys()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "surveys": surveys
    }

@router.get("/status/{status}", response_model=dict)
async def get_tag_survey_status(
        status: str,
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=100),
        service: TagSurveyService = Depends(get_tag_survey_service)
):
    surveys = service.get_survey_by_status(status=status, skip=skip, limit=limit)
    return {
        "status": status,
        "total": len(surveys),
        "skip": skip,
        "limit": limit,
        "surveys": surveys
    }

@router.get("/organizer/{organizer_email}", response_model=dict)
async def get_survey_by_organizer(
        organizer_email: str,
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=100),
        service: TagSurveyService = Depends(get_tag_survey_service)
):
    surveys = service.get_survey_by_organizer(organizer_email=organizer_email, skip=skip, limit=limit)
    return {
        "organizer_email": organizer_email,
        "total": len(surveys),
        "skip": skip,
        "limit": limit,
        "surveys": surveys
    }

@router.get("/{survey_id}", response_model=dict)
async def get_survey_by_id(
        survey_id: str,
        service: TagSurveyService = Depends(get_tag_survey_service)
):
    survey = service.get_survey_by_id(survey_id)
    if not survey:
        raise HTTPException(status_code=404, detail=f"Tag survey with ID {survey_id} not found")
    return survey

@router.put("/{survey_id}", response_model=dict)
async def update_survey_by_id(
        survey_id: str,
        survey_data: TagSurveyUpdate,
        service: TagSurveyService = Depends(get_tag_survey_service)
):
    success = service.update_survey(survey_id, survey_data)
    if not success:
        raise HTTPException(status_code=404, detail=f"Tag survey not found or no changes were made")
    return {
        "message": "Tag survey updated successfully",
        "survey_id": survey_id
    }

@router.delete("/{survey_id}", response_model=dict)
async def delete_survey_by_id(
        survey_id: str,
        service: TagSurveyService = Depends(get_tag_survey_service)
):
    success = service.delete_survey(survey_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Tag survey with ID {survey_id} not found")
    return {
        "message": "Tag survey deleted successfully",
        "survey_id": survey_id
    }