from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional
from app.models.custom_survey_template import (
    CustomSurveyTemplateCreate,
    CustomSurveyTemplateResponse,
    CustomSurveyTemplateUpdate
)
from app.services.custom_survey_template_service import CustomSurveyTemplateService
from app.database.connection import get_db

router = APIRouter(
    prefix="/custom-survey-template",
    tags=["custom survey template"]
)

def get_template_service(db=Depends(get_db)) -> CustomSurveyTemplateService:
    return CustomSurveyTemplateService(db)

@router.post("/", status_code=201, response_model=dict)
async def create_tag_survey_template(
        template_data: CustomSurveyTemplateCreate,
        service: CustomSurveyTemplateService = Depends(get_template_service)
):
    try:
        template_id = service.create_template(template_data)
        return {
            "message": "Template was created successfully",
            "template_id": template_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating template: {str(e)}")

@router.get("/", response_model=dict)
async def get_all_templates(
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=100),
        is_active: Optional[bool] = Query(None),
        service: CustomSurveyTemplateService = Depends(get_template_service)
):
    templates = service.get_all_templates(skip=skip, limit=limit, is_active=is_active)
    total = service.count_templates(is_active=is_active)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "templates": templates
    }

@router.get("/{template_id}", response_model=dict)
async def get_template_by_id(
        template_id: str,
        service: CustomSurveyTemplateService = Depends(get_template_service)
):
    template = service.get_template_by_id(template_id)
    if not template:
        raise HTTPException(status_code=404, detail=f"Template with ID {template_id} not found")
    return template

@router.put("/{template_id}", response_model=dict)
async def update_template(
        template_id: str,
        template_data: CustomSurveyTemplateUpdate,
        service: CustomSurveyTemplateService = Depends(get_template_service)
):
    success = service.update_template(template_id, template_data)
    if not success:
        raise HTTPException(status_code=404, detail=f"Template with ID {template_id} not found or no changes made")
    return {
        "message":"Template was updated successfully",
        "template_id": template_id
    }

@router.delete("/{template_id}", response_model=dict)
async def delete_template(
        template_id: str,
        service: CustomSurveyTemplateService = Depends(get_template_service)
):
    status = service.delete_template(template_id)
    if not status:
        raise HTTPException(status_code=404, detail=f"Template with ID {template_id} not found")
    return {
        "message":"Template was deleted successfully",
        "template_id": template_id
    }