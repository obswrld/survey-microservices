from datetime import datetime
from typing import Optional, List
from bson import ObjectId
from pymongo.database import Database
from app.models.tag_survey import TagSurveyCreate, TagSurveyUpdate

class TagSurveyService:
    def __init__(self, db: Database):
        self.collection = db["event_tags_surveys"]

    def create_survey(self, survey_data: TagSurveyCreate) -> str:
        survey_dict = survey_data.model_dump()
        survey_dict["created_at"] = datetime.utcnow()
        survey_dict["updated_at"] = datetime.utcnow()
        if "status" not in survey_dict:
            survey_dict["status"] = "pending"
        result = self.collection.insert_one(survey_dict)
        return str(result.inserted_id)

    def get_survey_by_id(self, survey_id: str) -> Optional[dict]:
        try:
            surveys = self.collection.find_one({"_id": ObjectId(survey_id)})
            if surveys:
                surveys["_id"] = str(surveys["_id"])
            return surveys
        except Exception as e:
            print(f"Error get the tag survey: {e}")
            return None

    def get_all_surveys(self, skip: int = 0, limit: int = 10) -> List[dict]:
        surveys = list(self.collection.find().skip(skip).limit(limit))
        for survey in surveys:
            survey["_id"] = str(survey["_id"])
        return surveys

    def update_survey(self, survey_id: str, survey_data: TagSurveyUpdate) -> bool:
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
            print(f"Error updating tag survey: {e}")
            return False

    def delete_survey(self, survey_id: str) -> bool:
        try:
            survey_result = self.collection.delete_one({"_id": ObjectId(survey_id)})
            return survey_result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting tag survey: {e}")
            return False

    def count_surveys(self) -> int:
        return self.collection.count_documents({})

    def get_survey_by_status(self, status: str, skip: int = 0, limit: int = 10) -> List[dict]:
        surveys = list(
            self.collection.find({"status": status})
            .skip(skip)
            .limit(limit)
        )
        for survey in surveys:
            survey["_id"] = str(survey["_id"])
        return surveys

    def get_survey_by_organizer(self, organizer_email: str, skip: int = 0, limit: int = 10) -> List[dict]:
        survey_organizers = list(
            self.collection.find({"organizer_email": organizer_email})
            .skip(skip)
            .limit(limit)
        )
        for survey_organizer in survey_organizers:
            survey_organizer["_id"] = str(survey_organizer["_id"])
        return survey_organizers