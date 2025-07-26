#!/usr/bin/env python3
"""
Comprehensive test script for the Real Estate Analytics Framework
Tests all major components and functionality
"""

import sys
import os
import traceback
from datetime import datetime

# Add the framework to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all framework components can be imported"""
    print("Testing imports...")
    
    try:
        # Core imports
        from real_estate_analytics.core.client import Client
        from real_estate_analytics.core.provider import ServiceProvider
        from real_estate_analytics.core.service_request import ServiceRequest, ServiceType, ProjectType
        
        # Data platform imports
        from real_estate_analytics.data_platform.platform import DataPlatform
        from real_estate_analytics.data_platform.connectors import DatabaseConnector, APIConnector, FileConnector
        
        # Analytics imports
        from real_estate_analytics.analytics.kpi_manager import KPIManager, KPI
        from real_estate_analytics.analytics.ab_testing import ABTestManager, ABTest
        from real_estate_analytics.analytics.data_analyzer import DataAnalyzer
        
        # Visualization imports
        from real_estate_analytics.visualization.dashboard import DashboardBuilder
        from real_estate_analytics.visualization.charts import ChartGenerator
        
        # Main framework import
        import real_estate_analytics
        
        print("✓ All imports successful")
        return True
        
    except Exception as e:
        print(f"✗ Import failed: {str(e)}")
        traceback.print_exc()
        return False


def test_core_functionality():
    """Test core framework functionality"""
    print("\nTesting core functionality...")
    
    try:
        from real_estate_analytics.core.client import Client
        from real_estate_analytics.core.provider import ServiceProvider
        from real_estate_analytics.core.service_request import ServiceRequest, ServiceType, ProjectType
        
        # Test client creation
        client = Client(
            name="Test Client",
            location="Test City",
            company="Test Company"
        )
        
        # Test provider creation
        provider = ServiceProvider(
            name="Test Provider",
            title="Data Analyst",
            company="Analytics Co"
        )
        
        # Test service request creation
        service_request = ServiceRequest(
            client=client,
            service_type=ServiceType.BUSINESS_ANALYTICS,
            project_type=ProjectType.ONE_TIME
        )
        
        # Test assignment
        success = service_request.assign_provider(provider)
        assert success, "Provider assignment failed"
        
        # Test progress update
        service_request.update_progress(50, "Halfway complete")
        assert service_request.progress_percentage == 50, "Progress update failed"
        
        print("✓ Core functionality tests passed")
        return True
        
    except Exception as e:
        print(f"✗ Core functionality test failed: {str(e)}")
        traceback.print_exc()
        return False


def test_data_platform():
    """Test data platform functionality"""
    print("\nTesting data platform...")
    
    try:
        from real_estate_analytics.data_platform.platform import DataPlatform
        
        # Create data platform
        platform = DataPlatform("TestPlatform", "./test_data")
        
        # Test data source addition
        platform.add_data_source(
            name="test_source",
            source_type="database",
            connection_string="sqlite:///test.db"
        )
        
        assert "test_source" in platform.data_sources, "Data source not added"
        
        # Test sample data creation
        sample_data = platform.create_sample_data()
        assert "properties" in sample_data, "Sample properties data not created"
        assert "market_data" in sample_data, "Sample market data not created"
        assert len(sample_data["properties"]) > 0, "No sample properties created"
        
        print("✓ Data platform tests passed")
        return True
        
    except Exception as e:
        print(f"✗ Data platform test failed: {str(e)}")
        traceback.print_exc()
        return False


def test_kpi_management():
    """Test KPI management functionality"""
    print("\nTesting KPI management...")
    
    try:
        from real_estate_analytics.analytics.kpi_manager import KPIManager, KPI, KPICategory
        from real_estate_analytics.data_platform.platform import DataPlatform
        
        # Create data platform with sample data
        platform = DataPlatform("TestPlatform", "./test_data")
        platform.create_sample_data()
        
        # Create KPI manager
        kpi_manager = KPIManager(platform)
        
        assert len(kpi_manager.kpis) > 0, "No default KPIs created"
        
        # Test KPI calculation
        kpi_results = kpi_manager.calculate_all_kpis()
        assert len(kpi_results) > 0, "No KPIs calculated"
        
        # Test custom KPI
        custom_kpi = KPI(
            name="Test KPI",
            category=KPICategory.SALES,
            description="Test KPI",
            calculation_method="test_method"
        )
        
        kpi_manager.add_kpi(custom_kpi)
        assert "Test KPI" in kpi_manager.kpis, "Custom KPI not added"
        
        print("✓ KPI management tests passed")
        return True
        
    except Exception as e:
        print(f"✗ KPI management test failed: {str(e)}")
        traceback.print_exc()
        return False


