"""Data platform setup and management for real estate analytics"""

import pandas as pd
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
import json
import os


@dataclass
class DataSource:
    """Represents a data source in the platform"""
    name: str
    source_type: str  # 'database', 'api', 'file', 'manual'
    connection_string: Optional[str] = None
    file_path: Optional[str] = None
    api_endpoint: Optional[str] = None
    update_frequency: str = "daily"  # daily, weekly, monthly, manual
    last_updated: Optional[datetime] = None
    schema: Dict[str, str] = field(default_factory=dict)
    is_active: bool = True


class DataPlatform:
    """Manages data platform setup and operations for real estate analytics"""
    
    def __init__(self, platform_name: str, base_path: str = "./data"):
        self.platform_name = platform_name
        self.base_path = base_path
        self.data_sources: Dict[str, DataSource] = {}
        self.databases: Dict[str, str] = {}
        self.data_catalog: Dict[str, Any] = {}
        
        # Create base directory structure
        self._setup_directory_structure()
        
        # Initialize default database
        self.default_db_path = os.path.join(base_path, "real_estate_analytics.db")
        self._initialize_default_database()
    
    def _setup_directory_structure(self):
        """Create the directory structure for the data platform"""
        directories = [
            self.base_path,
            os.path.join(self.base_path, "raw"),
            os.path.join(self.base_path, "processed"),
            os.path.join(self.base_path, "exports"),
            os.path.join(self.base_path, "backups")
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def _initialize_default_database(self):
        """Initialize the default SQLite database with real estate tables"""
        conn = sqlite3.connect(self.default_db_path)
        cursor = conn.cursor()
        
        # Properties table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS properties (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                address TEXT NOT NULL,
                property_type TEXT,
                bedrooms INTEGER,
                bathrooms INTEGER,
                square_feet REAL,
                lot_size REAL,
                year_built INTEGER,
                listing_price REAL,
                sale_price REAL,
                listing_date DATE,
                sale_date DATE,
                days_on_market INTEGER,
                agent_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Rental properties table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rental_properties (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                property_id INTEGER,
                monthly_rent REAL,
                lease_start DATE,
                lease_end DATE,
                tenant_id TEXT,
                occupancy_status TEXT,
                last_maintenance DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (property_id) REFERENCES properties (id)
            )
        ''')
        
        # Market data table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS market_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE,
                region TEXT,
                median_price REAL,
                average_days_on_market INTEGER,
                inventory_count INTEGER,
                price_per_sqft REAL,
                rental_yield REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # KPI tracking table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS kpi_tracking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE,
                kpi_name TEXT,
                kpi_value REAL,
                target_value REAL,
                category TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # Register the default database as a data source
        self.add_data_source(
            name="default_database",
            source_type="database",
            connection_string=f"sqlite:///{self.default_db_path}",
            schema={
                "properties": "Real estate property listings and sales data",
                "rental_properties": "Rental property management data",
                "market_data": "Market trends and regional data",
                "kpi_tracking": "Key performance indicators tracking"
            }
        )
    
    def add_data_source(self, name: str, source_type: str, **kwargs) -> DataSource:
        """Add a new data source to the platform"""
        data_source = DataSource(
            name=name,
            source_type=source_type,
            **kwargs
        )
        
        self.data_sources[name] = data_source
        self._update_data_catalog()
        return data_source
    
    def remove_data_source(self, name: str) -> bool:
        """Remove a data source from the platform"""
        if name in self.data_sources:
            self.data_sources[name].is_active = False
            self._update_data_catalog()
            return True
        return False
    
    def connect_to_source(self, source_name: str) -> Optional[Any]:
        """Connect to a specific data source"""
        if source_name not in self.data_sources:
            return None
        
        source = self.data_sources[source_name]
        
        if source.source_type == "database" and source.connection_string:
            if source.connection_string.startswith("sqlite:///"):
                db_path = source.connection_string.replace("sqlite:///", "")
                return sqlite3.connect(db_path)
        
        return None
    
    def load_data(self, source_name: str, query: str = None, table_name: str = None, params: tuple = None) -> Optional[pd.DataFrame]:
        """Load data from a specified source"""
        if source_name not in self.data_sources:
            return None
        
        source = self.data_sources[source_name]
        
        if source.source_type == "database":
            conn = self.connect_to_source(source_name)
            if conn:
                if query:
                    df = pd.read_sql_query(query, conn, params=params)
                elif table_name:
                    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
                else:
                    return None
                
                conn.close()
                source.last_updated = datetime.now()
                return df
        
        elif source.source_type == "file" and source.file_path:
            if source.file_path.endswith('.csv'):
                return pd.read_csv(source.file_path)
            elif source.file_path.endswith('.xlsx'):
                return pd.read_excel(source.file_path)
        
        return None
    
    def save_data(self, df: pd.DataFrame, table_name: str, source_name: str = "default_database", if_exists: str = "append") -> bool:
        """Save data to a specified source"""
        if source_name not in self.data_sources:
            return False
        
        source = self.data_sources[source_name]
        
        if source.source_type == "database":
            conn = self.connect_to_source(source_name)
            if conn:
                df.to_sql(table_name, conn, if_exists=if_exists, index=False)
                conn.close()
                source.last_updated = datetime.now()
                return True
        
        return False
    
    def create_sample_data(self) -> Dict[str, pd.DataFrame]:
        """Create sample real estate data for testing"""
        import random
        from datetime import datetime, timedelta
        
        # Sample properties data
        properties_data = []
        property_types = ["Single Family", "Condo", "Townhouse", "Multi-Family"]
        
        for i in range(100):
            listing_date = datetime.now() - timedelta(days=random.randint(1, 365))
            days_on_market = random.randint(1, 180)
            sale_date = listing_date + timedelta(days=days_on_market) if random.random() > 0.3 else None
            
            property_data = {
                'address': f"{random.randint(100, 9999)} {random.choice(['Main', 'Oak', 'Pine', 'Elm'])} St",
                'property_type': random.choice(property_types),
                'bedrooms': random.randint(1, 5),
                'bathrooms': random.randint(1, 4),
                'square_feet': random.randint(800, 4000),
                'lot_size': random.uniform(0.1, 2.0),
                'year_built': random.randint(1950, 2023),
                'listing_price': random.randint(200000, 800000),
                'sale_price': random.randint(180000, 750000) if sale_date else None,
                'listing_date': listing_date.date(),
                'sale_date': sale_date.date() if sale_date else None,
                'days_on_market': days_on_market if sale_date else None,
                'agent_id': f"AGENT_{random.randint(1, 20):03d}"
            }
            properties_data.append(property_data)
        
        properties_df = pd.DataFrame(properties_data)
        
        # Sample market data
        market_data = []
        regions = ["Downtown", "Suburbs", "Waterfront", "Historic District"]
        
        for i in range(52):  # Weekly data for a year
            date = datetime.now() - timedelta(weeks=i)
            for region in regions:
                market_data.append({
                    'date': date.date(),
                    'region': region,
                    'median_price': random.randint(300000, 600000),
                    'average_days_on_market': random.randint(20, 90),
                    'inventory_count': random.randint(50, 200),
                    'price_per_sqft': random.randint(150, 400),
                    'rental_yield': random.uniform(3.0, 8.0)
                })
        
        market_df = pd.DataFrame(market_data)
        
        # Save sample data to database
        self.save_data(properties_df, "properties", if_exists="replace")
        self.save_data(market_df, "market_data", if_exists="replace")
        
        return {
            "properties": properties_df,
            "market_data": market_df
        }
    
    def _update_data_catalog(self):
        """Update the data catalog with current sources"""
        self.data_catalog = {
            "platform_name": self.platform_name,
            "created_at": datetime.now().isoformat(),
            "active_sources": len([s for s in self.data_sources.values() if s.is_active]),
            "sources": {
                name: {
                    "type": source.source_type,
                    "last_updated": source.last_updated.isoformat() if source.last_updated else None,
                    "schema": source.schema,
                    "is_active": source.is_active
                }
                for name, source in self.data_sources.items()
            }
        }
    
    def get_platform_status(self) -> Dict[str, Any]:
        """Get comprehensive platform status"""
        return {
            "platform_name": self.platform_name,
            "base_path": self.base_path,
            "total_sources": len(self.data_sources),
            "active_sources": len([s for s in self.data_sources.values() if s.is_active]),
            "data_catalog": self.data_catalog,
            "database_path": self.default_db_path
        }
    
    def export_data_catalog(self, file_path: str = None) -> str:
        """Export data catalog to JSON file"""
        if not file_path:
            file_path = os.path.join(self.base_path, "data_catalog.json")
        
        with open(file_path, 'w') as f:
            json.dump(self.data_catalog, f, indent=2)
        
        return file_path

