# GCAP3226 Week 7: Web Crawler & API Code Templates
# Practical examples for government data collection

import requests
import json
import pandas as pd
import time
import random
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns

# =============================================================================
# 1. HONG KONG GOVERNMENT API TEMPLATES
# =============================================================================

class HKOWeatherAPI:
    """Hong Kong Observatory Weather API Interface"""
    
    def __init__(self):
        self.base_url = "https://data.weather.gov.hk/weatherAPI/opendata/weather.php"
    
    def get_current_weather(self):
        """Get current weather data"""
        params = {
            'dataType': 'rhrread',  # Real-time weather data
            'lang': 'en'
        }
        return self._make_request(params)
    
    def get_typhoon_info(self):
        """Get typhoon information"""
        params = {
            'dataType': 'tcm',  # Tropical cyclone information
            'lang': 'en'
        }
        return self._make_request(params)
    
    def get_air_quality(self):
        """Get air quality data"""
        params = {
            'dataType': 'aqhi',  # Air quality health index
            'lang': 'en'
        }
        return self._make_request(params)
    
    def _make_request(self, params):
        """Make API request with error handling"""
        try:
            response = requests.get(self.base_url, params=params, timeout=30)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"API Error: {response.status_code}")
                return None
        except Exception as e:
            print(f"Request failed: {e}")
            return None

# =============================================================================
# 2. TRANSPORT DEPARTMENT API TEMPLATES
# =============================================================================

class TransportAPI:
    """Transport Department API Interface"""
    
    def __init__(self):
        self.kmb_base = "https://data.etabus.gov.hk/v1/transport/kmb"
        self.ctb_base = "https://data.etabus.gov.hk/v1/transport/ctb"
    
    def get_bus_routes(self, company='kmb'):
        """Get all bus routes"""
        url = f"{self.kmb_base}/route" if company == 'kmb' else f"{self.ctb_base}/route"
        return self._make_request(url)
    
    def get_bus_stops(self, company='kmb'):
        """Get all bus stops"""
        url = f"{self.kmb_base}/stop" if company == 'kmb' else f"{self.ctb_base}/stop"
        return self._make_request(url)
    
    def get_bus_arrival(self, stop_id, route, company='kmb'):
        """Get real-time bus arrival information"""
        url = f"{self.kmb_base}/eta/{stop_id}/{route}" if company == 'kmb' else f"{self.ctb_base}/eta/{stop_id}/{route}"
        return self._make_request(url)
    
    def _make_request(self, url):
        """Make API request with error handling"""
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"API Error: {response.status_code}")
                return None
        except Exception as e:
            print(f"Request failed: {e}")
            return None

# =============================================================================
# 3. WEB SCRAPING TEMPLATES
# =============================================================================

