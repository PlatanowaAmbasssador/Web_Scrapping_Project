# Car Data Web Scraping and Analysis Project

## Overview
This project involves web scraping car data from a Polish car marketplace and performing comprehensive exploratory data analysis (EDA) along with price prediction using machine learning techniques. The project is structured to collect, process, and analyze car data in a systematic manner.

## Project Structure
```
.
├── 01_scrap_uzywane_static.ipynb    # Initial static scraping notebook
├── 02_zbieranie_linkow.ipynb        # Link collection notebook
├── 03_Executor.ipynb                # Main execution notebook
├── 04_Data_Analysis.ipynb           # EDA and ML analysis
├── automation_script.py             # Automated scraping script
├── Outputs/                         # Data storage directory
│   ├── df_page_links.pkl           # Collected page links
│   └── df_car_scrapped_data.pkl    # Scraped car data
├── README.md                        # Project documentation
└── requirements.txt                 # Python dependencies
```

## Features
- Automated web scraping of car data from Polish marketplace
- Robust data collection with error handling and retry mechanisms
- Data storage in pickle format for efficient processing
- Comprehensive Exploratory Data Analysis using Plotly
- Price prediction using machine learning models
- Interactive visualizations and insights

## Project Components

### 1. Data Collection
- **Initial Scraping** (`01_scrap_uzywane_static.ipynb`)
  - Basic static scraping implementation
  - Initial data structure validation
  - Basic error handling

- **Link Collection** (`02_zbieranie_linkow.ipynb`)
  - Systematic collection of car listing links
  - Pagination handling
  - Link validation and deduplication

- **Automated Scraping** (`automation_script.py`)
  - Robust scraping implementation
  - Error handling and retry mechanisms
  - Rate limiting and polite scraping practices
  - Data validation and cleaning

### 2. Data Processing and Analysis
- **Main Execution** (`03_Executor.ipynb`)
  - Orchestrates the scraping process
  - Manages data flow between components
  - Handles execution logging and monitoring

- **Data Analysis** (`04_Data_Analysis.ipynb`)
  - Comprehensive EDA
  - Price distribution analysis
  - Brand and model analysis
  - Feature correlation studies
  - Machine learning model development
  - Model performance evaluation

## Technical Requirements
- Python 3.10+
- Key dependencies (specified versions in requirements.txt):
  - pandas (2.0.3)
  - numpy (1.24.3)
  - plotly (5.18.0)
  - scikit-learn (1.3.0)
  - beautifulsoup4 (4.12.2)
  - selenium (4.15.2)
  - requests (2.31.0)
  - jupyter (1.0.0)
  - matplotlib (3.7.2)
  - seaborn (0.12.2)
  - lxml (4.9.3)
  - webdriver-manager (4.0.1)

## Installation
1. Clone the repository
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Start with `01_scrap_uzywane_static.ipynb` to understand the basic scraping structure
2. Run `02_zbieranie_linkow.ipynb` to collect all car listing links
3. Use `03_Executor.ipynb` to run the automated scraping process
4. Analyze the data using `04_Data_Analysis.ipynb`

## Output
The project generates:
- Comprehensive car dataset in pickle format
- Interactive visualizations of price distributions
- Brand and model analysis
- Feature correlation analysis
- Price prediction models with performance metrics
- Detailed insights and findings

## Notes
- The scraping process includes rate limiting to be respectful to the target website
- All data is stored in the `Outputs` directory
- The analysis notebook includes detailed visualizations and insights
- The project follows best practices for web scraping and data analysis