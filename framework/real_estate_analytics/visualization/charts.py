"""Chart generation utilities for real estate analytics"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
import os


class ChartGenerator:
    """Generates various charts for real estate analytics"""
    
    def __init__(self, data_platform=None, style: str = "plotly"):
        self.data_platform = data_platform
        self.style = style  # "plotly" or "matplotlib"
        self.color_palette = [
            '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
            '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
        ]
        
        # Set up matplotlib style
        if style == "matplotlib":
            plt.style.use('seaborn-v0_8')
            sns.set_palette("husl")
    
    def create_price_trend_chart(self, region: str = None, save_path: str = None) -> str:
        """Create a price trend chart"""
        if not self.data_platform:
            raise ValueError("Data platform not available")
        
        # Query data
        query = """
        SELECT date, region, median_price
        FROM market_data
        WHERE date >= date('now', '-12 months')
        """
        
        if region:
            query += " AND region = ?"
            params = (region,)
        else:
            params = None
        
        df = self.data_platform.load_data("default_database", query=query, params=params)
        
        if df.empty:
            raise ValueError("No data available for price trend chart")
        
        df['date'] = pd.to_datetime(df['date'])
        
        if self.style == "plotly":
            fig = self._create_plotly_price_trend(df, region)
            if not save_path:
                save_path = f"price_trend_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            fig.write_html(save_path)
        else:
            fig = self._create_matplotlib_price_trend(df, region)
            if not save_path:
                save_path = f"price_trend_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            fig.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close(fig)
        
        return save_path
    
    def create_property_performance_chart(self, property_type: str = None, save_path: str = None) -> str:
        """Create a property performance comparison chart"""
        if not self.data_platform:
            raise ValueError("Data platform not available")
        
        query = """
        SELECT property_type, 
               AVG(sale_price) as avg_price,
               AVG(days_on_market) as avg_days_on_market,
               COUNT(*) as sales_count
        FROM properties
        WHERE sale_date IS NOT NULL
        """
        
        if property_type:
            query += " AND property_type = ?"
            params = (property_type,)
        else:
            params = None
        
        query += " GROUP BY property_type"
        
        df = self.data_platform.load_data("default_database", query=query, params=params)
        
        if df.empty:
            raise ValueError("No data available for property performance chart")
        
        if self.style == "plotly":
            fig = self._create_plotly_property_performance(df)
            if not save_path:
                save_path = f"property_performance_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            fig.write_html(save_path)
        else:
            fig = self._create_matplotlib_property_performance(df)
            if not save_path:
                save_path = f"property_performance_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            fig.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close(fig)
        
        return save_path
    
    def create_rental_analysis_chart(self, save_path: str = None) -> str:
        """Create rental property analysis chart"""
        if not self.data_platform:
            raise ValueError("Data platform not available")
        
        query = """
        SELECT r.monthly_rent, r.occupancy_status, p.property_type, p.square_feet
        FROM rental_properties r
        JOIN properties p ON r.property_id = p.id
        """
        
        df = self.data_platform.load_data("default_database", query=query)
        
        if df.empty:
            raise ValueError("No rental data available")
        
        df['rent_per_sqft'] = df['monthly_rent'] / df['square_feet']
        
        if self.style == "plotly":
            fig = self._create_plotly_rental_analysis(df)
            if not save_path:
                save_path = f"rental_analysis_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            fig.write_html(save_path)
        else:
            fig = self._create_matplotlib_rental_analysis(df)
            if not save_path:
                save_path = f"rental_analysis_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            fig.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close(fig)
        
        return save_path
    
    def create_market_comparison_chart(self, regions: List[str] = None, save_path: str = None) -> str:
        """Create market comparison chart across regions"""
        if not self.data_platform:
            raise ValueError("Data platform not available")
        
        query = """
        SELECT region, 
               AVG(median_price) as avg_price,
               AVG(average_days_on_market) as avg_days_on_market,
               AVG(inventory_count) as avg_inventory
        FROM market_data
        WHERE date >= date('now', '-3 months')
        """
        
        if regions:
            placeholders = ','.join(['?' for _ in regions])
            query += f" AND region IN ({placeholders})"
            params = tuple(regions)
        else:
            params = None
        
        query += " GROUP BY region"
        
        df = self.data_platform.load_data("default_database", query=query, params=params)
        
        if df.empty:
            raise ValueError("No market data available for comparison")
        
        if self.style == "plotly":
            fig = self._create_plotly_market_comparison(df)
            if not save_path:
                save_path = f"market_comparison_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            fig.write_html(save_path)
        else:
            fig = self._create_matplotlib_market_comparison(df)
            if not save_path:
                save_path = f"market_comparison_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            fig.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close(fig)
        
        return save_path
    
    def create_kpi_dashboard_chart(self, kpi_manager, save_path: str = None) -> str:
        """Create a KPI dashboard chart"""
        if not kpi_manager:
            raise ValueError("KPI manager not available")
        
        kpi_data = kpi_manager.get_kpi_dashboard()
        
        if not kpi_data.get('kpis'):
            raise ValueError("No KPI data available")
        
        if self.style == "plotly":
            fig = self._create_plotly_kpi_dashboard(kpi_data)
            if not save_path:
                save_path = f"kpi_dashboard_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            fig.write_html(save_path)
        else:
            fig = self._create_matplotlib_kpi_dashboard(kpi_data)
            if not save_path:
                save_path = f"kpi_dashboard_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            fig.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close(fig)
        
        return save_path
    
    def create_ab_test_results_chart(self, ab_test, save_path: str = None) -> str:
        """Create A/B test results chart"""
        if not ab_test:
            raise ValueError("A/B test data not available")
        
        results = ab_test.get_current_results()
        
        if self.style == "plotly":
            fig = self._create_plotly_ab_test_results(results)
            if not save_path:
                save_path = f"ab_test_results_{ab_test.test_id[:8]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            fig.write_html(save_path)
        else:
            fig = self._create_matplotlib_ab_test_results(results)
            if not save_path:
                save_path = f"ab_test_results_{ab_test.test_id[:8]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            fig.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close(fig)
        
        return save_path
    
    # Plotly chart creation methods
    def _create_plotly_price_trend(self, df: pd.DataFrame, region: str = None) -> go.Figure:
        """Create Plotly price trend chart"""
        if region:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df['date'],
                y=df['median_price'],
                mode='lines+markers',
                name=f'{region} Median Price',
                line=dict(color=self.color_palette[0], width=3)
            ))
            title = f'Price Trends - {region}'
        else:
            fig = go.Figure()
            for i, reg in enumerate(df['region'].unique()):
                reg_data = df[df['region'] == reg]
                fig.add_trace(go.Scatter(
                    x=reg_data['date'],
                    y=reg_data['median_price'],
                    mode='lines+markers',
                    name=f'{reg} Median Price',
                    line=dict(color=self.color_palette[i % len(self.color_palette)], width=2)
                ))
            title = 'Price Trends by Region'
        
        fig.update_layout(
            title=title,
            xaxis_title='Date',
            yaxis_title='Median Price ($)',
            hovermode='x unified',
            template='plotly_white'
        )
        
        return fig
    
    def _create_plotly_property_performance(self, df: pd.DataFrame) -> go.Figure:
        """Create Plotly property performance chart"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Average Sale Price', 'Average Days on Market', 
                          'Sales Count', 'Price vs Days on Market'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Average sale price
        fig.add_trace(
            go.Bar(x=df['property_type'], y=df['avg_price'], name='Avg Price',
                  marker_color=self.color_palette[0]),
            row=1, col=1
        )
        
        # Average days on market
        fig.add_trace(
            go.Bar(x=df['property_type'], y=df['avg_days_on_market'], name='Avg Days',
                  marker_color=self.color_palette[1]),
            row=1, col=2
        )
        
        # Sales count
        fig.add_trace(
            go.Bar(x=df['property_type'], y=df['sales_count'], name='Sales Count',
                  marker_color=self.color_palette[2]),
            row=2, col=1
        )
        
        # Scatter plot: price vs days on market
        fig.add_trace(
            go.Scatter(x=df['avg_days_on_market'], y=df['avg_price'], 
                      mode='markers+text', text=df['property_type'],
                      textposition='top center', name='Price vs Days',
                      marker=dict(size=df['sales_count']*2, color=self.color_palette[3])),
            row=2, col=2
        )
        
        fig.update_layout(
            title_text="Property Performance Analysis",
            showlegend=False,
            height=800,
            template='plotly_white'
        )
        
        return fig
    
    def _create_plotly_rental_analysis(self, df: pd.DataFrame) -> go.Figure:
        """Create Plotly rental analysis chart"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Rent by Property Type', 'Occupancy Status', 
                          'Rent per Sq Ft Distribution', 'Rent vs Square Feet'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Average rent by property type
        avg_rent_by_type = df.groupby('property_type')['monthly_rent'].mean()
        fig.add_trace(
            go.Bar(x=avg_rent_by_type.index, y=avg_rent_by_type.values, 
                  name='Avg Rent', marker_color=self.color_palette[0]),
            row=1, col=1
        )
        
        # Occupancy status pie chart
        occupancy_counts = df['occupancy_status'].value_counts()
        fig.add_trace(
            go.Pie(labels=occupancy_counts.index, values=occupancy_counts.values,
                  name='Occupancy'),
            row=1, col=2
        )
        
        # Rent per sq ft histogram
        fig.add_trace(
            go.Histogram(x=df['rent_per_sqft'], name='Rent/SqFt Distribution',
                        marker_color=self.color_palette[2]),
            row=2, col=1
        )
        
        # Scatter: rent vs square feet
        fig.add_trace(
            go.Scatter(x=df['square_feet'], y=df['monthly_rent'], 
                      mode='markers', name='Rent vs SqFt',
                      marker=dict(color=self.color_palette[3])),
            row=2, col=2
        )
        
        fig.update_layout(
            title_text="Rental Property Analysis",
            height=800,
            template='plotly_white'
        )
        
        return fig
    
    def _create_plotly_market_comparison(self, df: pd.DataFrame) -> go.Figure:
        """Create Plotly market comparison chart"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Average Price by Region', 'Days on Market by Region',
                          'Inventory Levels', 'Market Overview'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": True}]]
        )
        
        # Average price by region
        fig.add_trace(
            go.Bar(x=df['region'], y=df['avg_price'], name='Avg Price',
                  marker_color=self.color_palette[0]),
            row=1, col=1
        )
        
        # Days on market by region
        fig.add_trace(
            go.Bar(x=df['region'], y=df['avg_days_on_market'], name='Avg Days',
                  marker_color=self.color_palette[1]),
            row=1, col=2
        )
        
        # Inventory levels
        fig.add_trace(
            go.Bar(x=df['region'], y=df['avg_inventory'], name='Inventory',
                  marker_color=self.color_palette[2]),
            row=2, col=1
        )
        
        # Market overview (price and days on market)
        fig.add_trace(
            go.Bar(x=df['region'], y=df['avg_price'], name='Price',
                  marker_color=self.color_palette[0], opacity=0.7),
            row=2, col=2
        )
        
        fig.add_trace(
            go.Scatter(x=df['region'], y=df['avg_days_on_market'], 
                      mode='lines+markers', name='Days on Market',
                      line=dict(color=self.color_palette[1], width=3)),
            row=2, col=2, secondary_y=True
        )
        
        fig.update_layout(
            title_text="Market Comparison Analysis",
            height=800,
            template='plotly_white'
        )
        
        return fig
    
    def _create_plotly_kpi_dashboard(self, kpi_data: Dict[str, Any]) -> go.Figure:
        """Create Plotly KPI dashboard chart"""
        kpis = kpi_data.get('kpis', {})
        
        if not kpis:
            return go.Figure().add_annotation(text="No KPI data available")
        
        # Extract KPI names, current values, and target values
        names = list(kpis.keys())
        current_values = [kpi.get('current_value', 0) for kpi in kpis.values()]
        target_values = [kpi.get('target_value', 0) for kpi in kpis.values()]
        
        fig = go.Figure()
        
        # Current values
        fig.add_trace(go.Bar(
            x=names,
            y=current_values,
            name='Current Value',
            marker_color=self.color_palette[0]
        ))
        
        # Target values
        fig.add_trace(go.Bar(
            x=names,
            y=target_values,
            name='Target Value',
            marker_color=self.color_palette[1],
            opacity=0.6
        ))
        
        fig.update_layout(
            title='KPI Dashboard - Current vs Target',
            xaxis_title='KPIs',
            yaxis_title='Values',
            barmode='group',
            template='plotly_white'
        )
        
        return fig
    
    def _create_plotly_ab_test_results(self, results: Dict[str, Any]) -> go.Figure:
        """Create Plotly A/B test results chart"""
        variants = results.get('variants', [])
        
        if not variants:
            return go.Figure().add_annotation(text="No A/B test data available")
        
        names = [v['name'] for v in variants]
        conversion_rates = [v['conversion_rate'] for v in variants]
        participants = [v['participants'] for v in variants]
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Conversion Rates', 'Participants'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Conversion rates
        fig.add_trace(
            go.Bar(x=names, y=conversion_rates, name='Conversion Rate',
                  marker_color=self.color_palette[0]),
            row=1, col=1
        )
        
        # Participants
        fig.add_trace(
            go.Bar(x=names, y=participants, name='Participants',
                  marker_color=self.color_palette[1]),
            row=1, col=2
        )
        
        fig.update_layout(
            title_text=f"A/B Test Results: {results.get('test_name', 'Unknown Test')}",
            template='plotly_white'
        )
        
        return fig
    
    # Matplotlib chart creation methods (simplified versions)
    def _create_matplotlib_price_trend(self, df: pd.DataFrame, region: str = None) -> plt.Figure:
        """Create matplotlib price trend chart"""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        if region:
            ax.plot(df['date'], df['median_price'], marker='o', linewidth=2, label=f'{region} Median Price')
            title = f'Price Trends - {region}'
        else:
            for i, reg in enumerate(df['region'].unique()):
                reg_data = df[df['region'] == reg]
                ax.plot(reg_data['date'], reg_data['median_price'], 
                       marker='o', linewidth=2, label=f'{reg} Median Price')
            title = 'Price Trends by Region'
        
        ax.set_title(title, fontsize=16, fontweight='bold')
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Median Price ($)', fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        return fig
    
    def _create_matplotlib_property_performance(self, df: pd.DataFrame) -> plt.Figure:
        """Create matplotlib property performance chart"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        # Average sale price
        ax1.bar(df['property_type'], df['avg_price'], color=self.color_palette[0])
        ax1.set_title('Average Sale Price')
        ax1.set_ylabel('Price ($)')
        
        # Average days on market
        ax2.bar(df['property_type'], df['avg_days_on_market'], color=self.color_palette[1])
        ax2.set_title('Average Days on Market')
        ax2.set_ylabel('Days')
        
        # Sales count
        ax3.bar(df['property_type'], df['sales_count'], color=self.color_palette[2])
        ax3.set_title('Sales Count')
        ax3.set_ylabel('Count')
        
        # Scatter plot
        ax4.scatter(df['avg_days_on_market'], df['avg_price'], 
                   s=df['sales_count']*10, alpha=0.6, color=self.color_palette[3])
        ax4.set_title('Price vs Days on Market')
        ax4.set_xlabel('Days on Market')
        ax4.set_ylabel('Price ($)')
        
        plt.tight_layout()
        return fig
    
    def _create_matplotlib_rental_analysis(self, df: pd.DataFrame) -> plt.Figure:
        """Create matplotlib rental analysis chart"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        # Average rent by property type
        avg_rent = df.groupby('property_type')['monthly_rent'].mean()
        ax1.bar(avg_rent.index, avg_rent.values, color=self.color_palette[0])
        ax1.set_title('Average Rent by Property Type')
        ax1.set_ylabel('Monthly Rent ($)')
        
        # Occupancy status
        occupancy_counts = df['occupancy_status'].value_counts()
        ax2.pie(occupancy_counts.values, labels=occupancy_counts.index, autopct='%1.1f%%')
        ax2.set_title('Occupancy Status')
        
        # Rent per sq ft distribution
        ax3.hist(df['rent_per_sqft'], bins=20, color=self.color_palette[2], alpha=0.7)
        ax3.set_title('Rent per Sq Ft Distribution')
        ax3.set_xlabel('Rent per Sq Ft ($)')
        ax3.set_ylabel('Frequency')
        
        # Scatter plot
        ax4.scatter(df['square_feet'], df['monthly_rent'], alpha=0.6, color=self.color_palette[3])
        ax4.set_title('Rent vs Square Feet')
        ax4.set_xlabel('Square Feet')
        ax4.set_ylabel('Monthly Rent ($)')
        
        plt.tight_layout()
        return fig
    
    def _create_matplotlib_market_comparison(self, df: pd.DataFrame) -> plt.Figure:
        """Create matplotlib market comparison chart"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        # Average price by region
        ax1.bar(df['region'], df['avg_price'], color=self.color_palette[0])
        ax1.set_title('Average Price by Region')
        ax1.set_ylabel('Price ($)')
        
        # Days on market by region
        ax2.bar(df['region'], df['avg_days_on_market'], color=self.color_palette[1])
        ax2.set_title('Days on Market by Region')
        ax2.set_ylabel('Days')
        
        # Inventory levels
        ax3.bar(df['region'], df['avg_inventory'], color=self.color_palette[2])
        ax3.set_title('Inventory Levels')
        ax3.set_ylabel('Inventory Count')
        
        # Market overview
        ax4_twin = ax4.twinx()
        ax4.bar(df['region'], df['avg_price'], alpha=0.7, color=self.color_palette[0], label='Price')
        ax4_twin.plot(df['region'], df['avg_days_on_market'], 'ro-', color=self.color_palette[1], label='Days on Market')
        ax4.set_title('Market Overview')
        ax4.set_ylabel('Price ($)')
        ax4_twin.set_ylabel('Days on Market')
        
        plt.tight_layout()
        return fig
    
    def _create_matplotlib_kpi_dashboard(self, kpi_data: Dict[str, Any]) -> plt.Figure:
        """Create matplotlib KPI dashboard chart"""
        kpis = kpi_data.get('kpis', {})
        
        names = list(kpis.keys())
        current_values = [kpi.get('current_value', 0) for kpi in kpis.values()]
        target_values = [kpi.get('target_value', 0) for kpi in kpis.values()]
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        x = np.arange(len(names))
        width = 0.35
        
        ax.bar(x - width/2, current_values, width, label='Current Value', color=self.color_palette[0])
        ax.bar(x + width/2, target_values, width, label='Target Value', color=self.color_palette[1], alpha=0.6)
        
        ax.set_title('KPI Dashboard - Current vs Target')
        ax.set_xlabel('KPIs')
        ax.set_ylabel('Values')
        ax.set_xticks(x)
        ax.set_xticklabels(names, rotation=45, ha='right')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def _create_matplotlib_ab_test_results(self, results: Dict[str, Any]) -> plt.Figure:
        """Create matplotlib A/B test results chart"""
        variants = results.get('variants', [])
        
        names = [v['name'] for v in variants]
        conversion_rates = [v['conversion_rate'] for v in variants]
        participants = [v['participants'] for v in variants]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Conversion rates
        ax1.bar(names, conversion_rates, color=self.color_palette[0])
        ax1.set_title('Conversion Rates')
        ax1.set_ylabel('Conversion Rate')
        
        # Participants
        ax2.bar(names, participants, color=self.color_palette[1])
        ax2.set_title('Participants')
        ax2.set_ylabel('Number of Participants')
        
        fig.suptitle(f"A/B Test Results: {results.get('test_name', 'Unknown Test')}")
        plt.tight_layout()
        return fig

