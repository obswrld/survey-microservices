from datetime import datetime
from typing import Optional
from bson import ObjectId
from pymongo.database import Database
from app.models.website_survey import SurveyCreate

class WebsiteSurveyServices:
    def __init__(self, db: Database):
        self.collection = db['website_building_survey']

    def create_survey(self, survey_data: SurveyCreate) -> str:
        survey_dict = survey_data.model_dump()
        survey_dict["created_at"] = datetime.utcnow()
        survey_dict["updated_at"] = datetime.utcnow()
        survey = self.collection.insert_one(survey_dict)
        return str(survey.inserted_id)

    def get_survey_by_id(self, survey_id: str) -> Optional[dict]:
        try:
            survey = self.collection.find_one({"_id": ObjectId(survey_id)})
            if survey:
                survey["_id"] = str(survey["_id"])
            return survey
        except Exception as e:
            print(f"Error getting survey: {e}")
            return None