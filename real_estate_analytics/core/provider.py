"""Service provider management for real estate analytics services"""

from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class ServiceProvider:
    """Represents a service provider offering real estate analytics services"""
    
    name: str
    title: str
    company: str
    specialization: str = "Real Estate Analytics"
    
    # Contact information
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    
    # Professional profile
    experience_years: int = 0
    certifications: List[str] = field(default_factory=list)
    languages: List[str] = field(default_factory=lambda: ["English"])
    
    # Technical skills
    technical_skills: List[str] = field(default_factory=list)
    tools_expertise: List[str] = field(default_factory=list)
    
    # Service offerings
    service_categories: List[str] = field(default_factory=list)
    hourly_rate: Optional[float] = None
    availability: str = "Available"  # Available, Busy, Unavailable
    
    # Performance metrics
    completed_projects: int = 0
    client_rating: float = 5.0
    response_time_hours: int = 24
    
    created_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Initialize default values"""
        if not self.technical_skills:
            self.technical_skills = [
                "SQL", "Python", "Data Analysis", "Statistical Analysis",
                "Dashboard Creation", "Data Visualization"
            ]
        
        if not self.tools_expertise:
            self.tools_expertise = [
                "Python (Pandas, Plotly, Dash)", "SQL", "Excel", "Power BI"
            ]
        
        if not self.service_categories:
            self.service_categories = [
                "Business Analytics",
                "Data Platform Setup",
                "KPI Identification", 
                "A/B Testing",
                "Dashboard Creation",
                "Data Analysis",
                "Strategic Analytics"
            ]
    
    def add_skill(self, skill: str) -> None:
        """Add a technical skill to the provider's profile"""
        if skill not in self.technical_skills:
            self.technical_skills.append(skill)
    
    def add_tool_expertise(self, tool: str) -> None:
        """Add tool expertise to the provider's profile"""
        if tool not in self.tools_expertise:
            self.tools_expertise.append(tool)
    
    def add_certification(self, certification: str) -> None:
        """Add a certification to the provider's profile"""
        if certification not in self.certifications:
            self.certifications.append(certification)
    
    def update_availability(self, status: str) -> None:
        """Update provider availability status"""
        valid_statuses = ["Available", "Busy", "Unavailable"]
        if status in valid_statuses:
            self.availability = status
        else:
            raise ValueError(f"Invalid status. Must be one of: {valid_statuses}")
    
    def complete_project(self, rating: float = 5.0) -> None:
        """Record a completed project and update metrics"""
        self.completed_projects += 1
        # Update average rating
        total_rating = self.client_rating * (self.completed_projects - 1) + rating
        self.client_rating = total_rating / self.completed_projects
    
    def can_handle_service(self, service_type: str) -> bool:
        """Check if provider can handle a specific service type"""
        return service_type in self.service_categories
    
    def get_provider_profile(self) -> Dict:
        """Return a comprehensive provider profile"""
        return {
            "basic_info": {
                "name": self.name,
                "title": self.title,
                "company": self.company,
                "specialization": self.specialization,
                "location": self.location
            },
            "contact": {
                "email": self.email,
                "phone": self.phone
            },
            "professional": {
                "experience_years": self.experience_years,
                "certifications": self.certifications,
                "languages": self.languages
            },
            "technical": {
                "skills": self.technical_skills,
                "tools": self.tools_expertise
            },
            "services": {
                "categories": self.service_categories,
                "hourly_rate": self.hourly_rate,
                "availability": self.availability
            },
            "performance": {
                "completed_projects": self.completed_projects,
                "client_rating": round(self.client_rating, 2),
                "response_time_hours": self.response_time_hours
            },
            "metadata": {
                "created_at": self.created_at.isoformat()
            }
        }
    
    def __str__(self) -> str:
        return f"{self.name} - {self.title} @ {self.company} (Rating: {self.client_rating:.1f})"

