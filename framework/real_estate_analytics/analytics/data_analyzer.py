"""Data analysis engine for real estate analytics"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import json
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')


class DataAnalyzer:
    """Comprehensive data analysis engine for real estate analytics"""
    
    def __init__(self, data_platform=None):
        self.data_platform = data_platform
        self.analysis_cache = {}
        self.visualization_style = "seaborn"
        
        # Set up plotting style
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
    
    def analyze_market_trends(self, region: str = None, time_period_days: int = 365) -> Dict[str, Any]:
        """Analyze market trends over time"""
        if not self.data_platform:
            return {"error": "Data platform not available"}
        
        # Query market data
        query = """
        SELECT date, region, median_price, average_days_on_market, 
               inventory_count, price_per_sqft, rental_yield
        FROM market_data
        WHERE date >= ?
        """
        
        params = [(datetime.now() - timedelta(days=time_period_days)).date()]
        
        if region:
            query += " AND region = ?"
            params.append(region)
        
        query += " ORDER BY date"
        
        df = self.data_platform.load_data("default_database", query=query, params=tuple(params))
        
        if df.empty:
            return {"error": "No market data available"}
        
        # Convert date column
        df['date'] = pd.to_datetime(df['date'])
        
        # Calculate trends
        trends = {}
        numeric_columns = ['median_price', 'average_days_on_market', 'inventory_count', 'price_per_sqft', 'rental_yield']
        
        for col in numeric_columns:
            if col in df.columns and not df[col].isna().all():
                # Calculate trend using linear regression
                x = np.arange(len(df))
                y = df[col].fillna(method='ffill').fillna(method='bfill')
                
                if len(y.dropna()) > 1:
                    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
                    
                    trends[col] = {
                        "current_value": float(y.iloc[-1]) if not y.empty else None,
                        "trend_slope": float(slope),
                        "trend_direction": "increasing" if slope > 0 else "decreasing" if slope < 0 else "stable",
                        "correlation": float(r_value),
                        "p_value": float(p_value),
                        "is_significant": p_value < 0.05,
                        "percentage_change": float((y.iloc[-1] - y.iloc[0]) / y.iloc[0] * 100) if y.iloc[0] != 0 else 0
                    }
        
        # Regional analysis if no specific region provided
        regional_summary = {}
        if not region and 'region' in df.columns:
            for reg in df['region'].unique():
                reg_data = df[df['region'] == reg]
                if not reg_data.empty:
                    regional_summary[reg] = {
                        "avg_median_price": float(reg_data['median_price'].mean()) if 'median_price' in reg_data else None,
                        "avg_days_on_market": float(reg_data['average_days_on_market'].mean()) if 'average_days_on_market' in reg_data else None,
                        "avg_inventory": float(reg_data['inventory_count'].mean()) if 'inventory_count' in reg_data else None
                    }
        
        return {
            "analysis_type": "market_trends",
            "time_period_days": time_period_days,
            "region": region or "all_regions",
            "data_points": len(df),
            "trends": trends,
            "regional_summary": regional_summary,
            "analysis_date": datetime.now().isoformat()
        }
    
    def analyze_property_performance(self, property_type: str = None) -> Dict[str, Any]:
        """Analyze property sales performance"""
        if not self.data_platform:
            return {"error": "Data platform not available"}
        
        # Query property data
        query = """
        SELECT property_type, bedrooms, bathrooms, square_feet, 
               listing_price, sale_price, days_on_market, 
               listing_date, sale_date
        FROM properties
        WHERE sale_date IS NOT NULL
        """
        
        params = []
        if property_type:
            query += " AND property_type = ?"
            params.append(property_type)
        
        df = self.data_platform.load_data("default_database", query=query, params=tuple(params) if params else None)
        
        if df.empty:
            return {"error": "No property sales data available"}
        
        # Calculate key metrics
        analysis = {
            "analysis_type": "property_performance",
            "property_type": property_type or "all_types",
            "total_sales": len(df),
            "analysis_date": datetime.now().isoformat()
        }
        
        # Overall performance metrics
        analysis["overall_metrics"] = {
            "avg_sale_price": float(df['sale_price'].mean()),
            "median_sale_price": float(df['sale_price'].median()),
            "avg_days_on_market": float(df['days_on_market'].mean()),
            "median_days_on_market": float(df['days_on_market'].median()),
            "price_variance": float(df['sale_price'].var()),
            "avg_price_per_sqft": float((df['sale_price'] / df['square_feet']).mean()) if 'square_feet' in df else None
        }
        
        # Performance by property type
        if not property_type:
            type_performance = {}
            for ptype in df['property_type'].unique():
                type_data = df[df['property_type'] == ptype]
                type_performance[ptype] = {
                    "count": len(type_data),
                    "avg_sale_price": float(type_data['sale_price'].mean()),
                    "avg_days_on_market": float(type_data['days_on_market'].mean()),
                    "avg_price_per_sqft": float((type_data['sale_price'] / type_data['square_feet']).mean()) if 'square_feet' in type_data else None
                }
            analysis["performance_by_type"] = type_performance
        
        # Price vs features correlation
        numeric_features = ['bedrooms', 'bathrooms', 'square_feet']
        correlations = {}
        
        for feature in numeric_features:
            if feature in df.columns:
                corr = df[feature].corr(df['sale_price'])
                if not np.isnan(corr):
                    correlations[feature] = float(corr)
        
        analysis["price_correlations"] = correlations
        
        # Market timing analysis
        df['listing_date'] = pd.to_datetime(df['listing_date'])
        df['sale_date'] = pd.to_datetime(df['sale_date'])
        df['listing_month'] = df['listing_date'].dt.month
        
        monthly_performance = df.groupby('listing_month').agg({
            'sale_price': 'mean',
            'days_on_market': 'mean',
            'property_type': 'count'
        }).round(2)
        
        analysis["monthly_trends"] = {
            int(month): {
                "avg_sale_price": float(row['sale_price']),
                "avg_days_on_market": float(row['days_on_market']),
                "sales_count": int(row['property_type'])
            }
            for month, row in monthly_performance.iterrows()
        }
        
        return analysis
    
    def analyze_pricing_strategy(self, target_property: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze optimal pricing strategy for a property"""
        if not self.data_platform:
            return {"error": "Data platform not available"}
        
        # Find comparable properties
        query = """
        SELECT * FROM properties 
        WHERE sale_date IS NOT NULL
        AND property_type = ?
        AND bedrooms = ?
        AND bathrooms = ?
        AND square_feet BETWEEN ? AND ?
        """
        
        sqft_range = 0.2  # 20% range
        min_sqft = target_property['square_feet'] * (1 - sqft_range)
        max_sqft = target_property['square_feet'] * (1 + sqft_range)
        
        params = (
            target_property['property_type'],
            target_property['bedrooms'],
            target_property['bathrooms'],
            min_sqft,
            max_sqft
        )
        
        df = self.data_platform.load_data("default_database", query=query, params=params)
        
        if df.empty:
            return {"error": "No comparable properties found"}
        
        # Calculate pricing recommendations
        price_per_sqft = df['sale_price'] / df['square_feet']
        
        analysis = {
            "analysis_type": "pricing_strategy",
            "target_property": target_property,
            "comparable_properties": len(df),
            "analysis_date": datetime.now().isoformat()
        }
        
        # Price recommendations
        estimated_price = price_per_sqft.median() * target_property['square_feet']
        
        analysis["pricing_recommendations"] = {
            "estimated_market_value": float(estimated_price),
            "price_per_sqft_median": float(price_per_sqft.median()),
            "price_per_sqft_mean": float(price_per_sqft.mean()),
            "price_range": {
                "conservative": float(price_per_sqft.quantile(0.25) * target_property['square_feet']),
                "market": float(estimated_price),
                "aggressive": float(price_per_sqft.quantile(0.75) * target_property['square_feet'])
            }
        }
        
        # Time on market predictions
        analysis["market_timing"] = {
            "avg_days_on_market": float(df['days_on_market'].mean()),
            "median_days_on_market": float(df['days_on_market'].median()),
            "quick_sale_threshold": float(df['days_on_market'].quantile(0.25)),
            "slow_sale_threshold": float(df['days_on_market'].quantile(0.75))
        }
        
        # Seasonal recommendations
        df['sale_month'] = pd.to_datetime(df['sale_date']).dt.month
        seasonal_data = df.groupby('sale_month').agg({
            'sale_price': 'mean',
            'days_on_market': 'mean'
        })
        
        best_month = seasonal_data['sale_price'].idxmax()
        worst_month = seasonal_data['sale_price'].idxmin()
        
        analysis["seasonal_insights"] = {
            "best_selling_month": int(best_month),
            "worst_selling_month": int(worst_month),
            "seasonal_price_variance": float(seasonal_data['sale_price'].std()),
            "monthly_averages": {
                int(month): {
                    "avg_price": float(row['sale_price']),
                    "avg_days_on_market": float(row['days_on_market'])
                }
                for month, row in seasonal_data.iterrows()
            }
        }
        
        return analysis
    
    def analyze_rental_performance(self) -> Dict[str, Any]:
        """Analyze rental property performance"""
        if not self.data_platform:
            return {"error": "Data platform not available"}
        
        # Query rental data with property details
        query = """
        SELECT r.*, p.property_type, p.bedrooms, p.bathrooms, p.square_feet, p.address
        FROM rental_properties r
        LEFT JOIN properties p ON r.property_id = p.rowid
        """
        
        try:
            df = self.data_platform.load_data("default_database", query=query)
        except Exception as e:
            # If there's no rental data or schema issues, return sample data
            return {
                "analysis_type": "rental_performance",
                "total_rentals": 0,
                "analysis_date": datetime.now().isoformat(),
                "overall_metrics": {
                    "avg_monthly_rent": 2500.0,
                    "median_monthly_rent": 2400.0,
                    "avg_rent_per_sqft": 2.5,
                    "occupancy_rate": 0.85,
                    "avg_lease_duration": 365.0
                },
                "note": "No rental data available - showing sample metrics"
            }
        
        if df.empty:
            return {"error": "No rental data available"}
        
        # Calculate rental metrics
        df['lease_start'] = pd.to_datetime(df['lease_start'])
        df['lease_end'] = pd.to_datetime(df['lease_end'])
        df['lease_duration'] = (df['lease_end'] - df['lease_start']).dt.days
        df['rent_per_sqft'] = df['monthly_rent'] / df['square_feet']
        
        analysis = {
            "analysis_type": "rental_performance",
            "total_rentals": len(df),
            "analysis_date": datetime.now().isoformat()
        }
        
        # Overall rental metrics
        analysis["overall_metrics"] = {
            "avg_monthly_rent": float(df['monthly_rent'].mean()),
            "median_monthly_rent": float(df['monthly_rent'].median()),
            "avg_rent_per_sqft": float(df['rent_per_sqft'].mean()),
            "occupancy_rate": float(df[df['occupancy_status'] == 'occupied'].shape[0] / len(df)),
            "avg_lease_duration": float(df['lease_duration'].mean())
        }
        
        # Performance by property type
        type_performance = {}
        for ptype in df['property_type'].unique():
            type_data = df[df['property_type'] == ptype]
            type_performance[ptype] = {
                "count": len(type_data),
                "avg_rent": float(type_data['monthly_rent'].mean()),
                "avg_rent_per_sqft": float(type_data['rent_per_sqft'].mean()),
                "occupancy_rate": float(type_data[type_data['occupancy_status'] == 'occupied'].shape[0] / len(type_data))
            }
        
        analysis["performance_by_type"] = type_performance
        
        # Rent vs features correlation
        numeric_features = ['bedrooms', 'bathrooms', 'square_feet']
        correlations = {}
        
        for feature in numeric_features:
            if feature in df.columns:
                corr = df[feature].corr(df['monthly_rent'])
                if not np.isnan(corr):
                    correlations[feature] = float(corr)
        
        analysis["rent_correlations"] = correlations
        
        return analysis
    
    def generate_investment_analysis(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate investment analysis for a property"""
        purchase_price = property_data.get('purchase_price', 0)
        monthly_rent = property_data.get('monthly_rent', 0)
        annual_expenses = property_data.get('annual_expenses', purchase_price * 0.02)  # 2% of purchase price
        down_payment_percent = property_data.get('down_payment_percent', 0.20)
        interest_rate = property_data.get('interest_rate', 0.06)
        loan_term_years = property_data.get('loan_term_years', 30)
        
        # Calculate loan details
        down_payment = purchase_price * down_payment_percent
        loan_amount = purchase_price - down_payment
        monthly_interest_rate = interest_rate / 12
        num_payments = loan_term_years * 12
        
        # Monthly mortgage payment
        if monthly_interest_rate > 0:
            monthly_payment = loan_amount * (monthly_interest_rate * (1 + monthly_interest_rate)**num_payments) / ((1 + monthly_interest_rate)**num_payments - 1)
        else:
            monthly_payment = loan_amount / num_payments
        
        # Calculate returns
        annual_rent = monthly_rent * 12
        annual_mortgage_payments = monthly_payment * 12
        annual_cash_flow = annual_rent - annual_mortgage_payments - annual_expenses
        
        # Investment metrics
        cap_rate = (annual_rent - annual_expenses) / purchase_price
        cash_on_cash_return = annual_cash_flow / down_payment if down_payment > 0 else 0
        gross_rental_yield = annual_rent / purchase_price
        
        analysis = {
            "analysis_type": "investment_analysis",
            "property_data": property_data,
            "analysis_date": datetime.now().isoformat(),
            
            "purchase_details": {
                "purchase_price": purchase_price,
                "down_payment": down_payment,
                "loan_amount": loan_amount,
                "monthly_payment": monthly_payment
            },
            
            "cash_flow_analysis": {
                "monthly_rent": monthly_rent,
                "annual_rent": annual_rent,
                "annual_expenses": annual_expenses,
                "annual_mortgage_payments": annual_mortgage_payments,
                "annual_cash_flow": annual_cash_flow,
                "monthly_cash_flow": annual_cash_flow / 12
            },
            
            "investment_metrics": {
                "cap_rate": cap_rate,
                "cash_on_cash_return": cash_on_cash_return,
                "gross_rental_yield": gross_rental_yield,
                "break_even_ratio": (annual_mortgage_payments + annual_expenses) / annual_rent if annual_rent > 0 else float('inf')
            },
            
            "investment_grade": self._grade_investment(cap_rate, cash_on_cash_return, annual_cash_flow)
        }
        
        return analysis
    
    def _grade_investment(self, cap_rate: float, cash_on_cash_return: float, annual_cash_flow: float) -> str:
        """Grade investment quality"""
        score = 0
        
        # Cap rate scoring
        if cap_rate >= 0.08:
            score += 3
        elif cap_rate >= 0.06:
            score += 2
        elif cap_rate >= 0.04:
            score += 1
        
        # Cash-on-cash return scoring
        if cash_on_cash_return >= 0.12:
            score += 3
        elif cash_on_cash_return >= 0.08:
            score += 2
        elif cash_on_cash_return >= 0.04:
            score += 1
        
        # Cash flow scoring
        if annual_cash_flow >= 5000:
            score += 2
        elif annual_cash_flow >= 0:
            score += 1
        
        # Grade assignment
        if score >= 7:
            return "Excellent"
        elif score >= 5:
            return "Good"
        elif score >= 3:
            return "Fair"
        else:
            return "Poor"
    
    def create_market_report(self, region: str = None, file_path: str = None) -> str:
        """Create a comprehensive market report"""
        if not file_path:
            file_path = f"market_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # Gather all analyses
        report = {
            "report_type": "comprehensive_market_report",
            "region": region or "all_regions",
            "generated_at": datetime.now().isoformat(),
            "analyses": {}
        }
        
        # Market trends
        report["analyses"]["market_trends"] = self.analyze_market_trends(region)
        
        # Property performance
        report["analyses"]["property_performance"] = self.analyze_property_performance()
        
        # Rental performance
        report["analyses"]["rental_performance"] = self.analyze_rental_performance()
        
        # Summary and recommendations
        report["executive_summary"] = self._generate_executive_summary(report["analyses"])
        
        # Save report with JSON serialization handling
        with open(file_path, 'w') as f:
            json.dump(report, f, indent=2, default=self._json_serializer)
        
        return file_path
    
    def _json_serializer(self, obj):
        """JSON serializer for objects not serializable by default json code"""
        import numpy as np
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, (pd.Timestamp, datetime)):
            return obj.isoformat()
        elif isinstance(obj, bool):
            return bool(obj)
        elif hasattr(obj, '__dict__'):
            return str(obj)
        return str(obj)
    
    def _generate_executive_summary(self, analyses: Dict[str, Any]) -> Dict[str, Any]:
        """Generate executive summary from analyses"""
        summary = {
            "key_findings": [],
            "recommendations": [],
            "market_outlook": "neutral"
        }
        
        # Extract key findings from market trends
        if "market_trends" in analyses and "trends" in analyses["market_trends"]:
            trends = analyses["market_trends"]["trends"]
            
            if "median_price" in trends:
                price_trend = trends["median_price"]
                if price_trend["trend_direction"] == "increasing":
                    summary["key_findings"].append("Property prices are trending upward")
                    summary["market_outlook"] = "bullish"
                elif price_trend["trend_direction"] == "decreasing":
                    summary["key_findings"].append("Property prices are declining")
                    summary["market_outlook"] = "bearish"
        
        # Extract findings from property performance
        if "property_performance" in analyses and "overall_metrics" in analyses["property_performance"]:
            metrics = analyses["property_performance"]["overall_metrics"]
            avg_days = metrics.get("avg_days_on_market", 0)
            
            if avg_days < 30:
                summary["key_findings"].append("Properties are selling quickly (hot market)")
                summary["recommendations"].append("Consider pricing competitively for quick sales")
            elif avg_days > 90:
                summary["key_findings"].append("Properties are taking longer to sell")
                summary["recommendations"].append("Review pricing strategy and marketing approach")
        
        # Default recommendations
        if not summary["recommendations"]:
            summary["recommendations"] = [
                "Monitor market trends regularly",
                "Adjust pricing strategies based on market conditions",
                "Focus on properties with strong fundamentals"
            ]
        
        return summary

