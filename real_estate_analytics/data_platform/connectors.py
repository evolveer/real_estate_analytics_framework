"""Database and API connectors for the real estate analytics platform"""

import sqlite3
import pandas as pd
import requests
from typing import Dict, List, Optional, Any
from abc import ABC, abstractmethod
import json


class BaseConnector(ABC):
    """Abstract base class for data connectors"""
    
    def __init__(self, name: str):
        self.name = name
        self.is_connected = False
    
    @abstractmethod
    def connect(self) -> bool:
        """Establish connection to the data source"""
        pass
    
    @abstractmethod
    def disconnect(self) -> bool:
        """Close connection to the data source"""
        pass
    
    @abstractmethod
    def test_connection(self) -> bool:
        """Test if connection is working"""
        pass


class DatabaseConnector(BaseConnector):
    """Database connector for various database types"""
    
    def __init__(self, name: str, db_type: str, connection_string: str):
        super().__init__(name)
        self.db_type = db_type.lower()
        self.connection_string = connection_string
        self.connection = None
    
    def connect(self) -> bool:
        """Establish database connection"""
        try:
            if self.db_type == "sqlite":
                self.connection = sqlite3.connect(self.connection_string)
                self.is_connected = True
                return True
            # Add support for other database types as needed
            # elif self.db_type == "postgresql":
            #     import psycopg2
            #     self.connection = psycopg2.connect(self.connection_string)
            # elif self.db_type == "mysql":
            #     import mysql.connector
            #     self.connection = mysql.connector.connect(**connection_params)
            
        except Exception as e:
            print(f"Database connection failed: {e}")
            self.is_connected = False
            return False
    
    def disconnect(self) -> bool:
        """Close database connection"""
        try:
            if self.connection:
                self.connection.close()
                self.is_connected = False
                return True
        except Exception as e:
            print(f"Error closing database connection: {e}")
        return False
    
    def test_connection(self) -> bool:
        """Test database connection"""
        if not self.is_connected:
            return self.connect()
        
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            return True
        except Exception:
            return False
    
    def execute_query(self, query: str, params: tuple = None) -> pd.DataFrame:
        """Execute SQL query and return results as DataFrame"""
        if not self.is_connected:
            self.connect()
        
        try:
            if params:
                return pd.read_sql_query(query, self.connection, params=params)
            else:
                return pd.read_sql_query(query, self.connection)
        except Exception as e:
            print(f"Query execution failed: {e}")
            return pd.DataFrame()
    
    def insert_data(self, table_name: str, data: pd.DataFrame, if_exists: str = "append") -> bool:
        """Insert data into database table"""
        if not self.is_connected:
            self.connect()
        
        try:
            data.to_sql(table_name, self.connection, if_exists=if_exists, index=False)
            return True
        except Exception as e:
            print(f"Data insertion failed: {e}")
            return False
    
    def get_table_schema(self, table_name: str) -> Dict[str, str]:
        """Get table schema information"""
        if not self.is_connected:
            self.connect()
        
        try:
            if self.db_type == "sqlite":
                cursor = self.connection.cursor()
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                return {col[1]: col[2] for col in columns}
        except Exception as e:
            print(f"Schema retrieval failed: {e}")
        
        return {}
    
    def list_tables(self) -> List[str]:
        """List all tables in the database"""
        if not self.is_connected:
            self.connect()
        
        try:
            if self.db_type == "sqlite":
                cursor = self.connection.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                return [table[0] for table in cursor.fetchall()]
        except Exception as e:
            print(f"Table listing failed: {e}")
        
        return []


class APIConnector(BaseConnector):
    """API connector for external data sources"""
    
    def __init__(self, name: str, base_url: str, api_key: str = None, headers: Dict[str, str] = None):
        super().__init__(name)
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.headers = headers or {}
        
        if api_key:
            self.headers['Authorization'] = f'Bearer {api_key}'
    
    def connect(self) -> bool:
        """Test API connection"""
        return self.test_connection()
    
    def disconnect(self) -> bool:
        """No persistent connection for APIs"""
        return True
    
    def test_connection(self) -> bool:
        """Test API connectivity"""
        try:
            response = requests.get(f"{self.base_url}/health", headers=self.headers, timeout=10)
            self.is_connected = response.status_code == 200
            return self.is_connected
        except Exception:
            # Try a simple GET request to base URL if health endpoint doesn't exist
            try:
                response = requests.get(self.base_url, headers=self.headers, timeout=10)
                self.is_connected = response.status_code < 500
                return self.is_connected
            except Exception:
                self.is_connected = False
                return False
    
    def get_data(self, endpoint: str, params: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """Get data from API endpoint"""
        try:
            url = f"{self.base_url}/{endpoint.lstrip('/')}"
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"API GET request failed: {e}")
            return None
    
    def post_data(self, endpoint: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Post data to API endpoint"""
        try:
            url = f"{self.base_url}/{endpoint.lstrip('/')}"
            response = requests.post(url, headers=self.headers, json=data, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"API POST request failed: {e}")
            return None
    
    def get_real_estate_data(self, location: str, property_type: str = None) -> pd.DataFrame:
        """Get real estate data from API (example implementation)"""
        params = {'location': location}
        if property_type:
            params['property_type'] = property_type
        
        data = self.get_data('properties', params)
        if data and 'properties' in data:
            return pd.DataFrame(data['properties'])
        
        return pd.DataFrame()


class FileConnector(BaseConnector):
    """File connector for CSV, Excel, and other file formats"""
    
    def __init__(self, name: str, file_path: str, file_type: str = None):
        super().__init__(name)
        self.file_path = file_path
        self.file_type = file_type or self._detect_file_type()
    
    def _detect_file_type(self) -> str:
        """Detect file type from extension"""
        if self.file_path.endswith('.csv'):
            return 'csv'
        elif self.file_path.endswith(('.xlsx', '.xls')):
            return 'excel'
        elif self.file_path.endswith('.json'):
            return 'json'
        else:
            return 'unknown'
    
    def connect(self) -> bool:
        """Check if file exists and is readable"""
        try:
            import os
            self.is_connected = os.path.exists(self.file_path) and os.access(self.file_path, os.R_OK)
            return self.is_connected
        except Exception:
            self.is_connected = False
            return False
    
    def disconnect(self) -> bool:
        """No persistent connection for files"""
        return True
    
    def test_connection(self) -> bool:
        """Test file accessibility"""
        return self.connect()
    
    def read_data(self, **kwargs) -> pd.DataFrame:
        """Read data from file"""
        if not self.connect():
            return pd.DataFrame()
        
        try:
            if self.file_type == 'csv':
                return pd.read_csv(self.file_path, **kwargs)
            elif self.file_type == 'excel':
                return pd.read_excel(self.file_path, **kwargs)
            elif self.file_type == 'json':
                return pd.read_json(self.file_path, **kwargs)
        except Exception as e:
            print(f"File reading failed: {e}")
        
        return pd.DataFrame()
    
    def write_data(self, data: pd.DataFrame, **kwargs) -> bool:
        """Write data to file"""
        try:
            if self.file_type == 'csv':
                data.to_csv(self.file_path, index=False, **kwargs)
            elif self.file_type == 'excel':
                data.to_excel(self.file_path, index=False, **kwargs)
            elif self.file_type == 'json':
                data.to_json(self.file_path, **kwargs)
            return True
        except Exception as e:
            print(f"File writing failed: {e}")
            return False

