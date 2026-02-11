from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class GeneralInfo(BaseModel):
    organization_name: str = Field(..., min_length=1, max_length=200, title="Organization Name")
    event_name: str = Field(..., min_length=1, max_length=200, title="Event Name")
    event_date: Optional[str] = Field(None, description="Date of the event (YYYY-MM-DD)")
    event_location: Optional[str] = Field(None, max_length=250, description="Location of the event")
    organization_email: EmailStr = Field(..., description="The Contact Email")
    organization_phone: Optional[str] = Field(None, description="The Contact Phone Number")
    organization_social_media: Optional[dict] = Field(
        default_factory=dict,
        description="Social media handles (X, Instagram, Facebook, LinkedIn) for the organization"
    )
    event_type: Optional[str] = Field(None, max_length=100, description="Type of the event (Conference, Workshop, Webinar)")
    event_attendees: Optional[int] = Field(None, ge=0, description="Number of attendees at the event")

class Branding(BaseModel):
    brand_colors: Optional[str] = Field(None, description="List of brand colors (hex codes)")
    organization_logo: Optional[str] = Field(None, description="Path to Upload the organization logo file.")
    fonts: Optional[str] = Field(None, max_length=100, description="Path to Upload the fonts file.")
    target_audience: Optional[str] = Field(None, description="Target audience for this event of the organization.")
    brand_description: str = Field(None, description="Brand description of the organization")
    theme_mode: str = Field(None, description="Theme mode of the organization")
    brand_guidelines_url: Optional[str] = Field(None, description="Brand Guidelines URL of the organization")

class WebStructure(BaseModel):
    required_pages: Optional[str] = Field(..., description="Required pages URL of the organization")
    has_navigation: bool = Field(None, description="Whether the organization has navigation")
    has_footer: bool = Field(None, description="Whether the organization has footer")

class WebContent(BaseModel):

class Ticketing(BaseModel):

class AboutSection(BaseModel):

class Gallery(BaseModel):

class FAQ(BaseModel):

class Domain(BaseModel):
    general_info: GeneralInfo
    branding: Branding
    web_structure: WebStructure
    web_content: WebContent
    gallery: Gallery
    faq: FAQ