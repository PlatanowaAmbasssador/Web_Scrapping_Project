# Car Data Web Scraping and Analysis Project

## Overview
This project involves web scraping car data and performing exploratory data analysis (EDA) along with price prediction using machine learning techniques.

## Project Structure
```
.
├── Data Collection/
│   ├── 01_scrap_uzywane_static.ipynb    # Initial static scraping notebook
│   ├── 02_zbieranie_linkow.ipynb        # Link collection notebook
│   └── automation_script.py             # Automated scraping script
├── Analysis/
│   └── 03_Data_Analysis.ipynb           # EDA and ML analysis
├── Outputs/
│   ├── df_page_links.pkl               # Collected page links
│   └── df_car_scrapped_data.pkl        # Scraped car data
├── README.md                           # Project documentation
├── requirements.txt                    # Python dependencies
└── .gitignore                         # Git ignore patterns
```

## Features
- Web scraping of car data
- Automated data collection
- Data storage in pickle format
- Exploratory Data Analysis using Plotly
- Price prediction using Linear Regression
- Interactive visualizations

## Analysis Components
1. **Data Collection**
   - Static web scraping (01_scrap_uzywane_static.ipynb)
   - Link collection (02_zbieranie_linkow.ipynb)
   - Automated scraping (automation_script.py)
   - Storage of raw data in pickle format

2. **Exploratory Data Analysis**
   - Price distribution analysis
   - Brand-wise price comparison
   - Year vs Price relationship
   - Correlation analysis

3. **Machine Learning**
   - Linear Regression model for price prediction
   - Feature importance analysis
   - Model performance evaluation

## Requirements
All required dependencies are listed in `requirements.txt`. Main requirements include:
- Python 3.10+
- pandas
- numpy
- plotly
- scikit-learn
- beautifulsoup4
- requests
- selenium
- jupyter
- matplotlib
- seaborn

To install all dependencies, run:
```bash
pip install -r requirements.txt
```

## Usage
1. Clone the repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the notebooks in sequence:
   - First run 01_scrap_uzywane_static.ipynb for initial data collection
   - Then run 02_zbieranie_linkow.ipynb to gather all car links
   - Use automation_script.py for automated data collection
   - Finally, run 03_Data_Analysis.ipynb for analysis and modeling
4. View the analysis results and visualizations

## Results
The project includes:
- Thinking process of scrapping the data
- Scrapping the data
- Interactive visualizations of car price distributions
- Correlation analysis of different features
- Price prediction model with performance metrics
- Feature importance analysis