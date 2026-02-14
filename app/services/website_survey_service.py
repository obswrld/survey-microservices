from pymongo.database import Database
from bson import ObjectId
from datetime import datetime
from typing import List, Optional
from app.models.website_survey import SurveyCreate, SurveyUpdate

class WebsiteSurveyService:
    def __init__(self, db: Database):
        self.collection = db["website_building_surveys"]

    def create_survey(self, survey_data: SurveyCreate) -> str:
        survey_dict = survey_data.model_dump()
        survey_dict["created_at"] = datetime.utcnow()
        survey_dict["updated_at"] = datetime.utcnow()
        result = self.collection.insert_one(survey_dict)
        return str(result.inserted_id)

    def get_survey_by_id(self, survey_id: str) -> Optional[dict]:
        try:
            survey = self.collection.find_one({"_id": ObjectId(survey_id)})
            if survey:
                survey["_id"] = str(survey["_id"])
            return survey
        except Exception as e:
            print(f"Error getting survey: {e}")
            return None

    def get_all_surveys(self, skip: int = 0, limit: int = 10) -> List[dict]:
        surveys = list(self.collection.find().skip(skip).limit(limit))
        for survey in surveys:
            survey["_id"] = str(survey["_id"])
        return surveys

    def update_survey(self, survey_id: str, survey_data: SurveyUpdate) -> bool:
        try:
            update_dict = survey_data.model_dump(exclude_unset=True)
            if not update_dict:
                return False
            update_dict["updated_at"] = datetime.utcnow()
            result = self.collection.update_one(
                {"_id": ObjectId(survey_id)},
                {"$set": update_dict}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating survey: {e}")
            return False

    def delete_survey(self, survey_id: str) -> bool:
        try:
            result = self.collection.delete_one({"_id": ObjectId(survey_id)})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting survey: {e}")
            return False

    def count_surveys(self) -> int:
        return self.collection.count_documents({})