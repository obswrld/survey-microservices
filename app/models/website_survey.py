from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

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
    brand_description: Optional[str] = Field(None, description="Brand description of the organization")
    theme_mode: str = Field(..., description="Theme mode of the organization")
    brand_guidelines_url: Optional[str] = Field(None, description="Brand Guidelines URL of the organization")

class WebStructure(BaseModel):
    required_pages: str = Field(..., description="Required pages URL of the organization")
    has_navigation: bool = Field(False, description="Whether the organization has navigation")
    has_footer: bool = Field(False, description="Whether the organization has footer")
    primary_cta: str = Field(..., description="Primary call to action for visitors")
    reference_websites: Optional[str] = Field(None, description="Reference web sites URL of the organization")

class WebContent(BaseModel):
    motto_tagline: str = Field(..., description="Motto tagline for homepage")
    homepage_description: str = Field(..., description="Homepage description")
    current_event: Optional[List[str]] = Field(None, description="Current event being promoted")
    past_events: Optional[List[str]] = Field(None, description="List of past 3-5 major events")
    show_portfolio: bool = Field(False, description="Show portfolio/gallery of past events")
    show_testimonials: bool = Field(False, description="Display testimonials from past attendees")
    testimonials: Optional[List[str]] = Field(None, description="List of testimonials")
    event_photos: Optional[List[str]] = Field(None, description="Paths to high-quality event photos")
    event_videos: Optional[List[str]] = Field(None, description="Paths to event videos")
    show_sponsors: bool = Field(False, description="Display sponsors and brands")
    sponsors: Optional[List[dict]] = Field(None, description="List of sponsor names and logo paths")

class Ticketing(BaseModel):
    sales_method: str = Field(..., description="How tickets should be sold: embedded, redirect, or custom")
    has_ticketing: bool = Field(False, description="Whether the organization has ticketing")
    ticket_type: Optional[List[str]] = Field(default_factory=list, description="Type of the ticket being sold at the event")
    ticket_price_range: Optional[List[float]] = Field(None, description="Price range of tickets")
    ticket_platform: Optional[List[str]] = Field(None, max_length=100, description="Platform of the ticket")
    ticket_url: Optional[str] = Field(None, description="ticketing url for the site.")

class AboutSection(BaseModel):
    organization_story: str = Field(..., description="About Organization events/event series")
    motto: Optional[str] = Field(None, description="About Motto event")
    mission_statement: Optional[str] = Field(None, description="About mission statement")
    vision_statement: Optional[str] = Field(None, description="About Vision statement")
    key_message: Optional[str] = Field(None, description="Specific message to highlights")
    accomplishment: Optional[List[dict]] = Field(None, description="Events accomplishment with description images")
    show_founder: bool = Field(False, description="Show foundation events/Display organizer's picture")
    founder_info: Optional[dict] = Field(None, description="Foundation info")
    show_team: bool = Field(False, description="Show teammates/Display the teams picture")
    team_members: Optional[List[dict]] = Field(None, description="List of team members with name, role amd image paths")
    sponsors: Optional[List[dict]] = Field(None, description="List of sponsor information")
    partners: Optional[List[dict]] = Field(None, description="List of partners information")

class Gallery(BaseModel):
    is_sectioned: bool = Field(False, description="Is Gallery sectioned by events or free photo gallery.")
    sectioned: Optional[List[dict]] = Field(None, description="List of sectioned gallery info with titles and images")
    photos: Optional[List[dict]] = Field(None, description="List of photo gallery info with titles and images")
    image_urls: Optional[List[dict]] = Field(default_factory=list, description="List of images URLs")
    video_urls: Optional[List[dict]] = Field(default_factory=list, description="List of video URLs")

class FAQ(BaseModel):
    questions: List[dict] = Field(..., description="List of FAQ items, with questions and answers")

class Domain(BaseModel):
    has_domain: bool = Field(False, description="Whether the domain is available")
    domain_name: Optional[str] = Field(None, max_length=250, description="Domain name")
    needs_help: bool = Field(False, description="needs help purchasing the domain.")

class SurveyCreate(BaseModel):
    general_info: GeneralInfo
    branding: Branding
    web_structure: WebStructure
    web_content: WebContent
    ticketing: Ticketing
    about: AboutSection
    gallery: Gallery
    faq: FAQ
    domain: Domain

class SurveyResponse(BaseModel):
    id: str = Field(..., alias="_id", description="Survey document ID")
    general_info: GeneralInfo
    branding: Branding
    web_structure: WebStructure
    web_content: WebContent
    ticketing: Ticketing
    about: AboutSection
    gallery: Gallery
    faq: FAQ
    domain: Domain
    status: str = Field(default="pending", description="Survey status: pending, in_progress, completed, approved")
    created_at: datetime
    updated_at: datetime

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "507f1f77bcf86cd799439011",
                "general_info": {
                    "organization_name": "EventPro Nigeria",
                    "event_category": "Music & Entertainment",
                    "email": "contact@eventpro.ng",
                    "phone": "+234 800 000 0000"
                },
                "created_at": "2024-02-10T10:30:00",
                "updated_at": "2024-02-10T10:30:00"
            }
        }

class SurveyUpdate(BaseModel):
    general_info: Optional[GeneralInfo] = None
    branding: Optional[Branding] = None
    web_structure: Optional[WebStructure] = None
    web_content: Optional[WebContent] = None
    ticketing: Optional[Ticketing] = None
    about: Optional[AboutSection] = None
    gallery: Optional[Gallery] = None
    faq: Optional[FAQ] = None
    domain: Optional[Domain] = None
    status: Optional[str] = None