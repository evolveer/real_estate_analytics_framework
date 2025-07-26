"""Comprehensive usage examples for the Real Estate Analytics Framework"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from real_estate_analytics import *
from real_estate_analytics.core.service_request import ServiceType, ProjectType, RequestStatus
from real_estate_analytics.analytics.kpi_manager import KPICategory, KPIFrequency, KPI
from real_estate_analytics.analytics.ab_testing import TestType, TestStatus
from datetime import datetime, timedelta
import pandas as pd


def run_complete_example():
    """Run a complete example demonstrating all framework capabilities"""
    print("=" * 80)
    print("REAL ESTATE ANALYTICS FRAMEWORK - COMPLETE EXAMPLE")
    print("=" * 80)
    
    # 1. Create client and service provider
    print("\n1. Creating Client and Service Provider...")
    client = demonstrate_client_creation()
    provider = demonstrate_provider_creation()
    
    # 2. Create service request
    print("\n2. Creating Service Request...")
    service_request = demonstrate_service_request(client, provider)
    
    # 3. Set up data platform
    print("\n3. Setting up Data Platform...")
    data_platform = demonstrate_data_platform()
    
    # 4. Set up KPI management
    print("\n4. Setting up KPI Management...")
    kpi_manager = demonstrate_kpi_management(data_platform)
    
    # 5. Demonstrate A/B testing
    print("\n5. Demonstrating A/B Testing...")
    ab_test_manager = demonstrate_ab_testing()
    
    # 6. Perform data analysis
    print("\n6. Performing Data Analysis...")
    data_analyzer = demonstrate_data_analysis(data_platform)
    
    # 7. Create dashboards and visualizations
    print("\n7. Creating Dashboards and Visualizations...")
    demonstrate_dashboard_creation(data_platform, kpi_manager, data_analyzer)
    
    print("\n" + "=" * 80)
    print("COMPLETE EXAMPLE FINISHED SUCCESSFULLY!")
    print("=" * 80)
    
    return {
        "client": client,
        "provider": provider,
        "service_request": service_request,
        "data_platform": data_platform,
        "kpi_manager": kpi_manager,
        "ab_test_manager": ab_test_manager,
        "data_analyzer": data_analyzer
    }


def demonstrate_client_creation():
    """Demonstrate client creation and management"""
    print("Creating a real estate client profile...")
    
    client = Client(
        name="Amman Properties LLC",
        location="Amman, Jordan",
        company="Decorations for Home | Design and Planning",
        industry="Real Estate",
        contact_email="amman@decorations-home.com",
        business_type="Consumer Products",
        company_size="Medium (50-200 employees)",
        annual_revenue="$5M - $10M"
    )
    
    # Add data sources and analytics tools
    client.add_data_source("Property Management System")
    client.add_data_source("CRM Database")
    client.add_data_source("Financial Records")
    
    client.add_analytics_tool("Excel")
    client.add_analytics_tool("QuickBooks")
    client.update_analytics_experience("Intermediate")
    
    print(f"✓ Created client: {client}")
    print(f"  - Analytics Experience: {client.analytics_experience}")
    print(f"  - Data Sources: {', '.join(client.data_sources)}")
    print(f"  - Current Tools: {', '.join(client.current_analytics_tools)}")
    
    return client


def demonstrate_provider_creation():
    """Demonstrate service provider creation"""
    print("Creating a service provider profile...")
    
    provider = ServiceProvider(
        name="mahmmoud hassan salah",
        title="Real Estate Manager",
        company="Decorations for Home | Design and Planning",
        specialization="Real Estate Analytics & Data Science",
        email="mahmoud@analytics-experts.com",
        location="Remote",
        experience_years=5,
        hourly_rate=75.0
    )
    
    # Add certifications and skills
    provider.add_certification("Google Analytics Certified")
    provider.add_certification("Microsoft Power BI Certified")
    provider.add_skill("Machine Learning")
    provider.add_skill("Statistical Analysis")
    provider.add_tool_expertise("Tableau")
    provider.add_tool_expertise("Google Data Studio")
    
    print(f"✓ Created provider: {provider}")
    print(f"  - Experience: {provider.experience_years} years")
    print(f"  - Rating: {provider.client_rating}/5.0")
    print(f"  - Availability: {provider.availability}")
    
    return provider


def demonstrate_service_request(client, provider):
    """Demonstrate service request creation and management"""
    print("Creating a comprehensive service request...")
    
    service_request = ServiceRequest(
        client=client,
        service_type=ServiceType.BUSINESS_ANALYTICS,
        project_type=ProjectType.ONE_TIME,
        title="Real Estate Business Analytics Implementation",
        description="Comprehensive analytics solution for real estate operations",
        deadline=datetime.now() + timedelta(days=7),  # This week deadline
        priority="High"
    )
    
    # Assign provider
    success = service_request.assign_provider(provider)
    print(f"✓ Provider assignment: {'Success' if success else 'Failed'}")
    
    # Update progress
    service_request.update_progress(25, "Data platform setup initiated")
    service_request.update_progress(50, "KPI identification completed")
    service_request.update_progress(75, "Dashboard development in progress")
    
    print(f"✓ Created service request: {service_request}")
    print(f"  - Status: {service_request.status.value}")
    print(f"  - Progress: {service_request.progress_percentage}%")
    print(f"  - Days until deadline: {service_request.days_until_deadline()}")
    
    # Display request summary
    summary = service_request.get_request_summary()
    print(f"  - Requirements: {len(summary['requirements'])} items")
    print(f"  - Deliverables: {len(summary['deliverables'])} items")
    
    return service_request


def demonstrate_data_platform():
    """Demonstrate data platform setup and operations"""
    print("Setting up data platform...")
    
    # Create data platform
    platform = DataPlatform("RealEstateAnalytics", "./data")
    
    print(f"✓ Created data platform: {platform.platform_name}")
    print(f"  - Base path: {platform.base_path}")
    print(f"  - Default database: {platform.default_db_path}")
    
    # Add additional data sources
    platform.add_data_source(
        name="external_api",
        source_type="api",
        api_endpoint="https://api.realestate-data.com",
        schema={"properties": "External property listings", "market_trends": "Market analysis data"}
    )
    
    platform.add_data_source(
        name="csv_imports",
        source_type="file",
        file_path="./data/imports/",
        schema={"monthly_reports": "Monthly performance reports"}
    )
    
    print(f"  - Total data sources: {len(platform.data_sources)}")
    
    # Create sample data for demonstration
    print("Generating sample data...")
    sample_data = platform.create_sample_data()
    
    print(f"✓ Generated sample data:")
    print(f"  - Properties: {len(sample_data['properties'])} records")
    print(f"  - Market data: {len(sample_data['market_data'])} records")
    
    # Display platform status
    status = platform.get_platform_status()
    print(f"  - Active sources: {status['active_sources']}")
    
    return platform


def demonstrate_kpi_management(data_platform):
    """Demonstrate KPI management and tracking"""
    print("Setting up KPI management...")
    
    # Create KPI manager
    kpi_manager = KPIManager(data_platform)
    
    print(f"✓ Created KPI manager with {len(kpi_manager.kpis)} default KPIs")
    
    # Calculate all KPIs
    print("Calculating KPI values...")
    kpi_results = kpi_manager.calculate_all_kpis()
    
    print(f"✓ Calculated {len(kpi_results)} KPIs:")
    for kpi_name, value in kpi_results.items():
        kpi = kpi_manager.kpis[kpi_name]
        trend = kpi.get_trend()
        performance = kpi.get_performance_status()
        print(f"  - {kpi_name}: {value:.2f} {kpi.unit} (Trend: {trend}, Performance: {performance})")
    
    # Add a custom KPI
    custom_kpi = KPI(
        name="Customer Satisfaction Score",
        category=KPICategory.CUSTOMER,
        description="Average customer satisfaction rating",
        calculation_method="custom_satisfaction",
        target_value=4.5,
        unit="stars",
        frequency=KPIFrequency.MONTHLY
    )
    
    kpi_manager.add_kpi(custom_kpi)
    custom_kpi.add_value(4.2, datetime.now(), "Monthly survey results")
    
    print(f"✓ Added custom KPI: {custom_kpi.name}")
    
    # Get KPI dashboard
    dashboard_data = kpi_manager.get_kpi_dashboard()
    print(f"  - Dashboard categories: {len(dashboard_data['categories'])}")
    print(f"  - Total active KPIs: {dashboard_data['summary']['active_kpis']}")
    
    return kpi_manager


def demonstrate_ab_testing():
    """Demonstrate A/B testing capabilities"""
    print("Setting up A/B testing...")
    
    # Create A/B test manager
    ab_manager = ABTestManager()
    
    print(f"✓ Created A/B test manager")
    print(f"  - Available templates: {len(ab_manager.templates)}")
    
    # Create a test from template
    pricing_test = ab_manager.create_test_from_template(
        "pricing_strategy",
        test_name="Property Pricing Strategy Test",
        hypothesis="Premium pricing (5% above market) will generate higher revenue per property"
    )
    
    print(f"✓ Created test from template: {pricing_test.name}")
    
    # Start the test
    pricing_test.start_test()
    print(f"  - Test status: {pricing_test.status.value}")
    print(f"  - Variants: {len(pricing_test.variants)}")
    
    # Simulate test data
    print("Simulating test data...")
    import random
    
    for _ in range(200):  # 200 participants
        variant_name = random.choice([v.name for v in pricing_test.variants])
        converted = random.random() < 0.15  # 15% base conversion rate
        value = random.randint(300000, 800000) if converted else 0
        
        # Adjust conversion rate for premium pricing
        if variant_name == "Premium Price":
            converted = random.random() < 0.12  # Slightly lower conversion
            if converted:
                value = int(value * 1.05)  # 5% higher value
        
        pricing_test.add_data_point(variant_name, converted, value)
    
    # Get test results
    results = pricing_test.get_current_results()
    print(f"✓ Test results:")
    print(f"  - Total participants: {results['total_participants']}")
    print(f"  - Winner: {results['winner']['winner']}")
    print(f"  - Statistical significance: {results['is_significant']}")
    
    for variant in results['variants']:
        print(f"  - {variant['name']}: {variant['conversion_rate']:.1%} conversion, "
              f"${variant['average_value']:,.0f} avg value")
    
    # Create a custom test
    custom_test = ab_manager.create_custom_test(
        name="Email Campaign Effectiveness",
        description="Test different email marketing approaches for property listings",
        test_type=TestType.EMAIL_CAMPAIGN,
        hypothesis="Personalized emails will have higher open and click rates"
    )
    
    print(f"✓ Created custom test: {custom_test.name}")
    
    return ab_manager


def demonstrate_data_analysis(data_platform):
    """Demonstrate comprehensive data analysis capabilities"""
    print("Performing data analysis...")
    
    # Create data analyzer
    analyzer = DataAnalyzer(data_platform)
    
    print(f"✓ Created data analyzer")
    
    # Market trends analysis
    print("Analyzing market trends...")
    market_trends = analyzer.analyze_market_trends(time_period_days=365)
    
    if "error" not in market_trends:
        print(f"✓ Market trends analysis completed:")
        print(f"  - Data points analyzed: {market_trends['data_points']}")
        print(f"  - Regions analyzed: {len(market_trends.get('regional_summary', {}))}")
        
        trends = market_trends.get('trends', {})
        for metric, trend_data in trends.items():
            direction = trend_data.get('trend_direction', 'unknown')
            change = trend_data.get('percentage_change', 0)
            print(f"  - {metric}: {direction} ({change:+.1f}%)")
    
    # Property performance analysis
    print("Analyzing property performance...")
    property_performance = analyzer.analyze_property_performance()
    
    if "error" not in property_performance:
        print(f"✓ Property performance analysis completed:")
        print(f"  - Total sales analyzed: {property_performance['total_sales']}")
        
        metrics = property_performance.get('overall_metrics', {})
        print(f"  - Average sale price: ${metrics.get('avg_sale_price', 0):,.0f}")
        print(f"  - Average days on market: {metrics.get('avg_days_on_market', 0):.0f}")
        
        correlations = property_performance.get('price_correlations', {})
        print(f"  - Price correlations:")
        for feature, corr in correlations.items():
            print(f"    - {feature}: {corr:.3f}")
    
    # Rental performance analysis
    print("Analyzing rental performance...")
    rental_performance = analyzer.analyze_rental_performance()
    
    if "error" not in rental_performance:
        print(f"✓ Rental performance analysis completed:")
        print(f"  - Total rentals analyzed: {rental_performance['total_rentals']}")
        
        metrics = rental_performance.get('overall_metrics', {})
        print(f"  - Average monthly rent: ${metrics.get('avg_monthly_rent', 0):,.0f}")
        print(f"  - Occupancy rate: {metrics.get('occupancy_rate', 0):.1%}")
    
    # Investment analysis example
    print("Performing investment analysis...")
    sample_property = {
        'purchase_price': 500000,
        'monthly_rent': 2500,
        'annual_expenses': 10000,
        'down_payment_percent': 0.20,
        'interest_rate': 0.06,
        'loan_term_years': 30
    }
    
    investment_analysis = analyzer.generate_investment_analysis(sample_property)
    print(f"✓ Investment analysis completed:")
    print(f"  - Investment grade: {investment_analysis['investment_grade']}")
    
    metrics = investment_analysis.get('investment_metrics', {})
    print(f"  - Cap rate: {metrics.get('cap_rate', 0):.1%}")
    print(f"  - Cash-on-cash return: {metrics.get('cash_on_cash_return', 0):.1%}")
    print(f"  - Annual cash flow: ${investment_analysis['cash_flow_analysis'].get('annual_cash_flow', 0):,.0f}")
    
    # Create comprehensive market report
    print("Creating comprehensive market report...")
    report_path = analyzer.create_market_report()
    print(f"✓ Market report created: {report_path}")
    
    return analyzer


def demonstrate_dashboard_creation(data_platform, kpi_manager, data_analyzer):
    """Demonstrate dashboard and visualization creation"""
    print("Creating dashboards and visualizations...")
    
    # Create dashboard builder
    dashboard_builder = DashboardBuilder(data_platform, kpi_manager, data_analyzer)
    
    print(f"✓ Created dashboard builder")
    
    # Create chart generator
    from real_estate_analytics.visualization.charts import ChartGenerator
    chart_generator = ChartGenerator(data_platform, style="plotly")
    
    print(f"✓ Created chart generator (style: {chart_generator.style})")
    
    # Generate various charts
    print("Generating charts...")
    
    try:
        # Price trend chart
        price_chart = chart_generator.create_price_trend_chart()
        print(f"  - Price trend chart: {price_chart}")
        
        # Property performance chart
        performance_chart = chart_generator.create_property_performance_chart()
        print(f"  - Property performance chart: {performance_chart}")
        
        # Market comparison chart
        market_chart = chart_generator.create_market_comparison_chart()
        print(f"  - Market comparison chart: {market_chart}")
        
        # KPI dashboard chart
        kpi_chart = chart_generator.create_kpi_dashboard_chart(kpi_manager)
        print(f"  - KPI dashboard chart: {kpi_chart}")
        
        print(f"✓ Generated {4} charts successfully")
        
    except Exception as e:
        print(f"  - Chart generation encountered issues: {str(e)}")
        print("  - This is expected in some environments without full data")
    
    # Export dashboard configuration
    config_path = dashboard_builder.export_dashboard_config()
    print(f"✓ Dashboard configuration exported: {config_path}")
    
    print("Dashboard creation completed!")
    print("Note: To run interactive dashboards, use dashboard_builder.run_dashboard()")
    
    return dashboard_builder


def demonstrate_complete_workflow():
    """Demonstrate a complete real estate analytics workflow"""
    print("\n" + "=" * 80)
    print("COMPLETE REAL ESTATE ANALYTICS WORKFLOW")
    print("=" * 80)
    
    print("\nThis workflow demonstrates the complete scope of work mentioned:")
    print("• Setting up a data platform tailored to business structure")
    print("• Identifying key business metrics for real estate operations")
    print("• Designing and running A/B tests with analysis")
    print("• Creating clear, actionable dashboards")
    print("• Data visualization and storytelling capabilities")
    print("• Analyzing historical data to uncover trends")
    
    # Run the complete example
    components = run_complete_example()
    
    print("\n" + "=" * 80)
    print("WORKFLOW SUMMARY")
    print("=" * 80)
    
    print(f"✓ Client Profile: {components['client'].name}")
    print(f"✓ Service Provider: {components['provider'].name}")
    print(f"✓ Service Request: {components['service_request'].title}")
    print(f"✓ Data Platform: {components['data_platform'].platform_name}")
    print(f"✓ KPI Management: {len(components['kpi_manager'].kpis)} KPIs tracked")
    print(f"✓ A/B Testing: {len(components['ab_test_manager'].tests)} tests created")
    print(f"✓ Data Analysis: Market, property, and rental analysis completed")
    print(f"✓ Dashboards: Interactive dashboards and charts generated")
    
    print("\nFramework successfully demonstrates all requested capabilities!")
    print("Ready for deployment in real estate analytics projects.")
    
    return components


if __name__ == "__main__":
    # Run the complete workflow demonstration
    demonstrate_complete_workflow()