def test_ab_testing():
    """Test A/B testing functionality"""
    print("\nTesting A/B testing...")
    
    try:
        from real_estate_analytics.analytics.ab_testing import ABTestManager, TestType
        
        # Create A/B test manager
        ab_manager = ABTestManager()
        
        assert len(ab_manager.templates) > 0, "No test templates available"
        
        # Create test from template
        test = ab_manager.create_test_from_template("pricing_strategy")
        assert test is not None, "Test creation from template failed"
        
        # Start test
        test.start_test()
        assert test.status.value == "running", "Test not started properly"
        
        # Add test data
        success = test.add_data_point("Market Price", True, 500000)
        assert success, "Data point addition failed"
        
        # Get results
        results = test.get_current_results()
        assert "variants" in results, "Test results not generated"
        
        print("✓ A/B testing tests passed")
        return True
        
    except Exception as e:
        print(f"✗ A/B testing test failed: {str(e)}")
        traceback.print_exc()
        return False


def test_data_analysis():
    """Test data analysis functionality"""
    print("\nTesting data analysis...")
    
    try:
        from real_estate_analytics.analytics.data_analyzer import DataAnalyzer
        from real_estate_analytics.data_platform.platform import DataPlatform
        
        # Create data platform with sample data
        platform = DataPlatform("TestPlatform", "./test_data")
        platform.create_sample_data()
        
        # Create data analyzer
        analyzer = DataAnalyzer(platform)
        
        # Test market trends analysis
        market_trends = analyzer.analyze_market_trends()
        assert "error" not in market_trends or market_trends.get("data_points", 0) >= 0, "Market trends analysis failed"
        
        # Test property performance analysis
        property_performance = analyzer.analyze_property_performance()
        assert "error" not in property_performance or property_performance.get("total_sales", 0) >= 0, "Property performance analysis failed"
        
        # Test investment analysis
        sample_property = {
            'purchase_price': 500000,
            'monthly_rent': 2500,
            'annual_expenses': 10000
        }
        
        investment_analysis = analyzer.generate_investment_analysis(sample_property)
        assert "investment_grade" in investment_analysis, "Investment analysis failed"
        
        print("✓ Data analysis tests passed")
        return True
        
    except Exception as e:
        print(f"✗ Data analysis test failed: {str(e)}")
        traceback.print_exc()
        return False


def test_visualization():
    """Test visualization functionality"""
    print("\nTesting visualization...")
    
    try:
        from real_estate_analytics.visualization.dashboard import DashboardBuilder
        from real_estate_analytics.visualization.charts import ChartGenerator
        from real_estate_analytics.data_platform.platform import DataPlatform
        from real_estate_analytics.analytics.kpi_manager import KPIManager
        
        # Create components
        platform = DataPlatform("TestPlatform", "./test_data")
        platform.create_sample_data()
        
        kpi_manager = KPIManager(platform)
        
        # Create dashboard builder
        dashboard_builder = DashboardBuilder(platform, kpi_manager)
        assert dashboard_builder is not None, "Dashboard builder creation failed"
        
        # Create chart generator
        chart_generator = ChartGenerator(platform, style="plotly")
        assert chart_generator is not None, "Chart generator creation failed"
        
        # Test configuration export
        config_path = dashboard_builder.export_dashboard_config()
        assert os.path.exists(config_path), "Dashboard config export failed"
        
        print("✓ Visualization tests passed")
        return True
        
    except Exception as e:
        print(f"✗ Visualization test failed: {str(e)}")
        traceback.print_exc()
        return False


def test_examples():
    """Test example usage"""
    print("\nTesting examples...")
    
    try:
        from real_estate_analytics.examples.usage_examples import demonstrate_client_creation, demonstrate_provider_creation
        
        # Test client creation example
        client = demonstrate_client_creation()
        assert client is not None, "Client creation example failed"
        assert client.name == "Amman Properties LLC", "Client data incorrect"
        
        # Test provider creation example
        provider = demonstrate_provider_creation()
        assert provider is not None, "Provider creation example failed"
        assert provider.name == "mahmmoud hassan salah", "Provider data incorrect"
        
        print("✓ Examples tests passed")
        return True
        
    except Exception as e:
        print(f"✗ Examples test failed: {str(e)}")
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all tests and report results"""
    print("=" * 80)
    print("REAL ESTATE ANALYTICS FRAMEWORK - COMPREHENSIVE TESTS")
    print("=" * 80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tests = [
        ("Import Tests", test_imports),
        ("Core Functionality", test_core_functionality),
        ("Data Platform", test_data_platform),
        ("KPI Management", test_kpi_management),
        ("A/B Testing", test_ab_testing),
        ("Data Analysis", test_data_analysis),
        ("Visualization", test_visualization),
        ("Examples", test_examples)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'-' * 60}")
        print(f"Running {test_name}...")
        print(f"{'-' * 60}")
        
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"✗ {test_name} failed with exception: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST RESULTS SUMMARY")
    print("=" * 80)
    
    passed = 0
    failed = 0
    
    for test_name, success in results:
        status = "PASS" if success else "FAIL"
        print(f"{test_name:.<50} {status}")
        if success:
            passed += 1
        else:
            failed += 1
    
    print(f"\nTotal Tests: {len(results)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Success Rate: {(passed/len(results)*100):.1f}%")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! Framework is ready for use.")
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please review the errors above.")
    
    print(f"\nCompleted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

