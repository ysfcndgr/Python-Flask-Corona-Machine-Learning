import http.client
import json
import logging
import pandas as pd
import numpy as np
import html
import re
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures, LabelEncoder
from datetime import datetime, date, timedelta
from typing import List, Dict, Any, Optional, Tuple
from flask import current_app
import os
import requests
from functools import lru_cache

logger = logging.getLogger(__name__)

class APIError(Exception):
    """Custom API exception"""
    pass

class CoronaAPIService:
    """Service for handling Corona API calls"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "api.collectapi.com"
        self.headers = {
            'content-type': "application/json",
            'authorization': f"apikey {api_key}"
        }
    
    def _make_request(self, endpoint: str, params: str = "") -> Dict[str, Any]:
        """Make HTTP request to API"""
        try:
            conn = http.client.HTTPSConnection(self.base_url)
            url = f"{endpoint}{params}"
            conn.request("GET", url, headers=self.headers)
            
            response = conn.getresponse()
            data = response.read()
            conn.close()
            
            if response.status != 200:
                raise APIError(f"API request failed with status {response.status}")
            
            return json.loads(data)
        except Exception as e:
            logger.error(f"API request error: {e}")
            raise APIError(f"Failed to fetch data from API: {e}")
    
    @lru_cache(maxsize=32)
    def get_total_data(self) -> Dict[str, Any]:
        """Get total Corona data with caching"""
        try:
            return self._make_request("/corona/totalData")
        except APIError as e:
            logger.error(f"Error getting total Corona data: {e}")
            return {"result": {}}
    
    @lru_cache(maxsize=32)
    def get_countries_data(self) -> List[Dict[str, Any]]:
        """Get countries Corona data with caching"""
        try:
            result = self._make_request("/corona/countriesData")
            return result.get('result', [])
        except APIError as e:
            logger.error(f"Error getting countries Corona data: {e}")
            return []
    
    @lru_cache(maxsize=32)
    def get_country_by_name(self, country: str) -> Dict[str, Any]:
        """Get specific country Corona data"""
        try:
            result = self._make_request("/corona/countriesData", f"?country={country}")
            return result.get('result', {})
        except APIError as e:
            logger.error(f"Error getting country data for {country}: {e}")
            return {}
    
    @lru_cache(maxsize=32)
    def get_corona_news(self) -> List[Dict[str, Any]]:
        """Get Corona news with caching"""
        try:
            result = self._make_request("/corona/coronaNews")
            return result.get('result', [])
        except APIError as e:
            logger.error(f"Error getting Corona news: {e}")
            return []

class DateService:
    """Service for date-related operations"""
    
    @staticmethod
    def get_upcoming_dates(days: int = 7) -> List[date]:
        """Get list of upcoming dates"""
        today = date.today()
        return [today + timedelta(days=i+1) for i in range(days)]
    
    @staticmethod
    def format_date(date_obj: date, format_str: str = "%Y-%m-%d") -> str:
        """Format date object to string"""
        return date_obj.strftime(format_str)

class PredictionService:
    """Service for machine learning predictions"""
    
    def __init__(self, dataset_path: str = 'static/dataset/turkey.xlsx'):
        self.dataset_path = dataset_path
        self.current_date = 190  # Base date for predictions
    
    def _load_data(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Load and preprocess data"""
        try:
            if not os.path.exists(self.dataset_path):
                logger.warning(f"Dataset not found at {self.dataset_path}")
                return None, None, None
            
            df = pd.read_excel(self.dataset_path)
            
            # Validate required columns
            required_columns = ['Cases', 'Deaths']
            for col in required_columns:
                if col not in df.columns:
                    logger.error(f"Required column '{col}' not found in dataset")
                    return None, None, None
            
            cases = df.Cases.values.reshape(-1, 1)
            deaths = df.Deaths.values.reshape(-1, 1)
            
            # Handle date column (assuming it's the 4th column, index 3)
            if df.shape[1] > 3:
                date_column = df.iloc[:, 3:4].values
                le = LabelEncoder()
                date_column[:, 0] = le.fit_transform(date_column[:, 0])
            else:
                # Create synthetic date column if not available
                date_column = np.arange(len(df)).reshape(-1, 1)
            
            return cases, deaths, date_column
            
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            return None, None, None
    
    def _train_model(self, X: np.ndarray, y: np.ndarray, degree: int = 5) -> Tuple[PolynomialFeatures, LinearRegression]:
        """Train polynomial regression model"""
        poly_features = PolynomialFeatures(degree=degree)
        X_poly = poly_features.fit_transform(X)
        
        model = LinearRegression()
        model.fit(X_poly, y)
        
        return poly_features, model
    
    def generate_predictions(self, days: int = 7) -> Tuple[List[int], List[int]]:
        """Generate Corona case and death predictions"""
        try:
            cases, deaths, dates = self._load_data()
            
            if cases is None or deaths is None or dates is None:
                logger.warning("Using mock data for predictions due to data loading issues")
                return self._generate_mock_predictions(days)
            
            # Train models
            cases_poly, cases_model = self._train_model(dates, cases)
            deaths_poly, deaths_model = self._train_model(dates, deaths)
            
            # Generate predictions
            case_predictions = []
            death_predictions = []
            
            for i in range(self.current_date, self.current_date + days):
                # Predict cases
                case_pred = cases_model.predict(cases_poly.fit_transform([[i]]))
                case_predictions.append(max(0, int(case_pred[0][0])))  # Ensure non-negative
                
                # Predict deaths
                death_pred = deaths_model.predict(deaths_poly.fit_transform([[i]]))
                death_predictions.append(max(0, int(death_pred[0][0])))  # Ensure non-negative
            
            return case_predictions, death_predictions
            
        except Exception as e:
            logger.error(f"Error generating predictions: {e}")
            return self._generate_mock_predictions(days)
    
    def _generate_mock_predictions(self, days: int) -> Tuple[List[int], List[int]]:
        """Generate mock predictions when real data is not available"""
        logger.info("Generating mock predictions")
        
        # Generate realistic-looking mock data
        base_cases = 1000
        base_deaths = 50
        
        case_predictions = []
        death_predictions = []
        
        for i in range(days):
            # Add some randomness but keep it realistic
            case_trend = base_cases + (i * 50) + np.random.randint(-100, 100)
            death_trend = base_deaths + (i * 2) + np.random.randint(-10, 10)
            
            case_predictions.append(max(0, case_trend))
            death_predictions.append(max(0, death_trend))
        
        return case_predictions, death_predictions