class GovernmentWebScraper:
    """Web scraper for government websites"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def scrape_news_announcements(self, url, max_pages=5):
        """Scrape government news and announcements"""
        all_news = []
        
        for page in range(1, max_pages + 1):
            try:
                page_url = f"{url}?page={page}"
                response = requests.get(page_url, headers=self.headers, timeout=30)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract news items (adjust selectors based on actual website)
                news_items = soup.find_all('div', class_='news-item')
                
                for item in news_items:
                    title = item.find('h3').text.strip() if item.find('h3') else 'No title'
                    date = item.find('span', class_='date').text.strip() if item.find('span', class_='date') else 'No date'
                    link = item.find('a')['href'] if item.find('a') else 'No link'
                    
                    all_news.append({
                        'title': title,
                        'date': date,
                        'link': link,
                        'scraped_at': datetime.now().isoformat()
                    })
                
                # Be respectful - add delay between requests
                time.sleep(random.uniform(1, 3))
                
            except Exception as e:
                print(f"Error scraping page {page}: {e}")
                continue
        
        return pd.DataFrame(all_news)
    
    def scrape_data_table(self, url, table_selector):
        """Scrape data from HTML tables"""
        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            table = soup.select_one(table_selector)
            if table:
                # Convert table to DataFrame
                df = pd.read_html(str(table))[0]
                return df
            else:
                print("Table not found")
                return None
                
        except Exception as e:
            print(f"Error scraping table: {e}")
            return None

# =============================================================================
# 4. DATA PROCESSING AND CLEANING TEMPLATES
# =============================================================================

class DataProcessor:
    """Data processing and cleaning utilities"""
    
    @staticmethod
    def clean_government_data(df):
        """Clean government data with common issues"""
        # Remove duplicates
        df = df.drop_duplicates()
        
        # Handle missing values
        df = df.fillna(method='ffill').fillna(method='bfill')
        
        # Standardize date formats
        date_columns = df.select_dtypes(include=['object']).columns
        for col in date_columns:
            if 'date' in col.lower() or 'time' in col.lower():
                try:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
                except:
                    pass
        
        # Remove extreme outliers (99th percentile)
        numeric_columns = df.select_dtypes(include=['number']).columns
        for col in numeric_columns:
            q99 = df[col].quantile(0.99)
            df = df[df[col] <= q99]
        
        return df
    
    @staticmethod
    def merge_api_data(api_data_list, merge_key):
        """Merge multiple API datasets"""
        if not api_data_list:
            return pd.DataFrame()
        
        merged_df = api_data_list[0]
        for data in api_data_list[1:]:
            merged_df = pd.merge(merged_df, data, on=merge_key, how='outer')
        
        return merged_df
    
    @staticmethod
    def create_time_series(df, date_col, value_col, freq='D'):
        """Create time series data"""
        df[date_col] = pd.to_datetime(df[date_col])
        df = df.set_index(date_col)
        ts = df[value_col].resample(freq).mean()
        return ts

# =============================================================================
# 5. VISUALIZATION TEMPLATES
# =============================================================================

class DataVisualizer:
    """Data visualization utilities"""
    
    @staticmethod
    def plot_time_series(data, title, xlabel, ylabel):
        """Plot time series data"""
        plt.figure(figsize=(12, 6))
        plt.plot(data.index, data.values)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    
    @staticmethod
    def plot_correlation_matrix(df, title):
        """Plot correlation matrix"""
        plt.figure(figsize=(10, 8))
        correlation_matrix = df.corr()
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
        plt.title(title)
        plt.tight_layout()
        plt.show()
    
    @staticmethod
    def plot_distribution(data, title, bins=30):
        """Plot data distribution"""
        plt.figure(figsize=(10, 6))
        plt.hist(data, bins=bins, alpha=0.7, edgecolor='black')
        plt.title(title)
        plt.xlabel('Value')
        plt.ylabel('Frequency')
        plt.tight_layout()
        plt.show()

# =============================================================================
# 6. TEAM-SPECIFIC DATA COLLECTION FUNCTIONS
# =============================================================================

class TeamDataCollectors:
    """Team-specific data collection functions"""
    
    @staticmethod
    def team1_flu_shot_data():
        """Team 1: Flu shot campaign data collection"""
        # This would be implemented based on available data sources
        print("Team 1: Implement flu shot data collection")
        # Example: Scrape Department of Health vaccination data
        pass
    
    @staticmethod
    def team2_bus_route_data():
        """Team 2: Bus route coordination data collection"""
        transport_api = TransportAPI()
        
        # Get bus routes
        routes = transport_api.get_bus_routes()
        
        # Get bus stops
        stops = transport_api.get_bus_stops()
        
        # Get weather data for correlation
        weather_api = HKOWeatherAPI()
        weather = weather_api.get_current_weather()
        
        return {
            'routes': routes,
            'stops': stops,
            'weather': weather
        }
    
    @staticmethod
    def team3_typhoon_data():
        """Team 3: Typhoon preparedness data collection"""
        weather_api = HKOWeatherAPI()
        
        # Get typhoon information
        typhoon_info = weather_api.get_typhoon_info()
        
        # Get current weather
        current_weather = weather_api.get_current_weather()
        
        return {
            'typhoon': typhoon_info,
            'weather': current_weather
        }
    
    @staticmethod
    def team4_waste_data():
        """Team 4: Municipal solid waste charging data collection"""
        # This would be implemented based on available data sources
        print("Team 4: Implement waste charging data collection")
        # Example: Scrape EPD waste data
        pass
    
    @staticmethod
    def team5_green_community_data():
        """Team 5: Green @ Community data collection"""
        # This would be implemented based on available data sources
        print("Team 5: Implement green community data collection")
        # Example: Scrape community program data
        pass
    
    @staticmethod
    def team6_bus_stop_data():
        """Team 6: Bus stop optimization data collection"""
        transport_api = TransportAPI()
        
        # Get bus stops
        stops = transport_api.get_bus_stops()
        
        # Get bus routes
        routes = transport_api.get_bus_routes()
        
        return {
            'stops': stops,
            'routes': routes
        }

# =============================================================================
# 7. EXAMPLE USAGE AND TESTING
# =============================================================================

def test_apis():
    """Test API functionality"""
    print("Testing Hong Kong Government APIs...")
    
    # Test weather API
    weather_api = HKOWeatherAPI()
    weather_data = weather_api.get_current_weather()
    if weather_data:
        print("✓ Weather API working")
        print(f"Sample data: {list(weather_data.keys())}")
    else:
        print("✗ Weather API failed")
    
    # Test transport API
    transport_api = TransportAPI()
    routes = transport_api.get_bus_routes()
    if routes:
        print("✓ Transport API working")
        print(f"Sample data: {list(routes.keys())}")
    else:
        print("✗ Transport API failed")

def example_data_collection():
    """Example of complete data collection workflow"""
    print("Example: Bus Route Data Collection")
    
    # Collect data
    team_data = TeamDataCollectors.team2_bus_route_data()
    
    # Process data
    if team_data['routes']:
        routes_df = pd.DataFrame(team_data['routes']['data'])
        routes_df = DataProcessor.clean_government_data(routes_df)
        
        # Visualize data
        if 'route' in routes_df.columns:
            route_counts = routes_df['route'].value_counts().head(10)
            DataVisualizer.plot_distribution(route_counts, "Top 10 Bus Routes")
        
        print(f"Collected {len(routes_df)} bus routes")
    
    return team_data

# =============================================================================
# 8. MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("GCAP3226 Week 7: Web Crawler & API Code Templates")
    print("=" * 50)
    
    # Test APIs
    test_apis()
    
    print("\n" + "=" * 50)
    
    # Example data collection
    example_data_collection()
    
    print("\nTemplates ready for use!")
    print("Customize the functions for your specific team project.")


