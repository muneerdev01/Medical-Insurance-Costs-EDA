# 📊 Medical Insurance Costs Analysis Dashboard

A comprehensive interactive Streamlit dashboard for exploratory data analysis of medical insurance costs data.

## Overview

This dashboard provides in-depth analysis of insurance cost patterns across different demographic segments and risk factors.

### Features

- **🎯 Interactive Filters**: Filter by smoker status, region, age range, and BMI
- **📈 Comprehensive Visualizations**: Distributions, relationships, and correlations
- **📊 Segment Analysis**: Compare costs across different customer groups
- **🔗 Correlation Analysis**: Heatmaps and correlation coefficients
- **📋 Statistical Summaries**: Detailed descriptive and comparison statistics
- **💡 Key Insights**: Business-focused recommendations and findings

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup Steps

1. **Navigate to the project directory**:
```bash
cd "d:\EDA\Medical Insurance Costs"
```

2. **Install required packages**:
```bash
pip install -r requirements.txt
```

Or manually install:
```bash
pip install streamlit pandas numpy plotly matplotlib seaborn scipy
```

## Running the Dashboard

### Command

```bash
streamlit run dashboard.py
```

### What You'll See

Once the dashboard launches in your browser:

1. **KPI Section**: Key performance indicators showing dataset overview
2. **Distribution Charts**: Histogram and pie charts of variables
3. **Relationship Analysis**: Scatter plots and box plots showing relationships with charges
4. **Segment Analysis**: Comparative analysis across demographic segments
5. **Correlation Matrix**: Visual correlation analysis
6. **Statistical Summaries**: Detailed statistics and group comparisons
7. **Data Explorer**: Browse the raw data
8. **Insights & Recommendations**: Business intelligence summary

## Using the Filters

Located in the left sidebar, you can:

- **Select Smoker Status**: Filter by smokers, non-smokers, or both
- **Choose Regions**: Include/exclude any US regions
- **Adjust Age Range**: Filter by minimum and maximum age
- **Set BMI Range**: Filter by minimum and maximum BMI

All visualizations update automatically based on your filters.

## Key Findings

### Critical Insights

1. **Smoking Impact** (Most Significant)
   - Smokers pay ~$32,050 average
   - Non-smokers pay ~$8,434 average
   - **379% cost increase for smokers**

2. **Age Effect** (Moderate)
   - Correlation with charges: r = 0.30
   - Charges increase significantly after age 40
   - Young adults (18-25) have lowest costs

3. **BMI Factor** (Moderate)
   - Correlation with charges: r = 0.20
   - Overweight/Obese individuals face higher costs
   - Weight management programs recommended

4. **Gender** (Minimal)
   - No significant gender-based pricing disparity
   - Male avg: $13,957 vs Female avg: $12,570

## Dashboard Sections

### 1. KPI Metrics
- Total records count
- Average charges
- Median charges
- Smoker percentage
- Average age

### 2. Distributions
- Insurance charges distribution
- Age distribution
- BMI distribution
- Categorical variables (sex, smoker, region)

### 3. Relationships
- Age vs charges (with trend line)
- BMI vs charges (with trend line)
- Children count vs charges
- Smoker status impact

### 4. Segment Analysis
- Charges by sex
- Charges by region
- Charges by age group
- Charges by BMI category

### 5. Correlation Analysis
- Full correlation matrix heatmap
- Correlation coefficients with charges

### 6. Statistical Summary
- Descriptive statistics
- Group comparisons (smoker vs non-smoker)
- Data quality metrics

### 7. Data Explorer
- View first 10 records
- Sample 20 random records
- Browse all records

## Data Source

**Dataset**: Medical Insurance Costs (insurance.csv)
- **Records**: 1,338 individuals
- **Features**: 7 variables
  - age: Customer age (18-64 years)
  - sex: Gender (male/female)
  - bmi: Body Mass Index (15.96-53.13)
  - children: Number of dependents (0-5)
  - smoker: Smoking status (yes/no)
  - region: US geographic region (4 regions)
  - charges: Annual medical costs ($)

## Recommendations

### For Insurance Companies

1. **Pricing Strategy**
   - Risk-tier smokers with 300-400% premium
   - Age-adjusted pricing (increase post-40)
   - BMI-based wellness incentives

2. **Risk Management**
   - Target smoking cessation programs (highest ROI)
   - Health screenings for 40+ customers
   - Weight management initiatives

3. **Customer Segmentation**
   - Low Risk: Young, healthy, non-smoker
   - Medium Risk: Middle-aged, non-smoker
   - High Risk: Smokers (all ages)

## Performance & Scale

- Handles 1,338+ records efficiently
- Real-time filtering and updates
- Multiple concurrent users supported
- Responsive design for all screen sizes

## Troubleshooting

### Issue: Module not found
**Solution**: Ensure all requirements are installed:
```bash
pip install -r requirements.txt
```

### Issue: Data file not found
**Solution**: Ensure `insurance.csv` is in the same directory as `dashboard.py`

### Issue: Dashboard won't load
**Solution**: Check Streamlit version and update if needed:
```bash
pip install --upgrade streamlit
```

## Files Included

- `dashboard.py` - Main Streamlit application
- `insurance.csv` - Raw dataset
- `insurance_processed.csv` - Dataset with derived features
- `requirements.txt` - Python package dependencies
- `README.md` - This documentation file

## Technical Stack

- **Framework**: Streamlit 1.31.1
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly (interactive), Matplotlib, Seaborn
- **Statistical Analysis**: SciPy

## Version History

- **v1.0** (March 2026) - Initial release with full EDA features

## License

Data analysis project for educational and business intelligence purposes.

## Contact & Support

For questions or issues with the dashboard, review the error messages or check:
- Streamlit documentation: https://docs.streamlit.io
- Plotly documentation: https://plotly.com/python/

---

**Last Updated**: March 2026  
**Data Records**: 1,338  
**Dashboard Status**: ✅ Production Ready
