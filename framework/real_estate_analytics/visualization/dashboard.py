"""Dashboard creation and management for real estate analytics"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import dash
from dash import dcc, html, Input, Output, callback
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import os


class DashboardBuilder:
    """Creates interactive dashboards for real estate analytics"""
    
    def __init__(self, data_platform=None, kpi_manager=None, data_analyzer=None):
        self.data_platform = data_platform
        self.kpi_manager = kpi_manager
        self.data_analyzer = data_analyzer
        self.app = None
        self.dashboard_config = {}
        
    def create_executive_dashboard(self) -> dash.Dash:
        """Create an executive-level dashboard with key metrics"""
        self.app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
        
        # Dashboard layout
        self.app.layout = html.Div([
            html.H1("Real Estate Analytics Dashboard", style={'textAlign': 'center', 'marginBottom': 30}),
            
            # KPI Cards Row
            html.Div([
                html.Div([
                    html.H3("Key Performance Indicators", style={'textAlign': 'center'}),
                    html.Div(id='kpi-cards')
                ], className='twelve columns')
            ], className='row', style={'marginBottom': 30}),
            
            # Charts Row 1
            html.Div([
                html.Div([
                    dcc.Graph(id='price-trends-chart')
                ], className='six columns'),
                
                html.Div([
                    dcc.Graph(id='sales-performance-chart')
                ], className='six columns')
            ], className='row', style={'marginBottom': 30}),
            
            # Charts Row 2
            html.Div([
                html.Div([
                    dcc.Graph(id='property-type-distribution')
                ], className='six columns'),
                
                html.Div([
                    dcc.Graph(id='market-inventory-chart')
                ], className='six columns')
            ], className='row', style={'marginBottom': 30}),
            
            # Refresh interval
            dcc.Interval(
                id='interval-component',
                interval=60*1000,  # Update every minute
                n_intervals=0
            )
        ])
        
        # Register callbacks
        self._register_dashboard_callbacks()
        
        return self.app
    
    def create_property_analysis_dashboard(self) -> dash.Dash:
        """Create a dashboard focused on property analysis"""
        self.app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
        
        self.app.layout = html.Div([
            html.H1("Property Analysis Dashboard", style={'textAlign': 'center', 'marginBottom': 30}),
            
            # Filters
            html.Div([
                html.Div([
                    html.Label("Property Type:"),
                    dcc.Dropdown(
                        id='property-type-filter',
                        options=[
                            {'label': 'All Types', 'value': 'all'},
                            {'label': 'Single Family', 'value': 'Single Family'},
                            {'label': 'Condo', 'value': 'Condo'},
                            {'label': 'Townhouse', 'value': 'Townhouse'},
                            {'label': 'Multi-Family', 'value': 'Multi-Family'}
                        ],
                        value='all'
                    )
                ], className='four columns'),
                
                html.Div([
                    html.Label("Date Range:"),
                    dcc.DatePickerRange(
                        id='date-range-picker',
                        start_date=datetime.now() - timedelta(days=365),
                        end_date=datetime.now()
                    )
                ], className='four columns'),
                
                html.Div([
                    html.Label("Price Range:"),
                    dcc.RangeSlider(
                        id='price-range-slider',
                        min=0,
                        max=1000000,
                        step=50000,
                        value=[200000, 800000],
                        marks={i: f'${i//1000}K' for i in range(0, 1000001, 200000)}
                    )
                ], className='four columns')
            ], className='row', style={'marginBottom': 30}),
            
            # Analysis Charts
            html.Div([
                html.Div([
                    dcc.Graph(id='price-distribution-chart')
                ], className='six columns'),
                
                html.Div([
                    dcc.Graph(id='days-on-market-chart')
                ], className='six columns')
            ], className='row', style={'marginBottom': 30}),
            
            html.Div([
                html.Div([
                    dcc.Graph(id='price-vs-features-scatter')
                ], className='twelve columns')
            ], className='row')
        ])
        
        self._register_property_analysis_callbacks()
        
        return self.app
    
    def create_rental_dashboard(self) -> dash.Dash:
        """Create a dashboard for rental property analytics"""
        self.app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
        
        self.app.layout = html.Div([
            html.H1("Rental Property Dashboard", style={'textAlign': 'center', 'marginBottom': 30}),
            
            # Rental KPIs
            html.Div([
                html.Div(id='rental-kpi-cards')
            ], className='row', style={'marginBottom': 30}),
            
            # Rental Charts
            html.Div([
                html.Div([
                    dcc.Graph(id='occupancy-rate-chart')
                ], className='six columns'),
                
                html.Div([
                    dcc.Graph(id='rental-yield-chart')
                ], className='six columns')
            ], className='row', style={'marginBottom': 30}),
            
            html.Div([
                html.Div([
                    dcc.Graph(id='rent-vs-property-type')
                ], className='twelve columns')
            ], className='row')
        ])
        
        self._register_rental_dashboard_callbacks()
        
        return self.app
    
    def _register_dashboard_callbacks(self):
        """Register callbacks for the executive dashboard"""
        
        @self.app.callback(
            [Output('kpi-cards', 'children'),
             Output('price-trends-chart', 'figure'),
             Output('sales-performance-chart', 'figure'),
             Output('property-type-distribution', 'figure'),
             Output('market-inventory-chart', 'figure')],
            [Input('interval-component', 'n_intervals')]
        )
        def update_dashboard(n):
            # Update KPI cards
            kpi_cards = self._create_kpi_cards()
            
            # Create charts
            price_trends = self._create_price_trends_chart()
            sales_performance = self._create_sales_performance_chart()
            property_distribution = self._create_property_type_distribution()
            inventory_chart = self._create_inventory_chart()
            
            return kpi_cards, price_trends, sales_performance, property_distribution, inventory_chart
    
    def _register_property_analysis_callbacks(self):
        """Register callbacks for property analysis dashboard"""
        
        @self.app.callback(
            [Output('price-distribution-chart', 'figure'),
             Output('days-on-market-chart', 'figure'),
             Output('price-vs-features-scatter', 'figure')],
            [Input('property-type-filter', 'value'),
             Input('date-range-picker', 'start_date'),
             Input('date-range-picker', 'end_date'),
             Input('price-range-slider', 'value')]
        )
        def update_property_analysis(property_type, start_date, end_date, price_range):
            # Apply filters and create charts
            price_dist = self._create_price_distribution_chart(property_type, start_date, end_date, price_range)
            days_market = self._create_days_on_market_chart(property_type, start_date, end_date, price_range)
            price_features = self._create_price_vs_features_scatter(property_type, start_date, end_date, price_range)
            
            return price_dist, days_market, price_features
    
    def _register_rental_dashboard_callbacks(self):
        """Register callbacks for rental dashboard"""
        
        @self.app.callback(
            [Output('rental-kpi-cards', 'children'),
             Output('occupancy-rate-chart', 'figure'),
             Output('rental-yield-chart', 'figure'),
             Output('rent-vs-property-type', 'figure')],
            [Input('interval-component', 'n_intervals')]
        )
        def update_rental_dashboard(n):
            kpi_cards = self._create_rental_kpi_cards()
            occupancy_chart = self._create_occupancy_rate_chart()
            yield_chart = self._create_rental_yield_chart()
            rent_type_chart = self._create_rent_vs_property_type()
            
            return kpi_cards, occupancy_chart, yield_chart, rent_type_chart
    
    def _create_kpi_cards(self) -> List[html.Div]:
        """Create KPI cards for the dashboard"""
        if not self.kpi_manager:
            return [html.Div("KPI Manager not available")]
        
        # Get current KPI values
        kpi_data = self.kpi_manager.get_kpi_dashboard()
        cards = []
        
        for kpi_name, kpi_info in kpi_data.get('kpis', {}).items():
            # Determine card color based on performance
            performance = kpi_info.get('performance_status', 'no_target')
            if performance == 'exceeding':
                card_color = '#28a745'  # Green
            elif performance == 'meeting':
                card_color = '#17a2b8'  # Blue
            elif performance == 'below':
                card_color = '#ffc107'  # Yellow
            else:
                card_color = '#dc3545'  # Red
            
            card = html.Div([
                html.H4(kpi_name, style={'margin': '0', 'color': 'white'}),
                html.H2(f"{kpi_info.get('current_value', 0):.2f} {kpi_info.get('unit', '')}", 
                        style={'margin': '10px 0', 'color': 'white'}),
                html.P(f"Target: {kpi_info.get('target_value', 'N/A')}", 
                      style={'margin': '0', 'color': 'white', 'fontSize': '12px'})
            ], style={
                'backgroundColor': card_color,
                'padding': '20px',
                'margin': '10px',
                'borderRadius': '5px',
                'textAlign': 'center',
                'minWidth': '200px'
            })
            
            cards.append(card)
        
        return [html.Div(cards, style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'center'})]
    
    def _create_price_trends_chart(self) -> go.Figure:
        """Create price trends chart"""
        if not self.data_platform:
            return go.Figure().add_annotation(text="Data platform not available")
        
        # Get market data
        query = """
        SELECT date, AVG(median_price) as avg_price
        FROM market_data
        WHERE date >= ?
        GROUP BY date
        ORDER BY date
        """
        
        df = self.data_platform.load_data("default_database", query=query, 
                                         params=((datetime.now() - timedelta(days=365)).date(),))
        
        if df.empty:
            return go.Figure().add_annotation(text="No data available")
        
        df['date'] = pd.to_datetime(df['date'])
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['avg_price'],
            mode='lines+markers',
            name='Average Price',
            line=dict(color='#1f77b4', width=3)
        ))
        
        fig.update_layout(
            title='Price Trends Over Time',
            xaxis_title='Date',
            yaxis_title='Average Price ($)',
            hovermode='x unified'
        )
        
        return fig
    
    def _create_sales_performance_chart(self) -> go.Figure:
        """Create sales performance chart"""
        if not self.data_platform:
            return go.Figure().add_annotation(text="Data platform not available")
        
        query = """
        SELECT 
            strftime('%Y-%m', sale_date) as month,
            COUNT(*) as sales_count,
            AVG(days_on_market) as avg_days_on_market
        FROM properties
        WHERE sale_date IS NOT NULL
        AND sale_date >= ?
        GROUP BY strftime('%Y-%m', sale_date)
        ORDER BY month
        """
        
        df = self.data_platform.load_data("default_database", query=query,
                                         params=((datetime.now() - timedelta(days=365)).date(),))
        
        if df.empty:
            return go.Figure().add_annotation(text="No sales data available")
        
        # Create subplot with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Bar(x=df['month'], y=df['sales_count'], name="Sales Count"),
            secondary_y=False,
        )
        
        fig.add_trace(
            go.Scatter(x=df['month'], y=df['avg_days_on_market'], 
                      mode='lines+markers', name="Avg Days on Market"),
            secondary_y=True,
        )
        
        fig.update_xaxes(title_text="Month")
        fig.update_yaxes(title_text="Number of Sales", secondary_y=False)
        fig.update_yaxes(title_text="Average Days on Market", secondary_y=True)
        
        fig.update_layout(title_text="Sales Performance Over Time")
        
        return fig
    
    def _create_property_type_distribution(self) -> go.Figure:
        """Create property type distribution chart"""
        if not self.data_platform:
            return go.Figure().add_annotation(text="Data platform not available")
        
        query = """
        SELECT property_type, COUNT(*) as count
        FROM properties
        WHERE sale_date IS NOT NULL
        GROUP BY property_type
        """
        
        df = self.data_platform.load_data("default_database", query=query)
        
        if df.empty:
            return go.Figure().add_annotation(text="No property data available")
        
        fig = go.Figure(data=[go.Pie(
            labels=df['property_type'],
            values=df['count'],
            hole=0.3
        )])
        
        fig.update_layout(title_text="Property Type Distribution")
        
        return fig
    
    def _create_inventory_chart(self) -> go.Figure:
        """Create market inventory chart"""
        if not self.data_platform:
            return go.Figure().add_annotation(text="Data platform not available")
        
        query = """
        SELECT date, AVG(inventory_count) as avg_inventory
        FROM market_data
        WHERE date >= ?
        GROUP BY date
        ORDER BY date
        """
        
        df = self.data_platform.load_data("default_database", query=query,
                                         params=((datetime.now() - timedelta(days=180)).date(),))
        
        if df.empty:
            return go.Figure().add_annotation(text="No inventory data available")
        
        df['date'] = pd.to_datetime(df['date'])
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['avg_inventory'],
            mode='lines+markers',
            name='Market Inventory',
            fill='tonexty',
            line=dict(color='#ff7f0e')
        ))
        
        fig.update_layout(
            title='Market Inventory Levels',
            xaxis_title='Date',
            yaxis_title='Average Inventory Count'
        )
        
        return fig
    
    def _create_rental_kpi_cards(self) -> List[html.Div]:
        """Create rental-specific KPI cards"""
        if not self.data_analyzer:
            return [html.Div("Data analyzer not available")]
        
        rental_analysis = self.data_analyzer.analyze_rental_performance()
        
        if "error" in rental_analysis:
            return [html.Div(rental_analysis["error"])]
        
        metrics = rental_analysis.get("overall_metrics", {})
        
        cards = [
            self._create_metric_card("Avg Monthly Rent", f"${metrics.get('avg_monthly_rent', 0):,.0f}", "#28a745"),
            self._create_metric_card("Occupancy Rate", f"{metrics.get('occupancy_rate', 0)*100:.1f}%", "#17a2b8"),
            self._create_metric_card("Avg Rent/SqFt", f"${metrics.get('avg_rent_per_sqft', 0):.2f}", "#ffc107"),
            self._create_metric_card("Avg Lease Duration", f"{metrics.get('avg_lease_duration', 0):.0f} days", "#6f42c1")
        ]
        
        return [html.Div(cards, style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'center'})]
    
    def _create_metric_card(self, title: str, value: str, color: str) -> html.Div:
        """Create a metric card"""
        return html.Div([
            html.H4(title, style={'margin': '0', 'color': 'white'}),
            html.H2(value, style={'margin': '10px 0', 'color': 'white'})
        ], style={
            'backgroundColor': color,
            'padding': '20px',
            'margin': '10px',
            'borderRadius': '5px',
            'textAlign': 'center',
            'minWidth': '200px'
        })
    
    def run_dashboard(self, dashboard_type: str = "executive", host: str = "127.0.0.1", port: int = 8050, debug: bool = True):
        """Run the dashboard server"""
        if dashboard_type == "executive":
            app = self.create_executive_dashboard()
        elif dashboard_type == "property":
            app = self.create_property_analysis_dashboard()
        elif dashboard_type == "rental":
            app = self.create_rental_dashboard()
        else:
            raise ValueError("Invalid dashboard type. Choose from: executive, property, rental")
        
        app.run_server(host=host, port=port, debug=debug)
    
    def export_dashboard_config(self, file_path: str = None) -> str:
        """Export dashboard configuration"""
        if not file_path:
            file_path = f"dashboard_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        config = {
            "dashboard_type": "real_estate_analytics",
            "created_at": datetime.now().isoformat(),
            "components": {
                "kpi_cards": True,
                "price_trends": True,
                "sales_performance": True,
                "property_distribution": True,
                "inventory_tracking": True
            },
            "data_sources": list(self.data_platform.data_sources.keys()) if self.data_platform else [],
            "refresh_interval": 60
        }
        
        with open(file_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        return file_path

