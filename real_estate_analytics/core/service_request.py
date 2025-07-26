"""Service request management for real estate analytics services"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import uuid

from .client import Client
from .provider import ServiceProvider


class RequestStatus(Enum):
    """Service request status enumeration"""
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    ON_HOLD = "on_hold"


class ServiceType(Enum):
    """Available service types"""
    BUSINESS_ANALYTICS = "Business Analytics"
    DATA_PLATFORM_SETUP = "Data Platform Setup"
    KPI_IDENTIFICATION = "KPI Identification"
    AB_TESTING = "A/B Testing"
    DASHBOARD_CREATION = "Dashboard Creation"
    DATA_ANALYSIS = "Data Analysis"
    STRATEGIC_ANALYTICS = "Strategic Analytics"


class ProjectType(Enum):
    """Project type enumeration"""
    ONE_TIME = "One-time project"
    ONGOING = "Ongoing project"
    CONSULTATION = "Consultation"


@dataclass
class ServiceRequest:
    """Represents a service request for real estate analytics"""
    
    # Basic request information
    client: Client
    service_type: ServiceType
    project_type: ProjectType = ProjectType.ONE_TIME
    
    # Request details
    title: str = "Real Estate Analytics Request"
    description: str = ""
    requirements: List[str] = field(default_factory=list)
    deliverables: List[str] = field(default_factory=list)
    
    # Timeline
    deadline: Optional[datetime] = None
    estimated_duration_days: int = 7
    
    # Assignment and status
    assigned_provider: Optional[ServiceProvider] = None
    status: RequestStatus = RequestStatus.PENDING
    priority: str = "Medium"  # Low, Medium, High, Urgent
    
    # Scope of work details (based on the provided example)
    scope_details: Dict[str, Any] = field(default_factory=dict)
    
    # Metadata
    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    # Progress tracking
    progress_percentage: int = 0
    milestones: List[Dict[str, Any]] = field(default_factory=list)
    
    def __post_init__(self):
        """Initialize default values and set up scope details"""
        if not self.deadline:
            self.deadline = self.created_at + timedelta(days=self.estimated_duration_days)
        
        # Set up default scope details based on the provided example
        if not self.scope_details:
            self.scope_details = {
                "data_platform_setup": True,
                "kpi_identification": True,
                "ab_testing": True,
                "dashboard_creation": True,
                "data_visualization": True,
                "historical_analysis": True,
                "tools": ["SQL", "Python (Pandas, Plotly, Dash)", "Excel", "Power BI"],
                "deliverables": [
                    "Data platform tailored to business structure",
                    "Key business metrics identification",
                    "A/B test design and analysis",
                    "Interactive dashboards",
                    "Data visualization and storytelling",
                    "Historical data analysis and trends"
                ]
            }
        
        # Set up default requirements if not provided
        if not self.requirements:
            self.requirements = [
                "Setting up a data platform tailored to business structure",
                "Identifying key business metrics for real estate operations",
                "Designing and running A/B tests with analysis",
                "Creating clear, actionable dashboards",
                "Data visualization and storytelling capabilities",
                "Analyzing historical data to uncover trends"
            ]
        
        # Set up default deliverables if not provided
        if not self.deliverables:
            self.deliverables = [
                "Configured data platform",
                "KPI tracking system",
                "A/B test results and recommendations",
                "Interactive dashboards (Power BI/Tableau/Google Data Studio)",
                "Data visualization reports",
                "Strategic recommendations based on data analysis"
            ]
    
    def assign_provider(self, provider: ServiceProvider) -> bool:
        """Assign a service provider to the request"""
        if provider.can_handle_service(self.service_type.value):
            self.assigned_provider = provider
            self.status = RequestStatus.ASSIGNED
            self.updated_at = datetime.now()
            return True
        return False
    
    def update_status(self, new_status: RequestStatus, notes: str = "") -> None:
        """Update the request status"""
        self.status = new_status
        self.updated_at = datetime.now()
        
        # Add milestone for status change
        milestone = {
            "timestamp": self.updated_at,
            "status": new_status.value,
            "notes": notes
        }
        self.milestones.append(milestone)
    
    def update_progress(self, percentage: int, notes: str = "") -> None:
        """Update project progress percentage"""
        if 0 <= percentage <= 100:
            self.progress_percentage = percentage
            self.updated_at = datetime.now()
            
            # Add progress milestone
            milestone = {
                "timestamp": self.updated_at,
                "progress": percentage,
                "notes": notes
            }
            self.milestones.append(milestone)
            
            # Auto-update status based on progress
            if percentage == 100:
                self.status = RequestStatus.COMPLETED
            elif percentage > 0 and self.status == RequestStatus.ASSIGNED:
                self.status = RequestStatus.IN_PROGRESS
    
    def add_requirement(self, requirement: str) -> None:
        """Add a new requirement to the request"""
        if requirement not in self.requirements:
            self.requirements.append(requirement)
            self.updated_at = datetime.now()
    
    def add_deliverable(self, deliverable: str) -> None:
        """Add a new deliverable to the request"""
        if deliverable not in self.deliverables:
            self.deliverables.append(deliverable)
            self.updated_at = datetime.now()
    
    def is_overdue(self) -> bool:
        """Check if the request is overdue"""
        return datetime.now() > self.deadline and self.status != RequestStatus.COMPLETED
    
    def days_until_deadline(self) -> int:
        """Calculate days until deadline"""
        delta = self.deadline - datetime.now()
        return delta.days
    
    def get_request_summary(self) -> Dict[str, Any]:
        """Get a comprehensive summary of the request"""
        return {
            "request_id": self.request_id,
            "client": str(self.client),
            "service_type": self.service_type.value,
            "project_type": self.project_type.value,
            "status": self.status.value,
            "priority": self.priority,
            "progress": f"{self.progress_percentage}%",
            "assigned_provider": str(self.assigned_provider) if self.assigned_provider else None,
            "timeline": {
                "created": self.created_at.strftime("%Y-%m-%d %H:%M"),
                "deadline": self.deadline.strftime("%Y-%m-%d %H:%M"),
                "days_remaining": self.days_until_deadline(),
                "is_overdue": self.is_overdue()
            },
            "scope": self.scope_details,
            "requirements": self.requirements,
            "deliverables": self.deliverables,
            "milestones_count": len(self.milestones)
        }
    
    def get_detailed_report(self) -> Dict[str, Any]:
        """Get a detailed report including all milestones"""
        summary = self.get_request_summary()
        summary["milestones"] = [
            {
                "timestamp": m["timestamp"].strftime("%Y-%m-%d %H:%M"),
                "event": m.get("status", f"Progress: {m.get('progress', 'N/A')}%"),
                "notes": m.get("notes", "")
            }
            for m in self.milestones
        ]
        return summary
    
    def __str__(self) -> str:
        return f"Request {self.request_id[:8]} - {self.service_type.value} for {self.client.name} ({self.status.value})"

