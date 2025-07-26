#!/usr/bin/env python3
"""
Real Estate Analytics Framework - Demo Script

This script demonstrates the complete capabilities of the framework
as specified in the scope of work.
"""

import sys
import os

# Add the framework to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    """Run the complete framework demonstration"""
    print("🏠 REAL ESTATE ANALYTICS FRAMEWORK DEMO")
    print("=" * 60)
    print()
    print("This demo showcases all the capabilities from your scope of work:")
    print("• Setting up a data platform tailored to business structure")
    print("• Identifying key business metrics for real estate operations")
    print("• Designing and running A/B tests with analysis")
    print("• Creating clear, actionable dashboards")
    print("• Data visualization and storytelling capabilities")
    print("• Analyzing historical data to uncover trends")
    print()
    
    try:
        # Import and run the complete workflow
        from real_estate_analytics.examples.usage_examples import demonstrate_complete_workflow
        
        print("🚀 Starting comprehensive demonstration...")
        print()
        
        # Run the complete workflow
        components = demonstrate_complete_workflow()
        
        print()
        print("✅ DEMO COMPLETED SUCCESSFULLY!")
        print()
        print("🎯 Framework Summary:")
        print(f"   • Client: {components['client'].name}")
        print(f"   • Provider: {components['provider'].name}")
        print(f"   • Service Request: {components['service_request'].title}")
        print(f"   • Data Platform: {components['data_platform'].platform_name}")
        print(f"   • KPIs Tracked: {len(components['kpi_manager'].kpis)}")
        print(f"   • A/B Tests: {len(components['ab_test_manager'].tests)}")
        print()
        print("📊 Generated Outputs:")
        print("   • Sample real estate data created")
        print("   • KPI calculations completed")
        print("   • A/B test results analyzed")
        print("   • Market analysis reports generated")
        print("   • Dashboard configurations exported")
        print()
        print("🎉 The framework is ready for your real estate analytics projects!")
        print()
        print("Next Steps:")
        print("1. Customize the client and provider profiles for your business")
        print("2. Connect your actual data sources")
        print("3. Configure KPIs specific to your metrics")
        print("4. Set up A/B tests for your marketing strategies")
        print("5. Create dashboards tailored to your stakeholders")
        print()
        print("📖 See README.md for detailed usage instructions")
        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
        print()
        print("🔧 Troubleshooting:")
        print("1. Ensure all dependencies are installed: pip install -r requirements.txt")
        print("2. Run the test suite: python test_framework.py")
        print("3. Check the README.md for setup instructions")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

