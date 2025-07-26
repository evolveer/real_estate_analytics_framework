"""KPI management and tracking for real estate analytics"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import json


class KPICategory(Enum):
    """KPI categories for real estate analytics"""
    SALES = "Sales Performance"
    RENTAL = "Rental Performance"
    MARKET = "Market Analysis"
    FINANCIAL = "Financial Metrics"
    OPERATIONAL = "Operational Efficiency"
    CUSTOMER = "Customer Satisfaction"


class KPIFrequency(Enum):
    """KPI calculation frequency"""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"


@dataclass
class KPI:
    """Represents a Key Performance Indicator"""
    
    name: str
    category: KPICategory
    description: str
    calculation_method: str
    target_value: Optional[float] = None
    current_value: Optional[float] = None
    frequency: KPIFrequency = KPIFrequency.MONTHLY
    unit: str = ""
    
    # Historical data
    historical_values: List[Dict[str, Any]] = field(default_factory=list)
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    last_calculated: Optional[datetime] = None
    is_active: bool = True
    
    def add_value(self, value: float, date: datetime = None, notes: str = "") -> None:
        """Add a new value to the KPI history"""
        if date is None:
            date = datetime.now()
        
        self.historical_values.append({
            "date": date,
            "value": value,
            "notes": notes
        })
        
        self.current_value = value
        self.last_calculated = date
    
    def get_trend(self, periods: int = 5) -> str:
        """Calculate trend direction based on recent values"""
        if len(self.historical_values) < 2:
            return "insufficient_data"
        
        recent_values = self.historical_values[-periods:]
        values = [entry["value"] for entry in recent_values]
        
        if len(values) < 2:
            return "insufficient_data"
        
        # Simple linear trend
        slope = np.polyfit(range(len(values)), values, 1)[0]
        
        if slope > 0.05:
            return "increasing"
        elif slope < -0.05:
            return "decreasing"
        else:
            return "stable"
    
    def get_performance_status(self) -> str:
        """Get performance status compared to target"""
        if self.target_value is None or self.current_value is None:
            return "no_target"
        
        performance_ratio = self.current_value / self.target_value
        
        if performance_ratio >= 1.0:
            return "exceeding"
        elif performance_ratio >= 0.9:
            return "meeting"
        elif performance_ratio >= 0.7:
            return "below"
        else:
            return "poor"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert KPI to dictionary representation"""
        return {
            "name": self.name,
            "category": self.category.value,
            "description": self.description,
            "current_value": self.current_value,
            "target_value": self.target_value,
            "unit": self.unit,
            "frequency": self.frequency.value,
            "trend": self.get_trend(),
            "performance_status": self.get_performance_status(),
            "last_calculated": self.last_calculated.isoformat() if self.last_calculated else None,
            "historical_count": len(self.historical_values)
        }


