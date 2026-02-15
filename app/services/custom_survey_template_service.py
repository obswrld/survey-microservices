from datetime import datetime
from typing import Optional, List
from bson import ObjectId
from pymongo.database import Database
from app.models import CustomSurveyTemplateCreate, CustomSurveyTemplateUpdate


class CustomSurveyTemplateService:
    def __init__(self, db: Database):
        self.templates_collection = db["custom_survey_templates"]
        self.responses_collection = db["custom_survey_responses"]

    def create_template(self, template_data: CustomSurveyTemplateCreate) -> str:
        template_dict = template_data.model_dump()
        template_dict["created_at"] = datetime.utcnow()
        template_dict["updated_at"] = datetime.utcnow()
        template_dict["response_count"] = 0
        result = self.templates_collection.insert_one(template_dict)
        return str(result.inserted_id)

    def get_template_by_id(self, template_id: str) -> Optional[dict]:
        try:
            template = self.templates_collection.find_one({"_id": ObjectId(template_id)})
            if not template:
                return None
            template["_id"] = str(template["_id"])
            response_count = self.responses_collection.count_documents({
                "template_id": str(template["_id"])
            })
            template["response_count"] = response_count
            return template
        except Exception as e:
            print(f"Error getting template: {e}")
            return None

    def get_all_templates(self, skip: int = 0, limit: int = 10, is_active: Optional[bool] = None) -> List[dict]:
        filter_criteria = {}
        if is_active is not None:
            filter_criteria["is_active"] = is_active
        templates = list(
            self.templates_collection.find(filter_criteria)
            .skip(skip)
            .limit(limit)
        )
        for template in templates:
            template["_id"] = str(template["_id"])
            response_count = self.responses_collection.count_documents({
                "template_id": str(template["_id"])
            })
            template["response_count"] = response_count
        return templates

    def update_templates(self, template_data: CustomSurveyTemplateUpdate) -> bool:
        try:
            update_dict = template_data.model_dump(exclude_unset=True)
            if not update_dict:
                return False
            update_dict["updated_at"] = datetime.utcnow()
            result = self.templates_collection.update_one(
                {"_id": template_data.template_id},
                {"$set": update_dict}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating template: {e}")
            return False

    def delete_template(self, template_id: str) -> bool:
        try:
            result = self.templates_collection.delete_one({"_id": ObjectId(template_id)})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting template: {e}")
            return False