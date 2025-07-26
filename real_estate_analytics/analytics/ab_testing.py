"""A/B testing framework for real estate analytics"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json
from scipy import stats
import uuid


class TestStatus(Enum):
    """A/B test status enumeration"""
    DRAFT = "draft"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TestType(Enum):
    """A/B test types for real estate"""
    PRICING_STRATEGY = "Pricing Strategy"
    MARKETING_CAMPAIGN = "Marketing Campaign"
    LISTING_PRESENTATION = "Listing Presentation"
    WEBSITE_DESIGN = "Website Design"
    EMAIL_CAMPAIGN = "Email Campaign"
    PROPERTY_STAGING = "Property Staging"


@dataclass
class TestVariant:
    """Represents a variant in an A/B test"""
    
    name: str
    description: str
    traffic_allocation: float  # Percentage of traffic (0.0 to 1.0)
    
    # Metrics tracking
    participants: int = 0
    conversions: int = 0
    total_value: float = 0.0
    
    # Configuration
    configuration: Dict[str, Any] = field(default_factory=dict)
    
    def add_participant(self, converted: bool = False, value: float = 0.0) -> None:
        """Add a participant to this variant"""
        self.participants += 1
        if converted:
            self.conversions += 1
            self.total_value += value
    
    def get_conversion_rate(self) -> float:
        """Calculate conversion rate for this variant"""
        return self.conversions / self.participants if self.participants > 0 else 0.0
    
    def get_average_value(self) -> float:
        """Calculate average value per participant"""
        return self.total_value / self.participants if self.participants > 0 else 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert variant to dictionary"""
        return {
            "name": self.name,
            "description": self.description,
            "traffic_allocation": self.traffic_allocation,
            "participants": self.participants,
            "conversions": self.conversions,
            "conversion_rate": self.get_conversion_rate(),
            "total_value": self.total_value,
            "average_value": self.get_average_value(),
            "configuration": self.configuration
        }


