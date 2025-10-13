# GCAP3226 Week 7: Quick Reference Guide
## Web Crawler & API Workshop

---

## 🚀 Quick Start Checklist

### Before the Workshop:
- [ ] Install Python packages: `pip install requests beautifulsoup4 pandas matplotlib seaborn`
- [ ] Set up Jupyter Notebook or Google Colab
- [ ] Review your team's project requirements
- [ ] Prepare questions about data collection challenges

### During the Workshop:
- [ ] Follow along with code examples
- [ ] Test APIs with your team's data needs
- [ ] Document any errors or issues
- [ ] Ask questions during Q&A sessions

### After the Workshop:
- [ ] Implement data collection for your project
- [ ] Clean and organize collected data
- [ ] Prepare for small group meeting
- [ ] Document your data collection methods

---

## 📊 Essential APIs for Hong Kong Government Data

### 1. Hong Kong Observatory (HKO)
```python
# Weather data
url = "https://data.weather.gov.hk/weatherAPI/opendata/weather.php"
params = {'dataType': 'rhrread', 'lang': 'en'}

# Typhoon information
params = {'dataType': 'tcm', 'lang': 'en'}

# Air quality
params = {'dataType': 'aqhi', 'lang': 'en'}
```

### 2. Transport Department
```python
# KMB bus routes
url = "https://data.etabus.gov.hk/v1/transport/kmb/route"

# Bus stops
url = "https://data.etabus.gov.hk/v1/transport/kmb/stop"

# Real-time arrival
url = "https://data.etabus.gov.hk/v1/transport/kmb/eta/{stop_id}/{route}"
```

### 3. Data.gov.hk
```python
# Open data portal
url = "https://data.gov.hk/en/datasets"
# Search for specific datasets by department
```

---

## 🔧 Common Code Patterns

### API Request with Error Handling
```python
import requests
import time

def safe_api_call(url, params=None, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=30)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"API Error: {response.status_code}")
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(2 ** attempt)  # Exponential backoff
    return None
```

### Web Scraping with BeautifulSoup
```python
from bs4 import BeautifulSoup
import requests

def scrape_website(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract data based on HTML structure
    data = []
    for item in soup.find_all('div', class_='data-item'):
        title = item.find('h3').text.strip()
        date = item.find('span', class_='date').text.strip()
        data.append({'title': title, 'date': date})
    
    return data
```

### Data Cleaning Template
```python
import pandas as pd

def clean_data(df):
    # Remove duplicates
    df = df.drop_duplicates()
    
    # Handle missing values
    df = df.fillna(method='ffill').fillna(method='bfill')
    
    # Convert dates
    date_cols = df.select_dtypes(include=['object']).columns
    for col in date_cols:
        if 'date' in col.lower():
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # Remove outliers
    numeric_cols = df.select_dtypes(include=['number']).columns
    for col in numeric_cols:
        q99 = df[col].quantile(0.99)
        df = df[df[col] <= q99]
    
    return df
```

---

## 🎯 Team-Specific Data Sources

### Team 1: Flu Shot Campaign
- **Department of Health**: Vaccination records
- **Hospital Authority**: Healthcare data
- **Census**: Demographic data
- **APIs**: Health department data portals

### Team 2: Bus Route Coordination
- **KMB/CTB/NWFB**: Real-time bus data
- **Transport Department**: Route information
- **Weather API**: Impact correlation
- **APIs**: Transport data APIs (provided above)

### Team 3: Typhoon Preparedness
- **Hong Kong Observatory**: Meteorological data
- **Emergency Services**: Response data
- **Historical Records**: Damage assessments
- **APIs**: HKO weather APIs (provided above)

### Team 4: Municipal Solid Waste
- **Environmental Protection Department**: Waste data
- **Policy Documents**: Implementation records
- **Household Surveys**: Behavioral data
- **APIs**: EPD data portals

### Team 5: Green @ Community
- **Environmental Protection Department**: Program data
- **Community Records**: Participation data
- **Environmental Monitoring**: Sensor data
- **APIs**: Environmental data APIs

### Team 6: Bus Stop Optimization
- **Transport Department**: Bus stop data
- **Ridership Statistics**: Passenger data
- **Urban Planning**: Geographic data
- **APIs**: Transport APIs (provided above)

---

## ⚠️ Important Guidelines

### Legal and Ethical Considerations:
1. **Respect robots.txt** - Check website scraping policies
2. **Rate limiting** - Don't overwhelm servers (add delays)
3. **Terms of service** - Follow API usage terms
4. **Data privacy** - Protect personal information
5. **Attribution** - Credit data sources

### Best Practices:
```python
import time
import random

# Add delays between requests
time.sleep(random.uniform(1, 3))

# Use proper headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# Handle errors gracefully
try:
    response = requests.get(url, timeout=30)
    # Process response
except Exception as e:
    print(f"Error: {e}")
    # Handle error appropriately
```

---

## 📝 Data Documentation Template

```python
# Document your data collection
data_metadata = {
    'source': 'Hong Kong Observatory API',
    'collection_date': '2025-10-14',
    'collection_method': 'API',
    'update_frequency': 'Real-time',
    'data_quality': 'Official government data',
    'limitations': 'Historical data limited to 7 days',
    'contact': 'Dr. Wu (Mathematics), Dr. Wang (English)',
    'team': 'Team 3 - Typhoon Preparedness'
}
```

---

## 🆘 Troubleshooting Common Issues

### API Issues:
- **403 Forbidden**: Check API key or rate limits
- **404 Not Found**: Verify URL and parameters
- **Timeout**: Increase timeout or add retry logic
- **JSON Decode Error**: Check response format

### Scraping Issues:
- **Empty Results**: Check HTML selectors
- **Blocked Requests**: Use proper headers and delays
- **Dynamic Content**: Consider Selenium for JavaScript
- **Rate Limited**: Add longer delays between requests

### Data Issues:
- **Missing Values**: Use fillna() or interpolation
- **Inconsistent Formats**: Standardize date/time formats
- **Outliers**: Remove or transform extreme values
- **Encoding Issues**: Use UTF-8 encoding

---

## 📞 Support Resources

### Immediate Help:
- **Dr. Wu**: Mathematical modeling and data analysis
- **Dr. Wang**: Project coordination and communication
- **AI Assistant**: Code debugging and implementation
- **Peer Support**: Team collaboration

### Online Resources:
- [Hong Kong Observatory API Docs](https://data.weather.gov.hk/weatherAPI/doc/)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Requests Documentation](https://docs.python-requests.org/)

### Tools:
- **Postman**: API testing
- **Jupyter Notebook**: Interactive development
- **Google Colab**: Cloud-based Python environment
- **GitHub**: Code version control

---

## 🎯 Next Steps

### This Week:
1. **Implement data collection** for your team project
2. **Clean and organize** collected data
3. **Document data sources** and methods
4. **Prepare for group meeting** with progress report

### Week 8:
1. **Finalize mathematical model** choice
2. **Begin model implementation** with Dr. Wu
3. **Create preliminary analysis** of collected data
4. **Identify additional data** needs

---

*Keep this reference guide handy during the workshop and throughout your project. Don't hesitate to ask questions and seek help when needed!*


