"""
Real Estate Analytics Framework

A comprehensive Python framework for handling real estate data analytics service requests,
including data platform setup, KPI identification, A/B testing, dashboard creation, and data analysis.
"""

__version__ = "1.0.0"
__author__ = "Real Estate Analytics Team"

from .core.service_request import ServiceRequest
from .core.client import Client
from .core.provider import ServiceProvider
from .data_platform.platform import DataPlatform
from .analytics.kpi_manager import KPIManager
from .analytics.ab_testing import ABTestManager
from .analytics.data_analyzer import DataAnalyzer
from .visualization.dashboard import DashboardBuilder

__all__ = [
    'ServiceRequest',
    'Client', 
    'ServiceProvider',
    'DataPlatform',
    'KPIManager',
    'ABTestManager',
    'DataAnalyzer',
    'DashboardBuilder'
]

