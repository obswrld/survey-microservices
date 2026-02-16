from pymongo.database import Database
from bson import ObjectId
from datetime import datetime
from typing import List, Optional, Dict, Any
from app.models.custom_survey_response import (
    CustomSurveyResponseCreate,
    CustomSurveyResponseDetail,
    CustomSurveyResponseUpdate
)

class CustomSurveyResponseService:
    def __init__(self, db: Database):
        self.responses_collection = db["custom_survey_responses"]
        self.templates_collection = db["custom_survey_templates"]


    def _validate_response(self, template: dict, responses: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        schema = template.get("schema", [])
        for field in schema:
            field_id = field.get("field_id")
            is_required = field.get("required", True)
            if is_required and field_id not in responses:
                return False, f"Required field '{field.get('title', field_id)}' is missing"
        for field_id, value in responses.items():
            field_def = next((f for f in schema if f.get("field_id") == field_id), None)
            if not field_def:
                return False, f"Unknown field '{field_id}' not in template schema"
            field_type = field_def.get("type")
            field_title = field_def.get("title", field_id)
            if value is None and not field_def.get("required", True):
                continue
            if field_type == "STRING":
                if not isinstance(value, str):
                    return False, f"Field '{field_title}' must be a string"
                validation = field_def.get("validation", {})
                if validation:
                    if "min_length" in validation and len(value) < validation["min_length"]:
                        return False, f"Field '{field_title}' must be at least {validation['min_length']} characters"
                    if "max_length" in validation and len(value) > validation["max_length"]:
                        return False, f"Field '{field_title}' must be at most {validation['max_length']} characters"
            elif field_type == "TEXT":
                if not isinstance(value, str):
                    return False, f"Field '{field_title}' must be a string"
                validation = field_def.get("validation", {})
                if validation:
                    if "min_length" in validation and len(value) < validation["min_length"]:
                        return False, f"Field '{field_title}' must be at least {validation['min_length']} characters"
                    if "max_length" in validation and len(value) > validation["max_length"]:
                        return False, f"Field '{field_title}' must be at most {validation['max_length']} characters"
            elif field_type == "NUMBER":
                if not isinstance(value, (int, float)):
                    return False, f"Field '{field_title}' must be a number"
                validation = field_def.get("validation", {})
                if validation:
                    if "min_value" in validation and value < validation["min_value"]:
                        return False, f"Field '{field_title}' must be at least {validation['min_value']}"
                    if "max_value" in validation and value > validation["max_value"]:
                        return False, f"Field '{field_title}' must be at most {validation['max_value']}"
            elif field_type == "BOOLEAN":
                if not isinstance(value, bool):
                    return False, f"Field '{field_title}' must be a boolean (true/false)"
            elif field_type == "DATE":
                if not isinstance(value, str):
                    return False, f"Field '{field_title}' must be a date string (YYYY-MM-DD)"
            elif field_type == "EMAIL":
                if not isinstance(value, str):
                    return False, f"Field '{field_title}' must be a string"
                if "@" not in value or "." not in value:
                    return False, f"Field '{field_title}' must be a valid email address"
            elif field_type == "OPTION":
                options = field_def.get("options", [])
                if value not in options:
                    return False, f"Field '{field_title}' must be one of: {', '.join(options)}"
            elif field_type == "FILE":
                if not isinstance(value, str):
                    return False, f"Field '{field_title}' must be a file path string"
        return True, None

    def create_response(self, response_data: CustomSurveyResponseCreate) -> Optional[str]:
        try:
            template = self.templates_collection.find_one({
                "_id": ObjectId(response_data.template_id)
            })
            if not template:
                raise ValueError(f"Template with ID {response_data.template_id} not found")
            is_valid, error_message = self._validate_response(template, response_data.responses)
            if not is_valid:
                raise ValueError(error_message)
            response_dict = response_data.model_dump()
            response_dict["template_name"] = template.get("name")
            response_dict["submitted_at"] = datetime.utcnow()
            result = self.responses_collection.insert_one(response_dict)
            self.templates_collection.update_one(
                {"_id": ObjectId(response_data.template_id)},
                {"$inc": {"response_count": 1}}
            )
            return str(result.inserted_id)
        except ValueError:
            raise
        except Exception as e:
            print(f"Error creating response: {e}")
            return None

    def get_response_by_id(self, response_id: str) -> Optional[Dict[str, Any]]:
        try:
            response = self.responses_collection.find_one(
                {"_id": ObjectId(response_id)}
            )
            if not response:
                return None
            template = self.templates_collection.find_one(
                {"_id": ObjectId(response["template_id"])}
            )
            if not template:
                print(f"Warning: Template {response['template_id']} not found for response {response_id}")
                return None
            response["_id"] = str(response["_id"])
            response["template_id"] = str(response["template_id"])
            result = {
                "_id": response["_id"],
                "template_id": response["template_id"],
                "template_name": template.get("template_name"),
                "schema": template.get("schema", []),
                "responses": response.get("responses", {}),
                "submitted_by": response.get("submitted_by"),
                "submitted_at": response.get("submitted_at"),
                "metadata": response.get("metadata", {}),
            }
            return result
        except Exception as e:
            print(f"Error getting response: {e}")
            return None

    def get_all_responses(self, template_id: Optional[str] = None, skip: int = 0, limit: int = 10) -> List[Dict]:
        filter_criteria = {}
        if template_id:
            filter_criteria["template_id"] = template_id
        responses = list(
            self.responses_collection.find(filter_criteria)
            .skip(skip)
            .limit(limit)
        )
        for response in responses:
            response["_id"] = str(response["_id"])
        return responses

    def update_response(self, response_id: str, response_data: CustomSurveyResponseUpdate) -> bool:
        try:
            update_dict = response_data.model_dump(exclude_unset=True)
            if not update_dict:
                return False
            if "responses" in update_dict:
                existing_response = self.responses_collection.find_one({
                    "_id": ObjectId(response_id)
                })
                if not existing_response:
                    return False
                template = self.templates_collection.find_one({
                    "_id": ObjectId(existing_response["template_id"])
                })
                if template:
                    is_valid, error_message = self._validate_response(template, update_dict["responses"])
                    if not is_valid:
                        raise ValueError(error_message)
            result = self.responses_collection.update_one(
                {"_id": ObjectId(response_id)},
                {"$set": update_dict}
            )
            return result.modified_count > 0
        except ValueError:
            raise
        except Exception as e:
            print(f"Error updating response: {e}")
            return False

    def delete_response(self, response_id: str) -> bool:
        try:
            result = self.responses_collection.delete_one({
                "_id": ObjectId(response_id)
            })
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting response: {e}")
            return False

    def count_responses(self, template_id: Optional[str] = None) -> int:
        filter_criteria = {}
        if template_id:
            filter_criteria["template_id"] = template_id
        return self.responses_collection.count_documents(filter_criteria)