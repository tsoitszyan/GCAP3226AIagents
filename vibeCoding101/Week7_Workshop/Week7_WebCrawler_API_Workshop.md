# GCAP3226 Week 7: Web Crawler & API Workshop
## Field Studies – Project Data Collection

**Date:** October 14, 2025 (Week 7)  
**Duration:** 3 hours  
**Focus:** Data Collection Techniques for Government Policy Analysis

---

## 🎯 Workshop Objectives

By the end of this workshop, students will be able to:
1. **Understand APIs and Web Scraping** for government data collection
2. **Implement basic web crawlers** using Python libraries
3. **Access government APIs** for real-time data
4. **Apply data collection techniques** to their specific team projects
5. **Set up automated data collection** for ongoing project monitoring

---

## 📋 Workshop Agenda

### Part 1: Introduction to Data Collection (45 minutes)
- **Government Data Sources Overview** (15 min)
- **APIs vs Web Scraping** (15 min)
- **Legal and Ethical Considerations** (15 min)

### Part 2: Hands-on API Workshop (60 minutes)
- **Hong Kong Government APIs** (20 min)
- **Weather Data APIs** (20 min)
- **Transport Data APIs** (20 min)

### Part 3: Web Scraping Fundamentals (60 minutes)
- **BeautifulSoup Introduction** (20 min)
- **Requests Library** (20 min)
- **Practical Scraping Exercise** (20 min)

### Part 4: Team-Specific Application (45 minutes)
- **Team Breakout Sessions** (30 min)
- **Data Collection Planning** (15 min)

---

## 🔧 Technical Setup

### Required Software
```bash
# Install required Python packages
pip install requests beautifulsoup4 pandas matplotlib seaborn
pip install hko-weather-api  # Hong Kong Observatory API
```

### Development Environment
- **Jupyter Notebook** or **Google Colab**
- **Python 3.8+**
- **Internet connection** for API access

---

## 📊 Government Data Sources

### Hong Kong Government APIs

#### 1. Hong Kong Observatory (HKO) API
```python
import requests
import json

# HKO Weather API
def get_weather_data():
    url = "https://data.weather.gov.hk/weatherAPI/opendata/weather.php"
    params = {
        'dataType': 'rhrread',  # Real-time weather data
        'lang': 'en'
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

# Example usage
weather_data = get_weather_data()
print(json.dumps(weather_data, indent=2))
```

#### 2. Transport Department API
```python
# Bus Route Information
def get_bus_routes():
    url = "https://data.etabus.gov.hk/v1/transport/kmb/route"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

# Real-time Bus Arrival
def get_bus_arrival(route, stop_id):
    url = f"https://data.etabus.gov.hk/v1/transport/kmb/eta/{stop_id}/{route}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None
```

#### 3. Environmental Protection Department
```python
# Air Quality Data
def get_air_quality():
    url = "https://data.weather.gov.hk/weatherAPI/opendata/airquality.php"
    params = {
        'dataType': 'aqhi',
        'lang': 'en'
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None
```

### Web Scraping Examples

#### 1. Basic Web Scraping with BeautifulSoup
```python
import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_government_news():
    url = "https://www.info.gov.hk/gia/general/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract news items
    news_items = []
    for item in soup.find_all('div', class_='news-item'):
        title = item.find('h3').text.strip()
        date = item.find('span', class_='date').text.strip()
        link = item.find('a')['href']
        
        news_items.append({
            'title': title,
            'date': date,
            'link': link
        })
    
    return pd.DataFrame(news_items)

# Example usage
news_df = scrape_government_news()
print(news_df.head())
```

#### 2. Scraping Data Tables
```python
def scrape_data_table(url, table_id):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    table = soup.find('table', id=table_id)
    if table:
        # Convert table to DataFrame
        df = pd.read_html(str(table))[0]
        return df
    else:
        print("Table not found")
        return None

# Example: Scraping census data
census_url = "https://www.censtatd.gov.hk/en/web_table.html?id=1"
census_data = scrape_data_table(census_url, "census-table")
```

---

## 🎯 Team-Specific Data Collection

### Team 1: Flu Shot Campaign Analysis
**Data Sources:**
- Department of Health vaccination records
- Hospital Authority data
- Census demographic data

**API/Scraping Targets:**
```python
# Hospital Authority API
def get_ha_vaccination_data():
    # Implementation for HA data access
    pass

# Census data scraping
def scrape_demographic_data():
    # Implementation for demographic data
    pass
```

### Team 2: Bus Route Coordination
**Data Sources:**
- KMB/CTB/NWFB APIs
- Octopus card data (if available)
- Weather data for impact analysis

**API/Scraping Targets:**
```python
# Already provided above - bus route and arrival APIs
# Additional: Weather impact correlation
def correlate_weather_transport():
    weather = get_weather_data()
    bus_data = get_bus_routes()
    # Analysis implementation
    pass
```

