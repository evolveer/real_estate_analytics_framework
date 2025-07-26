"""
Real Estate Analytics Framework - Streamlit UI
A comprehensive web interface for real estate data analytics
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random
import time
from datetime import datetime, timedelta
from faker import Faker

# Import the framework components
import sys
import os

# Add the parent directory to the Python path to allow imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    from real_estate_analytics.core.client import Client
    from real_estate_analytics.core.provider import ServiceProvider
    from real_estate_analytics.core.service_request import ServiceRequest, ServiceType, ProjectType
    from real_estate_analytics.data_platform.platform import DataPlatform
    from real_estate_analytics.analytics.kpi_manager import KPIManager, KPI, KPICategory
    from real_estate_analytics.analytics.ab_testing import ABTestManager, TestStatus
    from real_estate_analytics.analytics.data_analyzer import DataAnalyzer
    from real_estate_analytics.visualization.dashboard import DashboardBuilder
    from real_estate_analytics.visualization.charts import ChartGenerator
except ImportError as e:
    st.error(f"Framework import error: {e}")
    st.info("Please make sure the real_estate_analytics module is properly installed or in the Python path.")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Real Estate Analytics",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #c3e6cb;
    }
    .warning-message {
        background-color: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #ffeaa7;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def initialize_session_state():
    """Initialize session state variables"""
    if 'data_platform' not in st.session_state:
        st.session_state.data_platform = None
    if 'kpi_manager' not in st.session_state:
        st.session_state.kpi_manager = None
    if 'ab_test_manager' not in st.session_state:
        st.session_state.ab_test_manager = None
    if 'data_analyzer' not in st.session_state:
        st.session_state.data_analyzer = None
    if 'client' not in st.session_state:
        st.session_state.client = None
    if 'provider' not in st.session_state:
        st.session_state.provider = None
    if 'service_request' not in st.session_state:
        st.session_state.service_request = None
    if 'sample_data_generated' not in st.session_state:
        st.session_state.sample_data_generated = False

def main():
    """Main application function"""
    initialize_session_state()
    
    # Header
    st.markdown('<div class="main-header">🏠 Real Estate Analytics Framework</div>', unsafe_allow_html=True)
    
    # Sidebar for navigation and controls
    with st.sidebar:
        st.image("https://via.placeholder.com/200x100/1f77b4/ffffff?text=Real+Estate+Analytics", width=200)
        st.markdown("---")
        
        # Quick setup section
        st.subheader("🚀 Quick Setup")
        if st.button("Initialize Framework", type="primary", use_container_width=True):
            initialize_framework()
        
        if st.button("Generate Sample Data", use_container_width=True):
            generate_sample_data()
        
        st.markdown("---")
        
        # Status indicators
        st.subheader("📊 System Status")
        status_indicators()
    
    # Main content area with tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "🏢 Client Management", 
        "📊 Data Platform", 
        "📈 KPI Dashboard", 
        "🧪 A/B Testing", 
        "🔍 Data Analysis", 
        "📋 Reports", 
        "⚙️ Settings"
    ])
    
    with tab1:
        client_management_tab()
    
    with tab2:
        data_platform_tab()
    
    with tab3:
        kpi_dashboard_tab()
    
    with tab4:
        ab_testing_tab()
    
    with tab5:
        data_analysis_tab()
    
    with tab6:
        reports_tab()
    
    with tab7:
        settings_tab()

def initialize_framework():
    """Initialize the framework components"""
    with st.spinner("Initializing framework..."):
        try:
            # Create data platform
            st.session_state.data_platform = DataPlatform("StreamlitAnalytics", "./streamlit_data")
            
            # Create default client
            st.session_state.client = Client(
                name="Demo Real Estate Company",
                location="Demo City",
                business_type="Real Estate",
                company="Demo Properties LLC"
            )
            
            # Create default provider
            st.session_state.provider = ServiceProvider(
                name="Analytics Expert",
                title="Senior Data Analyst",
                company="Analytics Solutions"
            )
            
            # Create service request
            st.session_state.service_request = ServiceRequest(
                client=st.session_state.client,
                service_type=ServiceType.BUSINESS_ANALYTICS,
                project_type=ProjectType.ONE_TIME
            )
            
            # Assign provider
            st.session_state.service_request.assign_provider(st.session_state.provider)
            
            # Initialize other components
            st.session_state.kpi_manager = KPIManager(st.session_state.data_platform)
            st.session_state.ab_test_manager = ABTestManager()
            st.session_state.data_analyzer = DataAnalyzer(st.session_state.data_platform)
            
            st.success("✅ Framework initialized successfully!")
            time.sleep(1)
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Initialization failed: {str(e)}")

def generate_sample_data():
    """Generate sample data for demonstration"""
    if st.session_state.data_platform is None:
        st.error("Please initialize the framework first!")
        return
    
    with st.spinner("Generating sample data..."):
        try:
            sample_data = st.session_state.data_platform.create_sample_data()
            st.session_state.sample_data_generated = True
            
            # Generate sample A/B tests
            generate_sample_ab_tests()
            
            st.success(f"✅ Generated {len(sample_data['properties'])} properties, {len(sample_data['market_data'])} market records, and 5 sample A/B tests!")
            time.sleep(1)
            st.rerun()
        except Exception as e:
            st.error(f"❌ Data generation failed: {str(e)}")

def generate_sample_ab_tests():
    """Generate sample A/B tests for demonstration"""
    try:
        ab_manager = st.session_state.ab_test_manager
        
        # Sample Test 1: Pricing Strategy (Completed)
        test1 = ab_manager.create_test_from_template(
            template_name="pricing_strategy",
            test_name="Premium Pricing Strategy",
            hypothesis="Reducing listing price by 5% will increase conversion rate and reduce time on market"
        )
        if test1:
            # Add sample data to variants
            for i, variant in enumerate(test1.variants):
                if i == 0:  # Control group
                    for _ in range(150):
                        converted = random.random() < 0.12  # 12% conversion
                        value = 485000 if converted else 0
                        variant.add_participant(converted, value)
                else:  # Treatment group
                    for _ in range(145):
                        converted = random.random() < 0.18  # 18% conversion
                        value = 478000 if converted else 0
                        variant.add_participant(converted, value)
            
            test1.status = TestStatus.COMPLETED
            test1.start_date = datetime.now() - timedelta(days=45)
            test1.stop_test()
        
        # Sample Test 2: Marketing Campaign (not using template that doesn't exist)
        test2 = ab_manager.create_test_from_template(
            template_name="email_campaign",
            test_name="Social Media Ad Campaign",
            hypothesis="Video ads will outperform static image ads in lead generation"
        )
        if test2:
            # Add sample data to variants
            for i, variant in enumerate(test2.variants):
                if i == 0:  # Control group
                    for _ in range(200):
                        converted = random.random() < 0.08  # 8% conversion
                        value = 125 if converted else 0
                        variant.add_participant(converted, value)
                else:  # Treatment group
                    for _ in range(195):
                        converted = random.random() < 0.11  # 11% conversion
                        value = 98 if converted else 0
                        variant.add_participant(converted, value)
            
            test2.status = TestStatus.COMPLETED
            test2.start_date = datetime.now() - timedelta(days=30)
            test2.stop_test()
        
        # Sample Test 3: Email Campaign (Running)
        test3 = ab_manager.create_test_from_template(
            template_name="email_campaign",
            test_name="Property Listing Layout",
            hypothesis="Grid layout will improve user engagement compared to list layout"
        )
        if test3:
            # Add sample data to variants
            for i, variant in enumerate(test3.variants):
                if i == 0:  # Control group
                    for _ in range(89):
                        converted = random.random() < 0.15  # 15% conversion
                        value = random.randint(300000, 600000) if converted else 0
                        variant.add_participant(converted, value)
                else:  # Treatment group
                    for _ in range(91):
                        converted = random.random() < 0.18  # 18% conversion
                        value = random.randint(320000, 620000) if converted else 0
                        variant.add_participant(converted, value)
            
            test3.status = TestStatus.RUNNING
            test3.start_date = datetime.now() - timedelta(days=14)
        
        # Sample Test 4: Email Campaign (Running)
        test4 = ab_manager.create_test_from_template(
            template_name="email_campaign",
            test_name="Personalized Email Subject Lines",
            hypothesis="Personalized subject lines will increase email engagement rates"
        )
        if test4:
            # Add sample data to variants
            for i, variant in enumerate(test4.variants):
                if i == 0:  # Control group
                    for _ in range(125):
                        converted = random.random() < 0.24  # 24% conversion
                        value = random.randint(50, 200) if converted else 0
                        variant.add_participant(converted, value)
                else:  # Treatment group
                    for _ in range(128):
                        converted = random.random() < 0.31  # 31% conversion
                        value = random.randint(60, 220) if converted else 0
                        variant.add_participant(converted, value)
            
            test4.status = TestStatus.RUNNING
            test4.start_date = datetime.now() - timedelta(days=7)
        
        # Sample Test 5: Planned Test
        test5 = ab_manager.create_test_from_template(
            template_name="listing_photos",
            test_name="Virtual Tour Integration",
            hypothesis="Adding virtual tours will increase property inquiries by 25%"
        )
        if test5:
            test5.status = TestStatus.DRAFT
        
        st.session_state.sample_ab_tests_generated = True
        
    except Exception as e:
        st.error(f"Error generating sample A/B tests: {str(e)}")
        return False

def status_indicators():
    """Display system status indicators"""
    col1, col2 = st.columns(2)
    
    with col1:
        if st.session_state.data_platform:
            st.success("✅ Platform")
        else:
            st.error("❌ Platform")
    
    with col2:
        if st.session_state.sample_data_generated:
            st.success("✅ Data")
        else:
            st.warning("⚠️ No Data")
    
    col3, col4 = st.columns(2)
    
    with col3:
        if st.session_state.kpi_manager:
            st.success("✅ KPIs")
        else:
            st.error("❌ KPIs")
    
    with col4:
        if st.session_state.ab_test_manager:
            st.success("✅ A/B Tests")
        else:
            st.error("❌ A/B Tests")

def client_management_tab():
    """Client management interface"""
    st.header("🏢 Client & Service Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👤 Client Profile")
        
        if st.session_state.client:
            with st.container():
                st.markdown(f"**Name:** {st.session_state.client.name}")
                st.markdown(f"**Location:** {st.session_state.client.location}")
                st.markdown(f"**Business Type:** {st.session_state.client.business_type}")
                st.markdown(f"**Company:** {st.session_state.client.company}")
                
                # Edit client button
                if st.button("✏️ Edit Client Profile"):
                    edit_client_profile()
        else:
            st.info("No client profile available. Initialize the framework first.")
    
    with col2:
        st.subheader("👨‍💼 Service Provider")
        
        if st.session_state.provider:
            with st.container():
                st.markdown(f"**Name:** {st.session_state.provider.name}")
                st.markdown(f"**Title:** {st.session_state.provider.title}")
                st.markdown(f"**Company:** {st.session_state.provider.company}")
                st.markdown(f"**Rating:** {st.session_state.provider.client_rating}/5.0 ⭐")
                
                # Edit provider button
                if st.button("✏️ Edit Provider Profile"):
                    edit_provider_profile()
        else:
            st.info("No provider profile available. Initialize the framework first.")
    
    # Service Request Status
    st.subheader("📋 Service Request Status")
    
    if st.session_state.service_request:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Status", st.session_state.service_request.status.value.title())
        
        with col2:
            st.metric("Progress", f"{st.session_state.service_request.progress_percentage}%")
        
        with col3:
            days_left = st.session_state.service_request.days_until_deadline()
            st.metric("Days Until Deadline", days_left)
        
        # Progress update
        st.subheader("📈 Update Progress")
        col1, col2 = st.columns([3, 1])
        
        with col1:
            new_progress = st.slider("Progress Percentage", 0, 100, st.session_state.service_request.progress_percentage)
            progress_note = st.text_input("Progress Note", placeholder="Enter progress update...", key="progress_note_input")
        
        with col2:
            st.write("")  # Spacing
            st.write("")  # Spacing
            if st.button("Update Progress", type="primary"):
                st.session_state.service_request.update_progress(new_progress, progress_note)
                st.success("Progress updated!")
                st.rerun()
    else:
        st.info("No service request available. Initialize the framework first.")

def edit_client_profile():
    """Edit client profile in a modal-like interface"""
    with st.expander("Edit Client Profile", expanded=True):
        client = st.session_state.client
        
        new_name = st.text_input("Company Name", value=client.name, key="edit_client_name")
        new_location = st.text_input("Location", value=client.location, key="edit_client_location")
        new_business_type = st.selectbox("Business Type", 
                                       ["Real Estate", "Property Management", "Investment", "Development"],
                                       index=0 if client.business_type == "Real Estate" else 0)
        new_company = st.text_input("Company", value=client.company, key="edit_client_company")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Save Changes", type="primary"):
                client.name = new_name
                client.location = new_location
                client.business_type = new_business_type
                client.company = new_company
                st.success("Client profile updated!")
                st.rerun()
        
        with col2:
            if st.button("Cancel"):
                st.rerun()

def edit_provider_profile():
    """Edit provider profile in a modal-like interface"""
    with st.expander("Edit Provider Profile", expanded=True):
        provider = st.session_state.provider
        
        new_name = st.text_input("Provider Name", value=provider.name, key="edit_provider_name")
        new_title = st.text_input("Title", value=provider.title, key="edit_provider_title")
        new_company = st.text_input("Company", value=provider.company, key="edit_provider_company")
        new_rate = st.number_input("Hourly Rate ($)", value=provider.hourly_rate, min_value=0.0)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Save Changes", type="primary"):
                provider.name = new_name
                provider.title = new_title
                provider.company = new_company
                provider.hourly_rate = new_rate
                st.success("Provider profile updated!")
                st.rerun()
        
        with col2:
            if st.button("Cancel"):
                st.rerun()

def data_platform_tab():
    """Data platform management interface"""
    st.header("📊 Data Platform Management")
    
    if not st.session_state.data_platform:
        st.warning("Please initialize the framework first!")
        return
    
    # Platform overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Platform Name", st.session_state.data_platform.platform_name)
    
    with col2:
        st.metric("Data Sources", len(st.session_state.data_platform.data_sources))
    
    with col3:
        status = st.session_state.data_platform.get_platform_status()
        st.metric("Active Sources", status['active_sources'])
    
    # Data sources management
    st.subheader("🔗 Data Sources")
    
    # Display existing data sources
    for name, source in st.session_state.data_platform.data_sources.items():
        with st.expander(f"📁 {name} ({source.source_type})"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"**Type:** {source.source_type}")
                if hasattr(source, 'connection_string'):
                    st.write(f"**Connection:** {source.connection_string}")
                if hasattr(source, 'file_path'):
                    st.write(f"**Path:** {source.file_path}")
                st.write(f"**Last Updated:** {source.last_updated}")
            
            with col2:
                if st.button(f"Test Connection", key=f"test_{name}"):
                    test_data_source_connection(name)
    
    # Add new data source
    st.subheader("➕ Add New Data Source")
    
    with st.form("add_data_source"):
        col1, col2 = st.columns(2)
        
        with col1:
            source_name = st.text_input("Source Name", key="add_source_name")
            source_type = st.selectbox("Source Type", ["database", "api", "file"], key="add_source_type")
        
        with col2:
            if source_type == "database":
                connection_string = st.text_input("Connection String", placeholder="sqlite:///example.db", key="add_source_connection")
            elif source_type == "api":
                api_endpoint = st.text_input("API Endpoint", placeholder="https://api.example.com", key="add_source_api")
            else:
                file_path = st.text_input("File Path", placeholder="/path/to/file.csv", key="add_source_file")
        
        if st.form_submit_button("Add Data Source", type="primary"):
            add_new_data_source(source_name, source_type, locals())
    
    # Sample data section
    st.subheader("🎲 Sample Data")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if st.session_state.sample_data_generated:
            st.success("✅ Sample data is available")
        else:
            st.info("No sample data generated yet")
    
    with col2:
        if st.button("Generate Sample Data", type="primary"):
            generate_sample_data()
    
    # Data preview
    if st.session_state.sample_data_generated:
        st.subheader("👀 Data Preview")
        
        preview_type = st.selectbox("Select Data to Preview", ["Properties", "Market Data"], key="data_preview_selector")
        
        try:
            if preview_type == "Properties":
                df = st.session_state.data_platform.load_data("default_database", table_name="properties")
                if df is not None and not df.empty:
                    st.dataframe(df.head(10), use_container_width=True)
                else:
                    st.info("No properties data available")
            
            elif preview_type == "Market Data":
                df = st.session_state.data_platform.load_data("default_database", table_name="market_data")
                if df is not None and not df.empty:
                    st.dataframe(df.head(10), use_container_width=True)
                else:
                    st.info("No market data available")
        
        except Exception as e:
            st.error(f"Error loading data preview: {str(e)}")

def test_data_source_connection(source_name):
    """Test data source connection"""
    try:
        conn = st.session_state.data_platform.connect_to_source(source_name)
        if conn:
            st.success(f"✅ Connection to {source_name} successful!")
            conn.close()
        else:
            st.error(f"❌ Failed to connect to {source_name}")
    except Exception as e:
        st.error(f"❌ Connection error: {str(e)}")

def add_new_data_source(source_name, source_type, form_data):
    """Add a new data source"""
    if not source_name:
        st.error("Please provide a source name")
        return
    
    try:
        if source_type == "database":
            connection_string = form_data.get('connection_string', '')
            st.session_state.data_platform.add_data_source(
                name=source_name,
                source_type=source_type,
                connection_string=connection_string
            )
        elif source_type == "api":
            api_endpoint = form_data.get('api_endpoint', '')
            st.session_state.data_platform.add_data_source(
                name=source_name,
                source_type=source_type,
                api_endpoint=api_endpoint
            )
        else:  # file
            file_path = form_data.get('file_path', '')
            st.session_state.data_platform.add_data_source(
                name=source_name,
                source_type=source_type,
                file_path=file_path
            )
        
        st.success(f"✅ Data source '{source_name}' added successfully!")
        st.rerun()
        
    except Exception as e:
        st.error(f"❌ Failed to add data source: {str(e)}")

def kpi_dashboard_tab():
    """KPI dashboard interface"""
    st.header("📈 KPI Dashboard")
    
    if not st.session_state.kpi_manager:
        st.warning("Please initialize the framework first!")
        return
    
    # KPI calculation
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("📊 Key Performance Indicators")
    
    with col2:
        if st.button("🔄 Refresh KPIs", type="primary"):
            refresh_kpis()
    
    # Calculate and display KPIs
    try:
        kpi_results = st.session_state.kpi_manager.calculate_all_kpis()
        
        if kpi_results:
            # Display KPIs in a grid
            cols = st.columns(3)
            
            for i, (kpi_name, value) in enumerate(kpi_results.items()):
                col_idx = i % 3
                
                with cols[col_idx]:
                    kpi = st.session_state.kpi_manager.kpis[kpi_name]
                    
                    # Determine performance status
                    performance = kpi.get_performance_status()
                    
                    # Color coding based on performance
                    if performance == "exceeding":
                        delta_color = "normal"
                        status_emoji = "🟢"
                    elif performance == "meeting":
                        delta_color = "normal"
                        status_emoji = "🟡"
                    else:
                        delta_color = "inverse"
                        status_emoji = "🔴"
                    
                    st.metric(
                        label=f"{status_emoji} {kpi_name}",
                        value=f"{value:.2f} {kpi.unit}",
                        delta=f"Target: {kpi.target_value} {kpi.unit}",
                        delta_color=delta_color
                    )
        else:
            st.info("No KPI data available. Generate sample data first.")
    
    except Exception as e:
        st.error(f"Error calculating KPIs: {str(e)}")
    
    # KPI Management
    st.subheader("⚙️ KPI Management")
    
    # Add custom KPI
    with st.expander("➕ Add Custom KPI"):
        with st.form("add_kpi"):
            col1, col2 = st.columns(2)
            
            with col1:
                kpi_name = st.text_input("KPI Name", key="add_kpi_name")
                kpi_category = st.selectbox("Category", ["SALES", "MARKETING", "FINANCIAL", "OPERATIONAL", "CUSTOMER"], key="add_kpi_category")
                kpi_unit = st.text_input("Unit", placeholder="e.g., %, $, days", key="add_kpi_unit")
            
            with col2:
                kpi_target = st.number_input("Target Value", value=0.0)
                kpi_description = st.text_area("Description")
            
            if st.form_submit_button("Add KPI", type="primary"):
                add_custom_kpi(kpi_name, kpi_category, kpi_unit, kpi_target, kpi_description)
    
    # KPI History Chart
    st.subheader("📈 KPI Trends")
    
    if kpi_results:
        # Create a sample trend chart
        kpi_names = list(kpi_results.keys())[:6]  # Show top 6 KPIs
        selected_kpi = st.selectbox("Select KPI to view trend", kpi_names)
        
        if selected_kpi:
            create_kpi_trend_chart(selected_kpi)

def refresh_kpis():
    """Refresh KPI calculations"""
    with st.spinner("Refreshing KPIs..."):
        try:
            st.session_state.kpi_manager.calculate_all_kpis()
            st.success("✅ KPIs refreshed successfully!")
            time.sleep(1)
            st.rerun()
        except Exception as e:
            st.error(f"❌ Failed to refresh KPIs: {str(e)}")

def add_custom_kpi(name, category, unit, target, description):
    """Add a custom KPI"""
    if not name:
        st.error("Please provide a KPI name")
        return
    
    try:
        from real_estate_analytics.analytics.kpi_manager import KPICategory
        
        custom_kpi = KPI(
            name=name,
            category=getattr(KPICategory, category),
            description=description,
            calculation_method="custom",
            target_value=target,
            unit=unit
        )
        
        st.session_state.kpi_manager.add_kpi(custom_kpi)
        st.success(f"✅ Custom KPI '{name}' added successfully!")
        st.rerun()
        
    except Exception as e:
        st.error(f"❌ Failed to add custom KPI: {str(e)}")

def create_kpi_trend_chart(kpi_name):
    """Create a trend chart for a specific KPI"""
    try:
        # Generate sample trend data
        dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='D')
        
        # Get current KPI value
        kpi_results = st.session_state.kpi_manager.calculate_all_kpis()
        current_value = kpi_results.get(kpi_name, 0)
        
        # Generate trend data around current value
        import numpy as np
        trend_values = current_value + np.random.normal(0, current_value * 0.1, len(dates))
        
        # Create chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=dates,
            y=trend_values,
            mode='lines+markers',
            name=kpi_name,
            line=dict(color='#1f77b4', width=3)
        ))
        
        # Add target line
        kpi = st.session_state.kpi_manager.kpis[kpi_name]
        fig.add_hline(
            y=kpi.target_value,
            line_dash="dash",
            line_color="red",
            annotation_text=f"Target: {kpi.target_value}"
        )
        
        fig.update_layout(
            title=f"{kpi_name} Trend (Last 30 Days)",
            xaxis_title="Date",
            yaxis_title=f"Value ({kpi.unit})",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error creating trend chart: {str(e)}")

def ab_testing_tab():
    """A/B testing interface"""
    st.header("🧪 A/B Testing")
    
    if not st.session_state.ab_test_manager:
        st.warning("Please initialize the framework first!")
        return
    
    # Test overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Tests", len(st.session_state.ab_test_manager.tests))
    
    with col2:
        running_tests = sum(1 for test in st.session_state.ab_test_manager.tests.values() 
                          if test.status.value == "running")
        st.metric("Running Tests", running_tests)
    
    with col3:
        completed_tests = sum(1 for test in st.session_state.ab_test_manager.tests.values() 
                            if test.status.value == "completed")
        st.metric("Completed Tests", completed_tests)
    
    # Create new test
    st.subheader("➕ Create New A/B Test")
    
    with st.expander("Create Test from Template"):
        col1, col2 = st.columns(2)
        
        with col1:
            template_options = list(st.session_state.ab_test_manager.templates.keys())
            selected_template = st.selectbox("Select Template", template_options)
            test_name = st.text_input("Test Name", placeholder="Enter test name", key="ab_test_name")
        
        with col2:
            hypothesis = st.text_area("Hypothesis", placeholder="Enter your hypothesis")
        
        if st.button("Create Test", type="primary"):
            create_ab_test_from_template(selected_template, test_name, hypothesis)
    
    # Display existing tests
    st.subheader("📋 Existing Tests")
    
    if st.session_state.ab_test_manager.tests:
        for test_id, test in st.session_state.ab_test_manager.tests.items():
            # Status indicator
            status_icon = {
                "completed": "✅",
                "running": "🔄", 
                "planned": "📅",
                "draft": "📝"
            }.get(test.status.value, "❓")
            
            with st.expander(f"{status_icon} {test.name} ({test.status.value.upper()})"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**Hypothesis:** {test.hypothesis}")
                    st.write(f"**Template:** {test.template}")
                    
                    if hasattr(test, 'start_date') and test.start_date:
                        st.write(f"**Started:** {test.start_date.strftime('%Y-%m-%d')}")
                    if hasattr(test, 'end_date') and test.end_date:
                        st.write(f"**Ended:** {test.end_date.strftime('%Y-%m-%d')}")
                    
                    # Show test results for completed tests
                    if test.status.value == "completed" and hasattr(test, 'control_data'):
                        st.write("**Results:**")
                        
                        # Display metrics based on template type
                        if test.template == "pricing_strategy":
                            col_a, col_b = st.columns(2)
                            with col_a:
                                st.write("🅰️ **Control Group:**")
                                st.write(f"• Size: {test.control_data.get('size', 'N/A')}")
                                st.write(f"• Conversion: {test.control_data.get('conversion_rate', 0)*100:.1f}%")
                                st.write(f"• Avg Price: ${test.control_data.get('avg_sale_price', 0):,}")
                                st.write(f"• Days on Market: {test.control_data.get('avg_days_on_market', 0)}")
                            
                            with col_b:
                                st.write("🅱️ **Treatment Group:**")
                                st.write(f"• Size: {test.treatment_data.get('size', 'N/A')}")
                                st.write(f"• Conversion: {test.treatment_data.get('conversion_rate', 0)*100:.1f}%")
                                st.write(f"• Avg Price: ${test.treatment_data.get('avg_sale_price', 0):,}")
                                st.write(f"• Days on Market: {test.treatment_data.get('avg_days_on_market', 0)}")
                            
                            # Calculate statistical significance
                            improvement = ((test.treatment_data.get('conversion_rate', 0) - 
                                          test.control_data.get('conversion_rate', 0)) / 
                                         test.control_data.get('conversion_rate', 1)) * 100
                            
                            if improvement > 0:
                                st.success(f"🎉 **Result:** {improvement:.1f}% improvement in conversion rate")
                            else:
                                st.error(f"📉 **Result:** {abs(improvement):.1f}% decrease in conversion rate")
                        
                        elif test.template == "marketing_campaign":
                            col_a, col_b = st.columns(2)
                            with col_a:
                                st.write("🅰️ **Control (Static Ads):**")
                                st.write(f"• Size: {test.control_data.get('size', 'N/A')}")
                                st.write(f"• CTR: {test.control_data.get('click_through_rate', 0)*100:.1f}%")
                                st.write(f"• Lead Conv: {test.control_data.get('lead_conversion', 0)*100:.1f}%")
                                st.write(f"• Cost/Lead: ${test.control_data.get('cost_per_lead', 0)}")
                            
                            with col_b:
                                st.write("🅱️ **Treatment (Video Ads):**")
                                st.write(f"• Size: {test.treatment_data.get('size', 'N/A')}")
                                st.write(f"• CTR: {test.treatment_data.get('click_through_rate', 0)*100:.1f}%")
                                st.write(f"• Lead Conv: {test.treatment_data.get('lead_conversion', 0)*100:.1f}%")
                                st.write(f"• Cost/Lead: ${test.treatment_data.get('cost_per_lead', 0)}")
                            
                            ctr_improvement = ((test.treatment_data.get('click_through_rate', 0) - 
                                              test.control_data.get('click_through_rate', 0)) / 
                                             test.control_data.get('click_through_rate', 1)) * 100
                            
                            if ctr_improvement > 0:
                                st.success(f"🎉 **Result:** {ctr_improvement:.1f}% improvement in CTR")
                            
                    # Show progress for running tests
                    elif test.status.value == "running" and hasattr(test, 'control_data'):
                        st.write("**Current Progress:**")
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.write("🅰️ **Control Group:**")
                            st.write(f"• Participants: {test.control_data.get('size', 0)}")
                        with col_b:
                            st.write("🅱️ **Treatment Group:**")
                            st.write(f"• Participants: {test.treatment_data.get('size', 0)}")
                        
                        # Progress bar
                        days_running = (datetime.now() - test.start_date).days if hasattr(test, 'start_date') else 0
                        st.progress(min(days_running / 30, 1.0))  # Assume 30-day test duration
                        st.write(f"Running for {days_running} days")
                
                with col2:
                    # Test controls
                    if test.status.value == "draft":
                        if st.button(f"▶️ Start Test", key=f"start_{test_id}"):
                            start_ab_test(test_id)
                    
                    elif test.status.value == "running":
                        if st.button(f"⏹️ Stop Test", key=f"stop_{test_id}"):
                            stop_ab_test(test_id)
                        
                        if st.button(f"📊 View Results", key=f"results_{test_id}"):
                            display_ab_test_results(test_id)
                    
                    elif test.status.value == "completed":
                        if st.button(f"📊 Full Report", key=f"report_{test_id}"):
                            display_ab_test_results(test_id)
                    
                    # Add sample data button for new tests
                    if test.status.value == "draft":
                        if st.button(f"🎲 Add Sample Data", key=f"sample_{test_id}"):
                            add_sample_ab_test_data(test_id)
    else:
        st.info("No A/B tests created yet. Create your first test above!")
    
    # Test results visualization
    if st.session_state.ab_test_manager.tests:
        st.subheader("📊 Test Results Dashboard")
        
        test_options = [(test_id, test.name) for test_id, test in st.session_state.ab_test_manager.tests.items()]
        selected_test = st.selectbox(
            "Select Test for Results",
            test_options,
            format_func=lambda x: x[1]
        )
        
        if selected_test:
            display_ab_test_results(selected_test[0])

def create_ab_test_from_template(template_name, test_name, hypothesis):
    """Create A/B test from template"""
    if not test_name:
        st.error("Please provide a test name")
        return
    
    try:
        test = st.session_state.ab_test_manager.create_test_from_template(
            template_name, test_name, hypothesis
        )
        
        if test:
            st.success(f"✅ A/B test '{test_name}' created successfully!")
            st.rerun()
        else:
            st.error("❌ Failed to create test")
    
    except Exception as e:
        st.error(f"❌ Error creating test: {str(e)}")

def start_ab_test(test_id):
    """Start an A/B test"""
    try:
        test = st.session_state.ab_test_manager.tests[test_id]
        test.start_test()
        st.success(f"✅ Test '{test.name}' started!")
        st.rerun()
    except Exception as e:
        st.error(f"❌ Error starting test: {str(e)}")

def stop_ab_test(test_id):
    """Stop an A/B test"""
    try:
        test = st.session_state.ab_test_manager.tests[test_id]
        test.end_test()
        st.success(f"✅ Test '{test.name}' stopped!")
        st.rerun()
    except Exception as e:
        st.error(f"❌ Error stopping test: {str(e)}")

def add_sample_ab_test_data(test_id):
    """Add sample data to an A/B test"""
    try:
        test = st.session_state.ab_test_manager.tests[test_id]
        
        # Add sample data for each variant
        import random
        
        for variant in test.variants:
            for _ in range(50):  # 50 sample data points per variant
                converted = random.random() < 0.15  # 15% base conversion rate
                value = random.randint(300000, 800000) if converted else 0
                
                # Adjust for different variants
                if "Premium" in variant.name:
                    converted = random.random() < 0.12  # Lower conversion
                    if converted:
                        value = int(value * 1.05)  # Higher value
                
                test.add_data_point(variant.name, converted, value)
        
        st.success(f"✅ Sample data added to test '{test.name}'!")
        st.rerun()
        
    except Exception as e:
        st.error(f"❌ Error adding sample data: {str(e)}")

def display_ab_test_results(test_id):
    """Display A/B test results"""
    try:
        test = st.session_state.ab_test_manager.tests[test_id]
        results = test.get_current_results()
        
        if not results.get('variants'):
            st.info("No test data available yet.")
            return
        
        # Results summary
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Participants", results['total_participants'])
        
        with col2:
            winner_info = results.get('winner', {})
            st.metric("Winner", winner_info.get('winner', 'TBD'))
        
        with col3:
            significance = "Yes" if results.get('is_significant', False) else "No"
            st.metric("Statistically Significant", significance)
        
        # Variant comparison chart
        variants_data = results['variants']
        variant_names = [v['name'] for v in variants_data]
        conversion_rates = [v['conversion_rate'] * 100 for v in variants_data]  # Convert to percentage
        participants = [v['participants'] for v in variants_data]
        
        # Conversion rate chart
        fig_conversion = go.Figure(data=[
            go.Bar(name='Conversion Rate (%)', x=variant_names, y=conversion_rates)
        ])
        
        fig_conversion.update_layout(
            title="Conversion Rate by Variant",
            yaxis_title="Conversion Rate (%)",
            height=400
        )
        
        st.plotly_chart(fig_conversion, use_container_width=True)
        
        # Participants chart
        fig_participants = go.Figure(data=[
            go.Bar(name='Participants', x=variant_names, y=participants, marker_color='lightblue')
        ])
        
        fig_participants.update_layout(
            title="Participants by Variant",
            yaxis_title="Number of Participants",
            height=400
        )
        
        st.plotly_chart(fig_participants, use_container_width=True)
        
        # Detailed results table
        st.subheader("📋 Detailed Results")
        
        results_df = pd.DataFrame([
            {
                'Variant': v['name'],
                'Participants': v['participants'],
                'Conversions': v['conversions'],
                'Conversion Rate': f"{v['conversion_rate']:.1%}",
                'Average Value': f"${v['average_value']:,.0f}",
                'Confidence Interval': 'N/A'  # Will be populated from statistical analysis if available
            }
            for v in variants_data
        ])
        
        # Add confidence interval from statistical analysis if available
        if 'statistical_analysis' in results and 'confidence_interval' in results['statistical_analysis']:
            ci = results['statistical_analysis']['confidence_interval']
            if 'lower' in ci and 'upper' in ci:
                # Add statistical confidence interval information
                st.write(f"**Statistical Analysis:**")
                st.write(f"Confidence Interval for Difference: {ci['lower']:.1%} - {ci['upper']:.1%}")
        
        st.dataframe(results_df, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error displaying test results: {str(e)}")

def data_analysis_tab():
    """Data analysis interface"""
    st.header("🔍 Data Analysis")
    
    if not st.session_state.data_analyzer:
        st.warning("Please initialize the framework first!")
        return
    
    if not st.session_state.sample_data_generated:
        st.warning("Please generate sample data first!")
        return
    
    # Analysis options
    analysis_type = st.selectbox(
        "Select Analysis Type",
        ["Market Trends", "Property Performance", "Rental Analysis", "Investment Analysis"]
    )
    
    if analysis_type == "Market Trends":
        market_trends_analysis()
    elif analysis_type == "Property Performance":
        property_performance_analysis()
    elif analysis_type == "Rental Analysis":
        rental_analysis()
    elif analysis_type == "Investment Analysis":
        investment_analysis()

def market_trends_analysis():
    """Market trends analysis interface"""
    st.subheader("📈 Market Trends Analysis")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        time_period = st.slider("Analysis Period (days)", 30, 365, 180)
        region_filter = st.text_input("Region Filter (optional)", placeholder="Enter region name", key="market_trends_region_filter")
    
    with col2:
        st.write("")  # Spacing
        st.write("")  # Spacing
        if st.button("Run Analysis", type="primary"):
            run_market_trends_analysis(time_period, region_filter)

def run_market_trends_analysis(time_period, region_filter):
    """Run market trends analysis"""
    with st.spinner("Analyzing market trends..."):
        try:
            region = region_filter if region_filter else None
            results = st.session_state.data_analyzer.analyze_market_trends(
                time_period_days=time_period,
                region=region
            )
            
            if "error" in results:
                st.error(f"Analysis error: {results['error']}")
                return
            
            # Display results
            st.success("✅ Market trends analysis completed!")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Data Points Analyzed", results['data_points'])
                st.metric("Regions Analyzed", len(results.get('regional_summary', {})))
            
            with col2:
                st.metric("Time Period", f"{time_period} days")
                if region:
                    st.metric("Region Filter", region)
            
            # Trends visualization
            trends = results.get('trends', {})
            if trends:
                st.subheader("📊 Trend Analysis")
                
                trend_data = []
                for metric, trend_info in trends.items():
                    trend_data.append({
                        'Metric': metric.replace('_', ' ').title(),
                        'Direction': trend_info.get('trend_direction', 'unknown'),
                        'Change (%)': trend_info.get('percentage_change', 0)
                    })
                
                trend_df = pd.DataFrame(trend_data)
                st.dataframe(trend_df, use_container_width=True)
                
                # Create trend chart
                fig = go.Figure()
                
                metrics = [item['Metric'] for item in trend_data]
                changes = [item['Change (%)'] for item in trend_data]
                colors = ['green' if x > 0 else 'red' for x in changes]
                
                fig.add_trace(go.Bar(
                    x=metrics,
                    y=changes,
                    marker_color=colors,
                    name='Percentage Change'
                ))
                
                fig.update_layout(
                    title="Market Trends - Percentage Change",
                    yaxis_title="Change (%)",
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")

def property_performance_analysis():
    """Property performance analysis interface"""
    st.subheader("🏠 Property Performance Analysis")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        property_type_filter = st.selectbox(
            "Property Type Filter",
            ["All", "House", "Apartment", "Condo", "Townhouse"]
        )
    
    with col2:
        st.write("")  # Spacing
        if st.button("Run Analysis", type="primary"):
            run_property_performance_analysis(property_type_filter)

def run_property_performance_analysis(property_type_filter):
    """Run property performance analysis"""
    with st.spinner("Analyzing property performance..."):
        try:
            results = st.session_state.data_analyzer.analyze_property_performance()
            
            if "error" in results:
                st.error(f"Analysis error: {results['error']}")
                return
            
            # Display results
            st.success("✅ Property performance analysis completed!")
            
            # Overall metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Sales", results['total_sales'])
            
            with col2:
                avg_price = results['overall_metrics']['avg_sale_price']
                st.metric("Average Sale Price", f"${avg_price:,.0f}")
            
            with col3:
                avg_days = results['overall_metrics']['avg_days_on_market']
                st.metric("Average Days on Market", f"{avg_days:.0f}")
            
            # Property type performance
            if 'property_type_performance' in results:
                st.subheader("📊 Performance by Property Type")
                
                type_data = []
                for prop_type, metrics in results['property_type_performance'].items():
                    type_data.append({
                        'Property Type': prop_type,
                        'Average Price': f"${metrics['avg_price']:,.0f}",
                        'Sales Count': metrics['sales_count'],
                        'Avg Days on Market': f"{metrics['avg_days_on_market']:.0f}"
                    })
                
                type_df = pd.DataFrame(type_data)
                st.dataframe(type_df, use_container_width=True)
                
                # Visualization
                fig = make_subplots(
                    rows=1, cols=2,
                    subplot_titles=('Average Price by Type', 'Sales Count by Type')
                )
                
                prop_types = [item['Property Type'] for item in type_data]
                avg_prices = [float(item['Average Price'].replace('$', '').replace(',', '')) for item in type_data]
                sales_counts = [item['Sales Count'] for item in type_data]
                
                fig.add_trace(
                    go.Bar(x=prop_types, y=avg_prices, name='Avg Price'),
                    row=1, col=1
                )
                
                fig.add_trace(
                    go.Bar(x=prop_types, y=sales_counts, name='Sales Count', marker_color='lightblue'),
                    row=1, col=2
                )
                
                fig.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            
            # Price correlations
            if 'price_correlations' in results:
                st.subheader("🔗 Price Correlations")
                
                corr_data = []
                for feature, correlation in results['price_correlations'].items():
                    corr_data.append({
                        'Feature': feature.replace('_', ' ').title(),
                        'Correlation': f"{correlation:.3f}",
                        'Strength': 'Strong' if abs(correlation) > 0.5 else 'Moderate' if abs(correlation) > 0.3 else 'Weak'
                    })
                
                corr_df = pd.DataFrame(corr_data)
                st.dataframe(corr_df, use_container_width=True)
            
        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")

def rental_analysis():
    """Rental analysis interface"""
    st.subheader("🏢 Rental Analysis")
    
    if st.button("Run Rental Analysis", type="primary"):
        run_rental_analysis()

def run_rental_analysis():
    """Run rental analysis"""
    with st.spinner("Analyzing rental performance..."):
        try:
            results = st.session_state.data_analyzer.analyze_rental_performance()
            
            if "error" in results:
                st.warning(f"Analysis note: {results.get('note', results['error'])}")
                # Show sample data if no real rental data
                if 'overall_metrics' in results:
                    display_rental_results(results)
                return
            
            display_rental_results(results)
            
        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")

def display_rental_results(results):
    """Display rental analysis results"""
    st.success("✅ Rental analysis completed!")
    
    # Overall metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Rentals", results['total_rentals'])
    
    with col2:
        avg_rent = results['overall_metrics']['avg_monthly_rent']
        st.metric("Average Monthly Rent", f"${avg_rent:,.0f}")
    
    with col3:
        occupancy = results['overall_metrics']['occupancy_rate']
        st.metric("Occupancy Rate", f"{occupancy:.1%}")
    
    # Additional metrics if available
    if 'avg_rent_per_sqft' in results['overall_metrics']:
        col1, col2 = st.columns(2)
        
        with col1:
            rent_per_sqft = results['overall_metrics']['avg_rent_per_sqft']
            st.metric("Rent per Sq Ft", f"${rent_per_sqft:.2f}")
        
        with col2:
            lease_duration = results['overall_metrics']['avg_lease_duration']
            st.metric("Avg Lease Duration", f"{lease_duration:.0f} days")

def investment_analysis():
    """Investment analysis interface"""
    st.subheader("💰 Investment Analysis")
    
    with st.form("investment_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            purchase_price = st.number_input("Purchase Price ($)", value=500000, min_value=0)
            monthly_rent = st.number_input("Monthly Rent ($)", value=2500, min_value=0)
            annual_expenses = st.number_input("Annual Expenses ($)", value=10000, min_value=0)
        
        with col2:
            down_payment_percent = st.slider("Down Payment (%)", 0, 100, 20) / 100
            interest_rate = st.slider("Interest Rate (%)", 0.0, 10.0, 6.0) / 100
            loan_term_years = st.slider("Loan Term (years)", 1, 30, 30)
        
        if st.form_submit_button("Analyze Investment", type="primary"):
            run_investment_analysis({
                'purchase_price': purchase_price,
                'monthly_rent': monthly_rent,
                'annual_expenses': annual_expenses,
                'down_payment_percent': down_payment_percent,
                'interest_rate': interest_rate,
                'loan_term_years': loan_term_years
            })

def run_investment_analysis(property_data):
    """Run investment analysis"""
    with st.spinner("Analyzing investment..."):
        try:
            results = st.session_state.data_analyzer.generate_investment_analysis(property_data)
            
            st.success("✅ Investment analysis completed!")
            
            # Investment grade
            grade = results['investment_grade']
            grade_color = {
                'Excellent': 'green',
                'Good': 'blue',
                'Fair': 'orange',
                'Poor': 'red'
            }.get(grade, 'gray')
            
            st.markdown(f"### Investment Grade: <span style='color: {grade_color}'>{grade}</span>", unsafe_allow_html=True)
            
            # Key metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                cap_rate = results['investment_metrics']['cap_rate']
                st.metric("Cap Rate", f"{cap_rate:.1%}")
            
            with col2:
                cash_return = results['investment_metrics']['cash_on_cash_return']
                st.metric("Cash-on-Cash Return", f"{cash_return:.1%}")
            
            with col3:
                annual_cash_flow = results['cash_flow_analysis']['annual_cash_flow']
                st.metric("Annual Cash Flow", f"${annual_cash_flow:,.0f}")
            
            # Cash flow breakdown
            st.subheader("💰 Cash Flow Analysis")
            
            cash_flow = results['cash_flow_analysis']
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Income:**")
                st.write(f"Annual Rental Income: ${cash_flow['annual_rental_income']:,.0f}")
                
                st.write("**Expenses:**")
                st.write(f"Annual Expenses: ${cash_flow['annual_expenses']:,.0f}")
                st.write(f"Annual Debt Service: ${cash_flow['annual_debt_service']:,.0f}")
            
            with col2:
                # Cash flow chart
                categories = ['Rental Income', 'Expenses', 'Debt Service', 'Net Cash Flow']
                values = [
                    cash_flow['annual_rental_income'],
                    -cash_flow['annual_expenses'],
                    -cash_flow['annual_debt_service'],
                    cash_flow['annual_cash_flow']
                ]
                colors = ['green', 'red', 'red', 'blue' if values[3] > 0 else 'red']
                
                fig = go.Figure(data=[
                    go.Bar(x=categories, y=values, marker_color=colors)
                ])
                
                fig.update_layout(
                    title="Annual Cash Flow Breakdown",
                    yaxis_title="Amount ($)",
                    height=300
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Investment summary
            st.subheader("📋 Investment Summary")
            
            summary_data = {
                'Metric': ['Purchase Price', 'Down Payment', 'Loan Amount', 'Monthly Payment', 'Total Cash Required'],
                'Value': [
                    f"${property_data['purchase_price']:,.0f}",
                    f"${property_data['purchase_price'] * property_data['down_payment_percent']:,.0f}",
                    f"${property_data['purchase_price'] * (1 - property_data['down_payment_percent']):,.0f}",
                    f"${cash_flow['monthly_debt_service']:,.0f}",
                    f"${property_data['purchase_price'] * property_data['down_payment_percent']:,.0f}"
                ]
            }
            
            summary_df = pd.DataFrame(summary_data)
            st.dataframe(summary_df, use_container_width=True, hide_index=True)
            
        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")

def reports_tab():
    """Reports interface"""
    st.header("📋 Reports & Export")
    
    if not st.session_state.data_analyzer:
        st.warning("Please initialize the framework first!")
        return
    
    # Report generation
    st.subheader("📄 Generate Reports")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        report_type = st.selectbox(
            "Select Report Type",
            ["Comprehensive Market Report", "KPI Summary Report", "A/B Test Results Report"]
        )
        
        region_filter = st.text_input("Region Filter (optional)", placeholder="Enter region name", key="reports_region_filter")
    
    with col2:
        st.write("")  # Spacing
        st.write("")  # Spacing
        if st.button("Generate Report", type="primary"):
            generate_report(report_type, region_filter)
    
    # Export options
    st.subheader("📤 Export Data")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Export Properties Data", use_container_width=True):
            export_data("properties")
    
    with col2:
        if st.button("Export Market Data", use_container_width=True):
            export_data("market_data")
    
    with col3:
        if st.button("Export KPI Data", use_container_width=True):
            export_kpi_data()
    
    # Recent reports
    st.subheader("📁 Recent Reports")
    
    # List generated report files
    report_files = []
    if os.path.exists("./"):
        for file in os.listdir("./"):
            if file.endswith(('.json', '.csv')) and any(keyword in file for keyword in ['report', 'export', 'kpi']):
                report_files.append(file)
    
    if report_files:
        for file in sorted(report_files, reverse=True)[:10]:  # Show last 10 files
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"📄 {file}")
            
            with col2:
                if st.button("Download", key=f"download_{file}"):
                    download_file(file)
    else:
        st.info("No reports generated yet.")

def generate_report(report_type, region_filter):
    """Generate a report"""
    with st.spinner(f"Generating {report_type.lower()}..."):
        try:
            if report_type == "Comprehensive Market Report":
                region = region_filter if region_filter else None
                report_path = st.session_state.data_analyzer.create_market_report(region=region)
                st.success(f"✅ Report generated: {report_path}")
                
                # Show report preview
                with open(report_path, 'r') as f:
                    report_data = json.load(f)
                
                st.subheader("📄 Report Preview")
                st.json(report_data)
            
            elif report_type == "KPI Summary Report":
                generate_kpi_summary_report()
            
            elif report_type == "A/B Test Results Report":
                generate_ab_test_report()
            
        except Exception as e:
            st.error(f"Report generation failed: {str(e)}")

def generate_kpi_summary_report():
    """Generate KPI summary report"""
    try:
        kpi_results = st.session_state.kpi_manager.calculate_all_kpis()
        
        report_data = {
            "report_type": "kpi_summary",
            "generated_at": datetime.now().isoformat(),
            "kpis": {}
        }
        
        for kpi_name, value in kpi_results.items():
            kpi = st.session_state.kpi_manager.kpis[kpi_name]
            report_data["kpis"][kpi_name] = {
                "current_value": float(value),
                "target_value": float(kpi.target_value),
                "unit": kpi.unit,
                "performance": kpi.get_performance_status(),
                "category": kpi.category.value
            }
        
        report_path = f"kpi_summary_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(report_path, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        st.success(f"✅ KPI summary report generated: {report_path}")
        st.json(report_data)
        
    except Exception as e:
        st.error(f"KPI report generation failed: {str(e)}")

def generate_ab_test_report():
    """Generate A/B test results report"""
    try:
        report_data = {
            "report_type": "ab_test_results",
            "generated_at": datetime.now().isoformat(),
            "tests": {}
        }
        
        for test_id, test in st.session_state.ab_test_manager.tests.items():
            results = test.get_current_results()
            report_data["tests"][test_id] = {
                "name": test.name,
                "status": test.status.value,
                "hypothesis": test.hypothesis,
                "results": results
            }
        
        report_path = f"ab_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(report_path, 'w') as f:
            json.dump(report_data, f, indent=2, default=str)
        
        st.success(f"✅ A/B test report generated: {report_path}")
        st.json(report_data)
        
    except Exception as e:
        st.error(f"A/B test report generation failed: {str(e)}")

def export_data(table_name):
    """Export data to CSV"""
    try:
        df = st.session_state.data_platform.load_data("default_database", table_name=table_name)
        
        if df is not None and not df.empty:
            export_path = f"{table_name}_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            df.to_csv(export_path, index=False)
            st.success(f"✅ Data exported: {export_path}")
        else:
            st.warning(f"No data available for {table_name}")
    
    except Exception as e:
        st.error(f"Export failed: {str(e)}")

def export_kpi_data():
    """Export KPI data"""
    try:
        kpi_results = st.session_state.kpi_manager.calculate_all_kpis()
        
        kpi_data = []
        for kpi_name, value in kpi_results.items():
            kpi = st.session_state.kpi_manager.kpis[kpi_name]
            kpi_data.append({
                'KPI Name': kpi_name,
                'Current Value': value,
                'Target Value': kpi.target_value,
                'Unit': kpi.unit,
                'Performance': kpi.get_performance_status(),
                'Category': kpi.category.value
            })
        
        kpi_df = pd.DataFrame(kpi_data)
        export_path = f"kpi_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        kpi_df.to_csv(export_path, index=False)
        
        st.success(f"✅ KPI data exported: {export_path}")
        
    except Exception as e:
        st.error(f"KPI export failed: {str(e)}")

def download_file(filename):
    """Handle file download"""
    try:
        with open(filename, 'rb') as f:
            file_data = f.read()
        
        st.download_button(
            label=f"Download {filename}",
            data=file_data,
            file_name=filename,
            mime='application/octet-stream'
        )
        
    except Exception as e:
        st.error(f"Download failed: {str(e)}")

def settings_tab():
    """Settings interface"""
    st.header("⚙️ Settings & Configuration")
    
    # Framework settings
    st.subheader("🔧 Framework Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Data Platform Settings**")
        
        if st.session_state.data_platform:
            platform_name = st.text_input("Platform Name", value=st.session_state.data_platform.platform_name, key="settings_platform_name")
            base_path = st.text_input("Base Path", value=st.session_state.data_platform.base_path, key="settings_base_path")
            
            if st.button("Update Platform Settings"):
                st.session_state.data_platform.platform_name = platform_name
                st.session_state.data_platform.base_path = base_path
                st.success("✅ Platform settings updated!")
        else:
            st.info("Initialize framework to configure platform settings")
    
    with col2:
        st.write("**Display Settings**")
        
        # Theme selection (placeholder - Streamlit handles themes)
        theme = st.selectbox("Theme", ["Auto", "Light", "Dark"])
        
        # Chart settings
        default_chart_height = st.slider("Default Chart Height", 300, 800, 400)
        
        # Update session state with settings
        st.session_state.chart_height = default_chart_height
    
    # System information
    st.subheader("ℹ️ System Information")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**Framework Status**")
        st.write(f"Platform: {'✅ Active' if st.session_state.data_platform else '❌ Inactive'}")
        st.write(f"Sample Data: {'✅ Generated' if st.session_state.sample_data_generated else '❌ Not Generated'}")
    
    with col2:
        st.write("**Component Status**")
        st.write(f"KPI Manager: {'✅ Active' if st.session_state.kpi_manager else '❌ Inactive'}")
        st.write(f"A/B Testing: {'✅ Active' if st.session_state.ab_test_manager else '❌ Inactive'}")
    
    with col3:
        st.write("**Data Status**")
        if st.session_state.data_platform:
            status = st.session_state.data_platform.get_platform_status()
            st.write(f"Data Sources: {len(st.session_state.data_platform.data_sources)}")
            st.write(f"Active Sources: {status['active_sources']}")
        else:
            st.write("No platform data available")
    
    # Reset options
    st.subheader("🔄 Reset Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Reset Sample Data", type="secondary"):
            reset_sample_data()
    
    with col2:
        if st.button("Reset All KPIs", type="secondary"):
            reset_kpis()
    
    with col3:
        if st.button("Reset Framework", type="secondary"):
            reset_framework()
    
    # About section
    st.subheader("ℹ️ About")
    
    st.markdown("""
    **Real Estate Analytics Framework v1.0**
    
    A comprehensive Python framework for real estate data analytics, featuring:
    - 📊 Data platform management
    - 📈 KPI tracking and monitoring
    - 🧪 A/B testing capabilities
    - 🔍 Advanced data analysis
    - 📋 Report generation
    - 🎨 Interactive visualizations
    
    Built with Streamlit, Plotly, and Pandas for modern real estate analytics.
    """)

def reset_sample_data():
    """Reset sample data"""
    try:
        if st.session_state.data_platform:
            # Clear existing data
            st.session_state.sample_data_generated = False
            st.success("✅ Sample data reset!")
            st.rerun()
        else:
            st.warning("No platform available to reset")
    except Exception as e:
        st.error(f"Reset failed: {str(e)}")

def reset_kpis():
    """Reset KPIs"""
    try:
        if st.session_state.kpi_manager:
            # Reinitialize KPI manager
            st.session_state.kpi_manager = KPIManager(st.session_state.data_platform)
            st.success("✅ KPIs reset to defaults!")
            st.rerun()
        else:
            st.warning("No KPI manager available to reset")
    except Exception as e:
        st.error(f"KPI reset failed: {str(e)}")

def reset_framework():
    """Reset entire framework"""
    try:
        # Clear all session state
        for key in list(st.session_state.keys()):
            if key.startswith(('data_platform', 'kpi_manager', 'ab_test_manager', 'data_analyzer', 'client', 'provider', 'service_request', 'sample_data_generated')):
                del st.session_state[key]
        
        st.success("✅ Framework reset! Please reinitialize.")
        st.rerun()
        
    except Exception as e:
        st.error(f"Framework reset failed: {str(e)}")

if __name__ == "__main__":
    main()
