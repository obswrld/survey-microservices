from app.routes.website_survey_routes import router as website_survey_router
from app.routes.tag_survey_routes import router as tag_survey_router
from app.routes.custom_survey_template_routes import router as custom_survey_template_router
from app.routes.custom_survey_response_routes import router as custom_survey_response_router

__all__ = [
    "website_survey_router",
    "tag_survey_router",
    "custom_survey_template_router",
    "custom_survey_response_router",
]