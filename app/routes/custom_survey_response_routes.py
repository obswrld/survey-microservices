from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional
from app.database.connection import get_db
from app.models.custom_survey_response import (
    CustomSurveyResponseCreate,
    CustomSurveyResponseUpdate,
    CustomSurveyResponseDetail
)
from app.services.custom_survey_response_service import CustomSurveyResponseService

router = APIRouter(
    prefix="/custom-survey-responses",
    tags=["custom survey responses"]
)

def get_response_service(db=Depends(get_db)) -> CustomSurveyResponseService:
    return CustomSurveyResponseService(db)

@router.post("/", status_code=201, response_model=dict)
async def submit_response(
        response_data: CustomSurveyResponseCreate,
        service: CustomSurveyResponseService = Depends(get_response_service)
):
    try:
        response_id = service.create_response(response_data)
        return {
            "message": "Response submitted successfully",
            "response_id": response_id
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error submitting response: {str(e)}")

@router.get("/", status_code=200, response_model=dict)
async def get_all_responses(
        template_id: Optional[str] = Query(None),
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=100),
        service: CustomSurveyResponseService = Depends(get_response_service)
):
    responses = service.get_all_responses(template_id=template_id, skip=skip, limit=limit)
    total = service.count_responses(template_id=template_id)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "template_id": template_id,
        "responses": responses
    }

@router.get("/{response_id}", response_model=dict)
async def get_response_by_id(
        response_id: str,
        service: CustomSurveyResponseService = Depends(get_response_service)
):
    response = service.get_response_by_id(response_id)
    if not response:
        raise HTTPException(status_code=404, detail=f"Response with ID {response_id} not found")
    return response

@router.put("/{response_id}", response_model=dict)
async def update_response_by_id(
        response_id: str,
        response_data: CustomSurveyResponseUpdate,
        service: CustomSurveyResponseService = Depends(get_response_service)
):
    try:
        success = service.update_response(response_id, response_data)
        if not success:
            raise HTTPException(status_code=404, detail=f"Response with ID {response_id} not found or no changes made")
        return {
            "message": "Response updated successfully",
            "response_id": response_id
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating response: {str(e)}")

@router.delete("/{response_id}", response_model=dict)
async def delete_response_by_id(
        response_id: str,
        service: CustomSurveyResponseService = Depends(get_response_service)
):
    success = service.delete_response(response_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Response with ID {response_id} not found")
    return {
        "message": "Response deleted successfully",
        "response_id": response_id
    }