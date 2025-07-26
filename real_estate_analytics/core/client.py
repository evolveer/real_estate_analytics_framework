"""Client management for real estate analytics services"""

from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class Client:
    """Represents a client requesting real estate analytics services"""
    
    name: str
    location: str
    company: Optional[str] = None
    industry: str = "Real Estate"
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    business_type: str = "Consumer Products"  # Default from the example
    created_at: datetime = field(default_factory=datetime.now)
    
    # Business profile information
    company_size: Optional[str] = None
    annual_revenue: Optional[str] = None
    primary_markets: List[str] = field(default_factory=list)
    
    # Data and analytics maturity
    current_analytics_tools: List[str] = field(default_factory=list)
    data_sources: List[str] = field(default_factory=list)
    analytics_experience: str = "Beginner"  # Beginner, Intermediate, Advanced
    
    def __post_init__(self):
        """Initialize default values and validate data"""
        if not self.primary_markets:
            self.primary_markets = ["Residential", "Commercial"]
        
        if not self.current_analytics_tools:
            self.current_analytics_tools = ["Excel"]
    
    def add_data_source(self, source: str) -> None:
        """Add a data source to the client's profile"""
        if source not in self.data_sources:
            self.data_sources.append(source)
    
    def add_analytics_tool(self, tool: str) -> None:
        """Add an analytics tool to the client's current stack"""
        if tool not in self.current_analytics_tools:
            self.current_analytics_tools.append(tool)
    
    def get_client_profile(self) -> Dict:
        """Return a comprehensive client profile"""
        return {
            "basic_info": {
                "name": self.name,
                "location": self.location,
                "company": self.company,
                "industry": self.industry,
                "business_type": self.business_type
            },
            "contact": {
                "email": self.contact_email,
                "phone": self.contact_phone
            },
            "business_profile": {
                "company_size": self.company_size,
                "annual_revenue": self.annual_revenue,
                "primary_markets": self.primary_markets
            },
            "analytics_profile": {
                "current_tools": self.current_analytics_tools,
                "data_sources": self.data_sources,
                "experience_level": self.analytics_experience
            },
            "metadata": {
                "created_at": self.created_at.isoformat()
            }
        }
    
    def update_analytics_experience(self, level: str) -> None:
        """Update the client's analytics experience level"""
        valid_levels = ["Beginner", "Intermediate", "Advanced"]
        if level in valid_levels:
            self.analytics_experience = level
        else:
            raise ValueError(f"Invalid experience level. Must be one of: {valid_levels}")
    
    def __str__(self) -> str:
        return f"Client: {self.name} ({self.location}) - {self.business_type}"