@dataclass
class ABTest:
    """Represents an A/B test for real estate analytics"""
    
    name: str
    description: str
    test_type: TestType
    hypothesis: str
    
    # Test configuration
    variants: List[TestVariant] = field(default_factory=list)
    primary_metric: str = "conversion_rate"
    secondary_metrics: List[str] = field(default_factory=list)
    
    # Test parameters
    confidence_level: float = 0.95
    minimum_sample_size: int = 100
    minimum_effect_size: float = 0.05  # 5% minimum detectable effect
    
    # Timeline
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    planned_duration_days: int = 30
    
    # Status and results
    status: TestStatus = TestStatus.DRAFT
    results: Dict[str, Any] = field(default_factory=dict)
    
    # Metadata
    test_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    created_by: str = ""
    template: str = "custom"  # Template used to create the test
    
    def add_variant(self, variant: TestVariant) -> None:
        """Add a variant to the test"""
        # Ensure traffic allocations don't exceed 100%
        total_allocation = sum(v.traffic_allocation for v in self.variants) + variant.traffic_allocation
        if total_allocation > 1.0:
            raise ValueError("Total traffic allocation cannot exceed 100%")
        
        self.variants.append(variant)
    
    def start_test(self) -> bool:
        """Start the A/B test"""
        if len(self.variants) < 2:
            raise ValueError("Test must have at least 2 variants")
        
        # Validate traffic allocation
        total_allocation = sum(v.traffic_allocation for v in self.variants)
        if abs(total_allocation - 1.0) > 0.01:
            raise ValueError("Total traffic allocation must equal 100%")
        
        self.status = TestStatus.RUNNING
        self.start_date = datetime.now()
        self.end_date = self.start_date + timedelta(days=self.planned_duration_days)
        return True
    
    def pause_test(self) -> None:
        """Pause the A/B test"""
        if self.status == TestStatus.RUNNING:
            self.status = TestStatus.PAUSED
    
    def resume_test(self) -> None:
        """Resume the A/B test"""
        if self.status == TestStatus.PAUSED:
            self.status = TestStatus.RUNNING
    
    def stop_test(self) -> None:
        """Stop the A/B test and calculate final results"""
        self.status = TestStatus.COMPLETED
        self.end_date = datetime.now()
        self.results = self._calculate_results()
    
    def add_data_point(self, variant_name: str, converted: bool = False, value: float = 0.0) -> bool:
        """Add a data point to a specific variant"""
        for variant in self.variants:
            if variant.name == variant_name:
                variant.add_participant(converted, value)
                return True
        return False
    
    def get_current_results(self) -> Dict[str, Any]:
        """Get current test results without stopping the test"""
        return self._calculate_results()
    
    def _calculate_results(self) -> Dict[str, Any]:
        """Calculate statistical results for the test"""
        if len(self.variants) < 2:
            return {"error": "Insufficient variants for analysis"}
        
        results = {
            "test_id": self.test_id,
            "test_name": self.name,
            "status": self.status.value,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "total_participants": sum(v.participants for v in self.variants),
            "variants": [v.to_dict() for v in self.variants],
            "statistical_analysis": {}
        }
        
        # Perform statistical analysis
        if self.primary_metric == "conversion_rate":
            results["statistical_analysis"] = self._analyze_conversion_rates()
        elif self.primary_metric == "average_value":
            results["statistical_analysis"] = self._analyze_average_values()
        
        # Determine winner
        results["winner"] = self._determine_winner()
        results["confidence_level"] = self.confidence_level
        results["is_significant"] = results["statistical_analysis"].get("is_significant", False)
        
        return results
    
    def _analyze_conversion_rates(self) -> Dict[str, Any]:
        """Analyze conversion rates between variants"""
        if len(self.variants) != 2:
            return {"error": "Conversion rate analysis currently supports only 2 variants"}
        
        variant_a, variant_b = self.variants[0], self.variants[1]
        
        # Check for sufficient sample size
        if variant_a.participants < self.minimum_sample_size or variant_b.participants < self.minimum_sample_size:
            return {
                "error": "Insufficient sample size",
                "required_sample_size": self.minimum_sample_size,
                "variant_a_size": variant_a.participants,
                "variant_b_size": variant_b.participants
            }
        
        # Calculate conversion rates
        rate_a = variant_a.get_conversion_rate()
        rate_b = variant_b.get_conversion_rate()
        
        # Perform two-proportion z-test
        count_a, count_b = variant_a.conversions, variant_b.conversions
        n_a, n_b = variant_a.participants, variant_b.participants
        
        # Pooled proportion
        p_pool = (count_a + count_b) / (n_a + n_b)
        
        # Standard error
        se = np.sqrt(p_pool * (1 - p_pool) * (1/n_a + 1/n_b))
        
        # Z-score
        z_score = (rate_a - rate_b) / se if se > 0 else 0
        
        # P-value (two-tailed)
        p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))
        
        # Effect size (relative difference)
        effect_size = (rate_b - rate_a) / rate_a if rate_a > 0 else 0
        
        # Confidence interval for difference
        alpha = 1 - self.confidence_level
        z_critical = stats.norm.ppf(1 - alpha/2)
        margin_of_error = z_critical * se
        
        return {
            "variant_a": {
                "name": variant_a.name,
                "conversion_rate": rate_a,
                "participants": n_a,
                "conversions": count_a
            },
            "variant_b": {
                "name": variant_b.name,
                "conversion_rate": rate_b,
                "participants": n_b,
                "conversions": count_b
            },
            "difference": rate_b - rate_a,
            "relative_difference": effect_size,
            "z_score": z_score,
            "p_value": p_value,
            "is_significant": p_value < (1 - self.confidence_level),
            "confidence_interval": {
                "lower": (rate_b - rate_a) - margin_of_error,
                "upper": (rate_b - rate_a) + margin_of_error
            }
        }
    
    def _analyze_average_values(self) -> Dict[str, Any]:
        """Analyze average values between variants using t-test"""
        if len(self.variants) != 2:
            return {"error": "Average value analysis currently supports only 2 variants"}
        
        variant_a, variant_b = self.variants[0], self.variants[1]
        
        # For simplicity, assume normal distribution
        # In practice, you'd want to collect individual data points
        avg_a = variant_a.get_average_value()
        avg_b = variant_b.get_average_value()
        
        # Placeholder for t-test (would need individual data points for proper analysis)
        return {
            "variant_a": {
                "name": variant_a.name,
                "average_value": avg_a,
                "participants": variant_a.participants
            },
            "variant_b": {
                "name": variant_b.name,
                "average_value": avg_b,
                "participants": variant_b.participants
            },
            "difference": avg_b - avg_a,
            "relative_difference": (avg_b - avg_a) / avg_a if avg_a > 0 else 0,
            "note": "Full t-test analysis requires individual data points"
        }
    
    def _determine_winner(self) -> Dict[str, Any]:
        """Determine the winning variant"""
        if not self.variants:
            return {"winner": None, "reason": "No variants"}
        
        if self.primary_metric == "conversion_rate":
            best_variant = max(self.variants, key=lambda v: v.get_conversion_rate())
            best_rate = best_variant.get_conversion_rate()
            
            return {
                "winner": best_variant.name,
                "metric": "conversion_rate",
                "value": best_rate,
                "improvement": self._calculate_improvement(best_variant)
            }
        
        elif self.primary_metric == "average_value":
            best_variant = max(self.variants, key=lambda v: v.get_average_value())
            best_value = best_variant.get_average_value()
            
            return {
                "winner": best_variant.name,
                "metric": "average_value",
                "value": best_value,
                "improvement": self._calculate_improvement(best_variant)
            }
        
        return {"winner": None, "reason": "Unknown metric"}
    
    def _calculate_improvement(self, winning_variant: TestVariant) -> float:
        """Calculate improvement of winning variant over others"""
        if self.primary_metric == "conversion_rate":
            other_rates = [v.get_conversion_rate() for v in self.variants if v != winning_variant]
            if other_rates:
                baseline = max(other_rates)
                winner_rate = winning_variant.get_conversion_rate()
                return (winner_rate - baseline) / baseline if baseline > 0 else 0
        
        return 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert test to dictionary"""
        return {
            "test_id": self.test_id,
            "name": self.name,
            "description": self.description,
            "test_type": self.test_type.value,
            "hypothesis": self.hypothesis,
            "status": self.status.value,
            "primary_metric": self.primary_metric,
            "confidence_level": self.confidence_level,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "variants": [v.to_dict() for v in self.variants],
            "created_at": self.created_at.isoformat(),
            "created_by": self.created_by
        }


class ABTestManager:
    """Manages A/B tests for real estate analytics"""
    
    def __init__(self, data_platform=None):
        self.data_platform = data_platform
        self.tests: Dict[str, ABTest] = {}
        self.templates: Dict[str, Dict[str, Any]] = {}
        
        # Initialize test templates
        self._initialize_test_templates()
    
    def _initialize_test_templates(self):
        """Initialize common A/B test templates for real estate"""
        self.templates = {
            "pricing_strategy": {
                "name": "Pricing Strategy Test",
                "description": "Test different pricing strategies for property listings",
                "test_type": TestType.PRICING_STRATEGY,
                "primary_metric": "conversion_rate",
                "secondary_metrics": ["average_value", "time_to_sale"],
                "variants": [
                    {
                        "name": "Market Price",
                        "description": "Price at market value",
                        "traffic_allocation": 0.5
                    },
                    {
                        "name": "Premium Price",
                        "description": "Price 5% above market value",
                        "traffic_allocation": 0.5
                    }
                ]
            },
            "listing_photos": {
                "name": "Listing Photos Test",
                "description": "Test different photo styles for property listings",
                "test_type": TestType.LISTING_PRESENTATION,
                "primary_metric": "conversion_rate",
                "secondary_metrics": ["viewing_time", "inquiry_rate"],
                "variants": [
                    {
                        "name": "Professional Photos",
                        "description": "High-quality professional photography",
                        "traffic_allocation": 0.5
                    },
                    {
                        "name": "Staged Photos",
                        "description": "Professional photos with staging",
                        "traffic_allocation": 0.5
                    }
                ]
            },
            "email_campaign": {
                "name": "Email Campaign Test",
                "description": "Test different email marketing approaches",
                "test_type": TestType.EMAIL_CAMPAIGN,
                "primary_metric": "conversion_rate",
                "secondary_metrics": ["open_rate", "click_rate"],
                "variants": [
                    {
                        "name": "Standard Email",
                        "description": "Standard property listing email",
                        "traffic_allocation": 0.5
                    },
                    {
                        "name": "Personalized Email",
                        "description": "Personalized email with buyer preferences",
                        "traffic_allocation": 0.5
                    }
                ]
            }
        }
    
    def create_test_from_template(self, template_name: str, test_name: str = None, **kwargs) -> Optional[ABTest]:
        """Create a new test from a template"""
        if template_name not in self.templates:
            return None
        
        template = self.templates[template_name]
        
        test = ABTest(
            name=test_name or template["name"],
            description=template["description"],
            test_type=template["test_type"],
            hypothesis=kwargs.get("hypothesis", ""),
            primary_metric=template["primary_metric"],
            secondary_metrics=template["secondary_metrics"],
            template=template_name
        )
        
        # Add variants from template
        for variant_config in template["variants"]:
            variant = TestVariant(
                name=variant_config["name"],
                description=variant_config["description"],
                traffic_allocation=variant_config["traffic_allocation"]
            )
            test.add_variant(variant)
        
        self.tests[test.test_id] = test
        return test
    
    def create_custom_test(self, name: str, description: str, test_type: TestType, hypothesis: str) -> ABTest:
        """Create a custom A/B test"""
        test = ABTest(
            name=name,
            description=description,
            test_type=test_type,
            hypothesis=hypothesis
        )
        
        self.tests[test.test_id] = test
        return test
    
    def get_test(self, test_id: str) -> Optional[ABTest]:
        """Get a test by ID"""
        return self.tests.get(test_id)
    
    def list_tests(self, status: TestStatus = None) -> List[ABTest]:
        """List all tests, optionally filtered by status"""
        if status:
            return [test for test in self.tests.values() if test.status == status]
        return list(self.tests.values())
    
    def get_test_summary(self) -> Dict[str, Any]:
        """Get summary of all tests"""
        total_tests = len(self.tests)
        status_counts = {}
        
        for test in self.tests.values():
            status = test.status.value
            status_counts[status] = status_counts.get(status, 0) + 1
        
        return {
            "total_tests": total_tests,
            "status_breakdown": status_counts,
            "templates_available": list(self.templates.keys()),
            "last_updated": datetime.now().isoformat()
        }
    
    def export_test_results(self, test_id: str, file_path: str = None) -> Optional[str]:
        """Export test results to JSON file"""
        test = self.get_test(test_id)
        if not test:
            return None
        
        if not file_path:
            file_path = f"test_results_{test_id[:8]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        results = test.get_current_results()
        
        with open(file_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        return file_path