class AuthService:
    """Service for authentication-related operations"""
    
    @staticmethod
    def is_admin(user_status: int) -> bool:
        """Check if user is admin"""
        return user_status == 1
    
    @staticmethod
    def is_banned(user_status: int) -> bool:
        """Check if user is banned"""
        return user_status == 2
    
    @staticmethod
    def is_active(user_status: int) -> bool:
        """Check if user is active"""
        return user_status == 0

class ValidationService:
    """Service for input validation and sanitization"""
    
    @staticmethod
    def sanitize_html(content: str) -> str:
        """Basic HTML sanitization (you might want to use a library like bleach)"""
        # Basic sanitization - in production, use a proper HTML sanitizer
        return html.escape(content)
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate URL format"""
        pattern = r'^https?://(?:[-\w.])+(?:\:[0-9]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:\#(?:[\w.])*)?)?$'
        return re.match(pattern, url) is not None

class CacheService:
    """Simple in-memory cache service"""
    
    def __init__(self):
        self._cache = {}
        self._timestamps = {}
        self.default_ttl = 300  # 5 minutes
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if key in self._cache:
            timestamp = self._timestamps.get(key, 0)
            if datetime.now().timestamp() - timestamp < self.default_ttl:
                return self._cache[key]
            else:
                # Remove expired item
                del self._cache[key]
                del self._timestamps[key]
        return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache"""
        self._cache[key] = value
        self._timestamps[key] = datetime.now().timestamp()
    
    def clear(self) -> None:
        """Clear all cache"""
        self._cache.clear()
        self._timestamps.clear()

# Global cache instance
cache = CacheService()