### Team 3: Typhoon Preparedness
**Data Sources:**
- HKO typhoon data
- Emergency services data
- Historical damage reports

**API/Scraping Targets:**
```python
# HKO Typhoon API
def get_typhoon_data():
    url = "https://data.weather.gov.hk/weatherAPI/opendata/weather.php"
    params = {
        'dataType': 'tcm',
        'lang': 'en'
    }
    response = requests.get(url, params=params)
    return response.json() if response.status_code == 200 else None
```

### Team 4: Municipal Solid Waste Charging
**Data Sources:**
- EPD waste data
- Policy implementation records
- Household data

**API/Scraping Targets:**
```python
# EPD data scraping
def scrape_waste_data():
    # Implementation for waste data collection
    pass
```

### Team 5: Green @ Community
**Data Sources:**
- EPD community program data
- Environmental monitoring data
- Community participation records

**API/Scraping Targets:**
```python
# Environmental data API
def get_environmental_data():
    # Implementation for environmental data
    pass
```

### Team 6: Bus Stop Optimization
**Data Sources:**
- Transport Department bus stop data
- Ridership statistics
- Urban planning data

**API/Scraping Targets:**
```python
# Bus stop data API
def get_bus_stop_data():
    url = "https://data.etabus.gov.hk/v1/transport/kmb/stop"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None
```

---

## 📝 Hands-on Exercises

### Exercise 1: API Data Collection (30 minutes)
1. **Choose your team's relevant API**
2. **Write a function to collect data**
3. **Store data in a structured format (CSV/JSON)**
4. **Create a simple visualization**

### Exercise 2: Web Scraping (30 minutes)
1. **Identify a government website with relevant data**
2. **Write a scraper to extract the data**
3. **Handle errors and edge cases**
4. **Save data for analysis**

### Exercise 3: Data Integration (30 minutes)
1. **Combine API and scraped data**
2. **Clean and preprocess the data**
3. **Create a preliminary analysis**
4. **Document your findings**

---

## 🔒 Legal and Ethical Considerations

### Important Guidelines:
1. **Respect robots.txt** - Check website's scraping policies
2. **Rate limiting** - Don't overwhelm servers
3. **Terms of service** - Follow API usage terms
4. **Data privacy** - Protect personal information
5. **Attribution** - Credit data sources

### Best Practices:
```python
import time
import random

def respectful_scraping(url, delay_range=(1, 3)):
    """Add delays between requests to be respectful"""
    time.sleep(random.uniform(*delay_range))
    response = requests.get(url)
    return response
```

---

## 📊 Data Storage and Management

### Recommended Structure:
```
project_data/
├── raw_data/
│   ├── api_data/
│   ├── scraped_data/
│   └── manual_data/
├── processed_data/
├── analysis/
└── visualizations/
```

### Data Documentation Template:
```python
# Data collection metadata
data_metadata = {
    'source': 'Hong Kong Observatory API',
    'collection_date': '2025-10-14',
    'collection_method': 'API',
    'update_frequency': 'Real-time',
    'data_quality': 'Official government data',
    'limitations': 'Historical data limited to 7 days'
}
```

---

## 🎯 Next Steps for Teams

### Immediate Actions (This Week):
1. **Set up data collection infrastructure**
2. **Begin collecting relevant data**
3. **Document data sources and methods**
4. **Start preliminary analysis**

### Preparation for Week 8:
1. **Complete initial data collection**
2. **Clean and organize data**
3. **Identify data gaps**
4. **Plan mathematical model approach**

---

## 📚 Additional Resources

### Documentation:
- [Hong Kong Observatory API Documentation](https://data.weather.gov.hk/weatherAPI/doc/HKO_Open_Data_API_Documentation.pdf)
- [Transport Department Open Data](https://data.gov.hk/en/datasets)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

### Tutorials:
- [Python Web Scraping Tutorial](https://realpython.com/beautiful-soup-web-scraper-python/)
- [API Integration Best Practices](https://realpython.com/api-integration-in-python/)

### Tools:
- [Postman](https://www.postman.com/) - API testing
- [Scrapy](https://scrapy.org/) - Advanced web scraping
- [Pandas](https://pandas.pydata.org/) - Data manipulation

---

## 📞 Support and Contact

### Technical Support:
- **Dr. Wu**: Mathematical modeling and data analysis
- **Dr. Wang**: Project coordination and communication
- **AI Assistant**: Code debugging and implementation help

### Office Hours:
- **Dr. Wu**: Tuesdays 2-4 PM
- **Dr. Wang**: Wednesdays 10-12 PM

---

*This workshop provides the foundation for effective data collection in your government policy analysis projects. Remember to be respectful of data sources and always document your methods for reproducibility.*

