from pymongo.database import Database
from bson import ObjectId
from datetime import datetime, UTC
from typing import List, Optional
from app.models.website_survey import SurveyCreate

class WebsiteSurveyService:
    """
    Initialize the service with database connection

    Args:
    db: MongoDB database instance
    """

    def __init__(self, db: Database):
        self.collection = db["website_building_surveys"]

    def list_submissions(self, skip: int = 0, limit: int = 10) -> List[dict]:
        """
        Get all surveys with pagination

        Args:
            skip: Number of records to skip (for pagination)
            limit: Maximum number of records to return

        Returns:
            List[dict]: List of survey documents
        """

        surveys = list(self.collection.find().skip(skip).limit(limit))
        for survey in surveys:
            survey["_id"] = str(survey["_id"])
        return surveys

    def submit(self, survey_data: SurveyCreate) -> str:
        """
        Create a new survey

        Args:
            survey_data: Survey data from request

        Returns:
            str: ID of the created survey

        Raises:
            Exception: If creation fails
        """

        survey_dict = survey_data.model_dump()
        survey_dict["created_at"] = datetime.now(UTC)
        survey_dict["updated_at"] = datetime.now(UTC)
        result = self.collection.insert_one(survey_dict)
        return str(result.inserted_id)

    def get_by_id(self, survey_id: str) -> Optional[dict]:
        """
        Get a survey by its ID

        Args:
            survey_id: The survey ID

        Returns:
            dict: Survey document if found, None otherwise
        """

        try:
            survey = self.collection.find_one({"_id": ObjectId(survey_id)})
            survey["_id"] = str(survey["_id"])
            return survey
        except Exception as e:
            print(f"Error getting survey: {e}")
            return None

    def count(self) -> int:
        """
        Count total number of surveys

        Returns:
            int: Total count of surveys
        """

        return self.collection.count_documents({})