class KPIManager:
    """Manages KPIs for real estate analytics"""
    
    def __init__(self, data_platform=None):
        self.data_platform = data_platform
        self.kpis: Dict[str, KPI] = {}
        self.calculation_functions: Dict[str, Callable] = {}
        
        # Initialize default real estate KPIs
        self._initialize_default_kpis()
        self._register_calculation_functions()
    
    def _initialize_default_kpis(self):
        """Initialize default real estate KPIs"""
        default_kpis = [
            # Sales Performance KPIs
            KPI(
                name="Average Days on Market",
                category=KPICategory.SALES,
                description="Average number of days properties stay on the market before selling",
                calculation_method="avg_days_on_market",
                target_value=45.0,
                unit="days",
                frequency=KPIFrequency.MONTHLY
            ),
            KPI(
                name="Sales Conversion Rate",
                category=KPICategory.SALES,
                description="Percentage of listings that result in sales",
                calculation_method="sales_conversion_rate",
                target_value=0.75,
                unit="%",
                frequency=KPIFrequency.MONTHLY
            ),
            KPI(
                name="Average Sale Price",
                category=KPICategory.SALES,
                description="Average sale price of properties",
                calculation_method="avg_sale_price",
                target_value=500000.0,
                unit="$",
                frequency=KPIFrequency.MONTHLY
            ),
            
            # Rental Performance KPIs
            KPI(
                name="Occupancy Rate",
                category=KPICategory.RENTAL,
                description="Percentage of rental properties that are occupied",
                calculation_method="occupancy_rate",
                target_value=0.95,
                unit="%",
                frequency=KPIFrequency.MONTHLY
            ),
            KPI(
                name="Average Rental Yield",
                category=KPICategory.RENTAL,
                description="Average rental yield across all properties",
                calculation_method="avg_rental_yield",
                target_value=0.06,
                unit="%",
                frequency=KPIFrequency.QUARTERLY
            ),
            
            # Market Analysis KPIs
            KPI(
                name="Price per Square Foot",
                category=KPICategory.MARKET,
                description="Average price per square foot in the market",
                calculation_method="price_per_sqft",
                target_value=250.0,
                unit="$/sqft",
                frequency=KPIFrequency.MONTHLY
            ),
            KPI(
                name="Market Inventory",
                category=KPICategory.MARKET,
                description="Total number of properties available in the market",
                calculation_method="market_inventory",
                target_value=150.0,
                unit="properties",
                frequency=KPIFrequency.WEEKLY
            ),
            
            # Financial KPIs
            KPI(
                name="Revenue Growth Rate",
                category=KPICategory.FINANCIAL,
                description="Monthly revenue growth rate",
                calculation_method="revenue_growth_rate",
                target_value=0.05,
                unit="%",
                frequency=KPIFrequency.MONTHLY
            ),
            KPI(
                name="Profit Margin",
                category=KPICategory.FINANCIAL,
                description="Profit margin on real estate transactions",
                calculation_method="profit_margin",
                target_value=0.15,
                unit="%",
                frequency=KPIFrequency.QUARTERLY
            )
        ]
        
        for kpi in default_kpis:
            self.kpis[kpi.name] = kpi
    
    def _register_calculation_functions(self):
        """Register calculation functions for KPIs"""
        self.calculation_functions = {
            "avg_days_on_market": self._calculate_avg_days_on_market,
            "sales_conversion_rate": self._calculate_sales_conversion_rate,
            "avg_sale_price": self._calculate_avg_sale_price,
            "occupancy_rate": self._calculate_occupancy_rate,
            "avg_rental_yield": self._calculate_avg_rental_yield,
            "price_per_sqft": self._calculate_price_per_sqft,
            "market_inventory": self._calculate_market_inventory,
            "revenue_growth_rate": self._calculate_revenue_growth_rate,
            "profit_margin": self._calculate_profit_margin
        }
    
    def add_kpi(self, kpi: KPI) -> None:
        """Add a new KPI to the manager"""
        self.kpis[kpi.name] = kpi
    
    def remove_kpi(self, kpi_name: str) -> bool:
        """Remove a KPI from the manager"""
        if kpi_name in self.kpis:
            self.kpis[kpi_name].is_active = False
            return True
        return False
    
    def calculate_kpi(self, kpi_name: str, date: datetime = None) -> Optional[float]:
        """Calculate a specific KPI value"""
        if kpi_name not in self.kpis:
            return None
        
        kpi = self.kpis[kpi_name]
        if kpi.calculation_method not in self.calculation_functions:
            return None
        
        try:
            value = self.calculation_functions[kpi.calculation_method](date)
            if value is not None:
                kpi.add_value(value, date or datetime.now())
            return value
        except Exception as e:
            print(f"Error calculating KPI {kpi_name}: {e}")
            return None
    
    def calculate_all_kpis(self, date: datetime = None) -> Dict[str, float]:
        """Calculate all active KPIs"""
        results = {}
        for kpi_name, kpi in self.kpis.items():
            if kpi.is_active:
                value = self.calculate_kpi(kpi_name, date)
                if value is not None:
                    results[kpi_name] = value
        return results
    
    def get_kpi_dashboard(self) -> Dict[str, Any]:
        """Get KPI dashboard data"""
        dashboard = {
            "summary": {
                "total_kpis": len(self.kpis),
                "active_kpis": len([k for k in self.kpis.values() if k.is_active]),
                "last_updated": datetime.now().isoformat()
            },
            "categories": {},
            "kpis": {}
        }
        
        # Group KPIs by category
        for kpi_name, kpi in self.kpis.items():
            if kpi.is_active:
                category = kpi.category.value
                if category not in dashboard["categories"]:
                    dashboard["categories"][category] = []
                
                dashboard["categories"][category].append(kpi.to_dict())
                dashboard["kpis"][kpi_name] = kpi.to_dict()
        
        return dashboard
    
    def export_kpi_data(self, file_path: str = None) -> str:
        """Export KPI data to JSON file"""
        if not file_path:
            file_path = f"kpi_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        export_data = {
            "export_date": datetime.now().isoformat(),
            "kpis": {name: kpi.to_dict() for name, kpi in self.kpis.items()},
            "historical_data": {
                name: [
                    {
                        "date": entry["date"].isoformat(),
                        "value": entry["value"],
                        "notes": entry["notes"]
                    }
                    for entry in kpi.historical_values
                ]
                for name, kpi in self.kpis.items()
            }
        }
        
        with open(file_path, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        return file_path
    
    # KPI Calculation Methods
    def _calculate_avg_days_on_market(self, date: datetime = None) -> Optional[float]:
        """Calculate average days on market"""
        if not self.data_platform:
            return None
        
        query = """
        SELECT AVG(days_on_market) as avg_days
        FROM properties 
        WHERE sale_date IS NOT NULL AND days_on_market IS NOT NULL
        """
        
        if date:
            query += f" AND sale_date >= '{(date - timedelta(days=30)).date()}'"
        
        df = self.data_platform.load_data("default_database", query=query)
        return float(df.iloc[0]['avg_days']) if not df.empty and df.iloc[0]['avg_days'] else None
    
    def _calculate_sales_conversion_rate(self, date: datetime = None) -> Optional[float]:
        """Calculate sales conversion rate"""
        if not self.data_platform:
            return None
        
        query = """
        SELECT 
            COUNT(*) as total_listings,
            COUNT(sale_date) as sold_listings
        FROM properties
        """
        
        if date:
            query += f" WHERE listing_date >= '{(date - timedelta(days=30)).date()}'"
        
        df = self.data_platform.load_data("default_database", query=query)
        if not df.empty and df.iloc[0]['total_listings'] > 0:
            return float(df.iloc[0]['sold_listings']) / float(df.iloc[0]['total_listings'])
        return None
    
    def _calculate_avg_sale_price(self, date: datetime = None) -> Optional[float]:
        """Calculate average sale price"""
        if not self.data_platform:
            return None
        
        query = """
        SELECT AVG(sale_price) as avg_price
        FROM properties 
        WHERE sale_price IS NOT NULL
        """
        
        if date:
            query += f" AND sale_date >= '{(date - timedelta(days=30)).date()}'"
        
        df = self.data_platform.load_data("default_database", query=query)
        return float(df.iloc[0]['avg_price']) if not df.empty and df.iloc[0]['avg_price'] else None
    
    def _calculate_occupancy_rate(self, date: datetime = None) -> Optional[float]:
        """Calculate occupancy rate for rental properties"""
        if not self.data_platform:
            return None
        
        query = """
        SELECT 
            COUNT(*) as total_rentals,
            COUNT(CASE WHEN occupancy_status = 'occupied' THEN 1 END) as occupied_rentals
        FROM rental_properties
        WHERE lease_end > date('now') OR lease_end IS NULL
        """
        
        df = self.data_platform.load_data("default_database", query=query)
        if not df.empty and df.iloc[0]['total_rentals'] > 0:
            return float(df.iloc[0]['occupied_rentals']) / float(df.iloc[0]['total_rentals'])
        return None
    
    def _calculate_avg_rental_yield(self, date: datetime = None) -> Optional[float]:
        """Calculate average rental yield"""
        if not self.data_platform:
            return None
        
        query = """
        SELECT AVG(rental_yield) as avg_yield
        FROM market_data
        WHERE rental_yield IS NOT NULL
        """
        
        if date:
            query += f" AND date >= '{(date - timedelta(days=90)).date()}'"
        
        df = self.data_platform.load_data("default_database", query=query)
        return float(df.iloc[0]['avg_yield']) / 100 if not df.empty and df.iloc[0]['avg_yield'] else None
    
    def _calculate_price_per_sqft(self, date: datetime = None) -> Optional[float]:
        """Calculate average price per square foot"""
        if not self.data_platform:
            return None
        
        query = """
        SELECT AVG(price_per_sqft) as avg_price_sqft
        FROM market_data
        WHERE price_per_sqft IS NOT NULL
        """
        
        if date:
            query += f" AND date >= '{(date - timedelta(days=30)).date()}'"
        
        df = self.data_platform.load_data("default_database", query=query)
        return float(df.iloc[0]['avg_price_sqft']) if not df.empty and df.iloc[0]['avg_price_sqft'] else None
    
    def _calculate_market_inventory(self, date: datetime = None) -> Optional[float]:
        """Calculate current market inventory"""
        if not self.data_platform:
            return None
        
        query = """
        SELECT AVG(inventory_count) as avg_inventory
        FROM market_data
        WHERE inventory_count IS NOT NULL
        """
        
        if date:
            query += f" AND date >= '{(date - timedelta(days=7)).date()}'"
        
        df = self.data_platform.load_data("default_database", query=query)
        return float(df.iloc[0]['avg_inventory']) if not df.empty and df.iloc[0]['avg_inventory'] else None
    
    def _calculate_revenue_growth_rate(self, date: datetime = None) -> Optional[float]:
        """Calculate revenue growth rate"""
        # This would typically connect to financial data
        # For now, return a placeholder calculation
        return 0.05  # 5% growth rate
    
    def _calculate_profit_margin(self, date: datetime = None) -> Optional[float]:
        """Calculate profit margin"""
        # This would typically connect to financial data
        # For now, return a placeholder calculation
        return 0.15  # 15% profit margin

