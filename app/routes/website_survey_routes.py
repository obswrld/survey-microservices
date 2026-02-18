from fastapi import APIRouter, HTTPException, Query, Depends
from app.models.website_survey import (
    SurveyCreate,
)
from app.services.website_survey_service import WebsiteSurveyService
from app.database.connection import get_db

router = APIRouter(
    prefix="/website-survey",
    tags=["website survey"]
)

def get_survey_service(db=Depends(get_db)) -> WebsiteSurveyService:
    """
       Dependency function that creates and returns a WebsiteSurveyService instance

    Args:
       db: Database connection (injected by FastAPI)

    Returns:
       WebsiteSurveyService: Service instance for handling business logic
    """
    return WebsiteSurveyService(db)

@router.get("/", response_model=dict)
async def list_submissions(
        skip: int = Query(0, ge=0, description="Number of records to skip"),
        limit: int = Query(10, ge=1,le=100, description="Maximum number of records to return"),
        survey_service: WebsiteSurveyService = Depends(get_website_survey_service)
):
    """
        Get all website surveys with pagination

    Args:
    skip: Number of records to skip (default: 0)
    limit: Maximum records to return (default: 10, max: 100)
    service: Service instance (injected by FastAPI)

    Returns:
    dict: Paginated list of surveys with metadata
    """
    surveys = survey_service.list_submissions(skip=skip, limit=limit)
    total = survey_service.count()
    return {
       "total": total,
       "skip": skip,
       "limit": limit,
       "surveys": surveys
   }

@router.post("/", status_code=201, response_model=dict)
async def submit(
        survey_data: SurveyCreate,
        service: WebsiteSurveyService = Depends(get_website_survey_service)
):
    """
    Create a new website building survey
    Args:
        survey_data: Survey data validated by Pydantic
        service: Service instance (injected by FastAPI)
    Returns:
        dict: Success message with survey ID
    Raises:
        HTTPException 500: If creation fails
    """
    try:
        survey_id = service.submit(survey_data)
        return {
            "message": "Website Survey Created successfully",
            "survey_id": survey_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating survey: {str(e)}")

@router.get("/{survey_id}", response_model=dict)
async def get_by_id(
        survey_id: str,
        service: WebsiteSurveyService = Depends(get_website_survey_service)
):
    """
    Get a specific website survey by ID

    Args:
        survey_id: Survey ID from URL path
        service: Service instance (injected by FastAPI)

    Returns:
        dict: Survey data

    Raises:
        HTTPException 404: If survey not found
        HTTPException 400: If survey_id format is invalid
    """
    survey = service.get_by_id(survey_id)
    if not survey:
        raise HTTPException(status_code=404, detail=f"Survey with ID {survey_id} not found")
    return survey