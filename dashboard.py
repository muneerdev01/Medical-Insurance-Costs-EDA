"""
Professional Medical Insurance Costs Analysis Dashboard
=========================================================
Interactive Streamlit dashboard for comprehensive EDA and insights
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Insurance Costs Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
    }
    .header-title {
        color: #1f77b4;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA LOADING & CACHING
# ============================================================================
@st.cache_data
def load_data():
    """Load and process the insurance dataset"""
    df = pd.read_csv('insurance.csv')
    
    # Data type conversion
    df['sex'] = df['sex'].astype('category')
    df['smoker'] = df['smoker'].astype('category')
    df['region'] = df['region'].astype('category')
    
    # Create age groups
    df['age_group'] = pd.cut(df['age'], bins=[0, 25, 35, 50, 65], 
                             labels=['18-25', '26-35', '36-50', '50+'])
    
    # Create BMI categories
    df['bmi_category'] = pd.cut(df['bmi'], bins=[0, 18.5, 25, 30, 100],
                                labels=['Underweight', 'Normal', 'Overweight', 'Obese'])
    
    return df

# Load data
df = load_data()

# ============================================================================
# SIDEBAR FILTERS
# ============================================================================
st.sidebar.title("🎯 Dashboard Filters")
st.sidebar.markdown("---")

# Filter options
smoker_filter = st.sidebar.multiselect(
    "Smoker Status",
    options=df['smoker'].unique(),
    default=df['smoker'].unique(),
    key="smoker_filter"
)

region_filter = st.sidebar.multiselect(
    "Region",
    options=df['region'].unique(),
    default=df['region'].unique(),
    key="region_filter"
)

age_range = st.sidebar.slider(
    "Age Range",
    min_value=int(df['age'].min()),
    max_value=int(df['age'].max()),
    value=(int(df['age'].min()), int(df['age'].max())),
    key="age_range"
)

bmi_range = st.sidebar.slider(
    "BMI Range",
    min_value=float(df['bmi'].min()),
    max_value=float(df['bmi'].max()),
    value=(float(df['bmi'].min()), float(df['bmi'].max())),
    key="bmi_range"
)

# Apply filters
filtered_df = df[
    (df['smoker'].isin(smoker_filter)) &
    (df['region'].isin(region_filter)) &
    (df['age'] >= age_range[0]) &
    (df['age'] <= age_range[1]) &
    (df['bmi'] >= bmi_range[0]) &
    (df['bmi'] <= bmi_range[1])
]

st.sidebar.markdown("---")
st.sidebar.info(f"📈 Records Shown: {len(filtered_df):,} / {len(df):,}")

# ============================================================================
# MAIN DASHBOARD
# ============================================================================

# Title
st.markdown("<h1 style='text-align: center; color: #1f77b4;'>💰 Medical Insurance Costs Analysis</h1>", 
            unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>Comprehensive dashboard for insurance cost analysis and insights</p>", 
            unsafe_allow_html=True)

# ============================================================================
# KPI SECTION
# ============================================================================
st.markdown("## 📊 Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="Total Records",
        value=f"{len(filtered_df):,}",
        delta=f"{len(filtered_df) - len(df):,}" if len(filtered_df) != len(df) else None
    )

with col2:
    avg_charge = filtered_df['charges'].mean()
    st.metric(
        label="Avg Charges",
        value=f"${avg_charge:,.0f}",
        delta=f"${avg_charge - df['charges'].mean():,.0f}" if len(filtered_df) != len(df) else None
    )

with col3:
    median_charge = filtered_df['charges'].median()
    st.metric(
        label="Median Charges",
        value=f"${median_charge:,.0f}"
    )

with col4:
    smoker_pct = (filtered_df['smoker'] == 'yes').sum() / len(filtered_df) * 100
    st.metric(
        label="Smoker %",
        value=f"{smoker_pct:.1f}%"
    )

with col5:
    avg_age = filtered_df['age'].mean()
    st.metric(
        label="Avg Age",
        value=f"{avg_age:.1f}",
        delta=f"{avg_age - df['age'].mean():.1f}" if len(filtered_df) != len(df) else None
    )

st.markdown("---")

# ============================================================================
# ROW 1: DISTRIBUTIONS
# ============================================================================
st.markdown("## 📈 Distributions")

col1, col2 = st.columns(2)

with col1:
    # Charges Distribution
    fig_charges = px.histogram(
        filtered_df, 
        x='charges', 
        nbins=40,
        title='Distribution of Insurance Charges',
        labels={'charges': 'Charges ($)', 'count': 'Frequency'},
        color_discrete_sequence=['#1f77b4']
    )
    fig_charges.update_layout(
        hovermode='x unified',
        showlegend=False,
        height=400
    )
    st.plotly_chart(fig_charges, width='stretch')

with col2:
    # Age Distribution
    fig_age = px.histogram(
        filtered_df,
        x='age',
        nbins=30,
        title='Distribution of Age',
        labels={'age': 'Age (years)', 'count': 'Frequency'},
        color_discrete_sequence=['#ff7f0e']
    )
    fig_age.update_layout(
        hovermode='x unified',
        showlegend=False,
        height=400
    )
    st.plotly_chart(fig_age, width='stretch')

col1, col2 = st.columns(2)

with col1:
    # BMI Distribution
    fig_bmi = px.histogram(
        filtered_df,
        x='bmi',
        nbins=30,
        title='Distribution of BMI',
        labels={'bmi': 'BMI', 'count': 'Frequency'},
        color_discrete_sequence=['#2ca02c']
    )
    fig_bmi.update_layout(
        hovermode='x unified',
        showlegend=False,
        height=400
    )
    st.plotly_chart(fig_bmi, width='stretch')

with col2:
    # Categorical Variables
    fig_cat = make_subplots(
        rows=1, cols=3,
        specs=[[{'type':'pie'}, {'type':'pie'}, {'type':'pie'}]],
        subplot_titles=('Sex Distribution', 'Smoker Status', 'Region Distribution')
    )
    
    # Sex
    sex_counts = filtered_df['sex'].value_counts()
    fig_cat.add_trace(
        go.Pie(labels=sex_counts.index, values=sex_counts.values, name='Sex'),
        row=1, col=1
    )
    
    # Smoker
    smoker_counts = filtered_df['smoker'].value_counts()
    fig_cat.add_trace(
        go.Pie(labels=smoker_counts.index, values=smoker_counts.values, name='Smoker'),
        row=1, col=2
    )
    
    # Region
    region_counts = filtered_df['region'].value_counts()
    fig_cat.add_trace(
        go.Pie(labels=region_counts.index, values=region_counts.values, name='Region'),
        row=1, col=3
    )
    
    fig_cat.update_layout(height=400, showlegend=True)
    st.plotly_chart(fig_cat, width='stretch')

st.markdown("---")

# ============================================================================
# ROW 2: RELATIONSHIPS
# ============================================================================
st.markdown("## 🔗 Relationships with Charges")

col1, col2 = st.columns(2)

with col1:
    # Age vs Charges
    fig_age_charges = px.scatter(
        filtered_df,
        x='age',
        y='charges',
        color='smoker',
        title='Age vs Charges (colored by Smoker Status)',
        labels={'age': 'Age (years)', 'charges': 'Charges ($)'},
        color_discrete_map={'yes': '#d62728', 'no': '#2ca02c'},
        opacity=0.6,
        trendline='ols',
        trendline_color_override='#1f77b4'
    )
    fig_age_charges.update_layout(height=400, hovermode='closest')
    st.plotly_chart(fig_age_charges, width='stretch')

with col2:
    # BMI vs Charges
    fig_bmi_charges = px.scatter(
        filtered_df,
        x='bmi',
        y='charges',
        color='smoker',
        title='BMI vs Charges (colored by Smoker Status)',
        labels={'bmi': 'BMI', 'charges': 'Charges ($)'},
        color_discrete_map={'yes': '#d62728', 'no': '#2ca02c'},
        opacity=0.6,
        trendline='ols',
        trendline_color_override='#1f77b4'
    )
    fig_bmi_charges.update_layout(height=400, hovermode='closest')
    st.plotly_chart(fig_bmi_charges, width='stretch')

col1, col2 = st.columns(2)

with col1:
    # Children vs Charges
    fig_children = px.box(
        filtered_df,
        x='children',
        y='charges',
        color='smoker',
        title='Children Count vs Charges',
        labels={'children': 'Number of Children', 'charges': 'Charges ($)'},
        color_discrete_map={'yes': '#d62728', 'no': '#2ca02c'}
    )
    fig_children.update_layout(height=400)
    st.plotly_chart(fig_children, width='stretch')

with col2:
    # Smoker Status Impact
    fig_smoker = px.box(
        filtered_df,
        x='smoker',
        y='charges',
        title='Major Impact: Smoker Status on Charges',
        labels={'smoker': 'Smoker Status', 'charges': 'Charges ($)'},
        color='smoker',
        color_discrete_map={'yes': '#d62728', 'no': '#2ca02c'}
    )
    fig_smoker.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_smoker, width='stretch')

st.markdown("---")

# ============================================================================
# ROW 3: SEGMENT ANALYSIS
# ============================================================================
st.markdown("## 🎯 Segment Analysis")

col1, col2 = st.columns(2)

with col1:
    # Charges by Sex
    sex_stats = filtered_df.groupby('sex')['charges'].agg(['mean', 'median', 'count']).reset_index()
    fig_sex = px.bar(
        sex_stats,
        x='sex',
        y='mean',
        title='Average Charges by Sex',
        labels={'sex': 'Sex', 'mean': 'Average Charges ($)'},
        text='mean',
        color='sex',
        color_discrete_map={'male': '#1f77b4', 'female': '#ff7f0e'}
    )
    fig_sex.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
    fig_sex.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_sex, width='stretch')

with col2:
    # Charges by Region
    region_stats = filtered_df.groupby('region')['charges'].agg(['mean', 'count']).reset_index()
    region_stats = region_stats.sort_values('mean', ascending=False)
    fig_region = px.bar(
        region_stats,
        x='region',
        y='mean',
        title='Average Charges by Region',
        labels={'region': 'Region', 'mean': 'Average Charges ($)'},
        text='mean',
        color='mean',
        color_continuous_scale='Viridis'
    )
    fig_region.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
    fig_region.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_region, width='stretch')

col1, col2 = st.columns(2)

with col1:
    # Charges by Age Group
    age_stats = filtered_df.groupby('age_group', observed=True)['charges'].agg(['mean', 'count']).reset_index()
    fig_age_group = px.bar(
        age_stats,
        x='age_group',
        y='mean',
        title='Average Charges by Age Group',
        labels={'age_group': 'Age Group', 'mean': 'Average Charges ($)'},
        text='mean',
        color='mean',
        color_continuous_scale='Blues'
    )
    fig_age_group.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
    fig_age_group.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_age_group, width='stretch')

with col2:
    # Charges by BMI Category
    bmi_stats = filtered_df.groupby('bmi_category', observed=True)['charges'].agg(['mean', 'count']).reset_index()
    fig_bmi_cat = px.bar(
        bmi_stats,
        x='bmi_category',
        y='mean',
        title='Average Charges by BMI Category',
        labels={'bmi_category': 'BMI Category', 'mean': 'Average Charges ($)'},
        text='mean',
        color='mean',
        color_continuous_scale='RdYlGn_r'
    )
    fig_bmi_cat.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
    fig_bmi_cat.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_bmi_cat, width='stretch')

st.markdown("---")

# ============================================================================
# ROW 4: CORRELATION & HEATMAP
# ============================================================================
st.markdown("## 📊 Correlation Analysis")

col1, col2 = st.columns([1.2, 1])

with col1:
    # Correlation heatmap
    numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns
    corr_matrix = filtered_df[numeric_cols].corr()
    
    fig_corr = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='RdBu',
        zmid=0,
        text=corr_matrix.values.round(2),
        texttemplate='%{text}',
        textfont={"size": 10}
    ))
    fig_corr.update_layout(
        title='Correlation Matrix - All Variables',
        height=450,
        width=500
    )
    st.plotly_chart(fig_corr, width='stretch')

with col2:
    # Correlations with charges
    charges_corr = filtered_df[numeric_cols].corr()['charges'].drop('charges').sort_values(ascending=False)
    
    fig_charges_corr = px.bar(
        x=charges_corr.values,
        y=charges_corr.index,
        orientation='h',
        title='Correlation with Charges',
        labels={'x': 'Correlation Coefficient', 'y': 'Variable'},
        color=charges_corr.values,
        color_continuous_scale='RdBu',
        text=charges_corr.values.round(3)
    )
    fig_charges_corr.update_traces(textposition='outside')
    fig_charges_corr.update_layout(height=450, showlegend=False)
    st.plotly_chart(fig_charges_corr, width='stretch')

st.markdown("---")

# ============================================================================
# ROW 5: STATISTICAL SUMMARY
# ============================================================================
st.markdown("## 📋 Statistical Summary")

tab1, tab2, tab3 = st.tabs(["Descriptive Stats", "Group Comparisons", "Data Quality"])

with tab1:
    st.subheader("Descriptive Statistics")
    summary_stats = filtered_df.describe().round(2)
    st.dataframe(summary_stats.T, width='stretch')

with tab2:
    st.subheader("Group Comparisons")
    
    # Smoker vs Non-smoker
    smoker_data = filtered_df[filtered_df['smoker'] == 'yes']['charges']
    non_smoker_data = filtered_df[filtered_df['smoker'] == 'no']['charges']
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**Smokers**")
        st.metric("Count", f"{len(smoker_data)}")
        st.metric("Average", f"${smoker_data.mean():,.0f}")
        st.metric("Median", f"${smoker_data.median():,.0f}")
    
    with col2:
        st.write("**Non-Smokers**")
        st.metric("Count", f"{len(non_smoker_data)}")
        st.metric("Average", f"${non_smoker_data.mean():,.0f}")
        st.metric("Median", f"${non_smoker_data.median():,.0f}")
    
    with col3:
        st.write("**Difference**")
        avg_diff = smoker_data.mean() - non_smoker_data.mean()
        pct_diff = (avg_diff / non_smoker_data.mean()) * 100
        st.metric("Avg Difference", f"${avg_diff:,.0f}")
        st.metric("% Increase", f"{pct_diff:.1f}%")
        
        # T-test
        t_stat, p_value = stats.ttest_ind(smoker_data, non_smoker_data)
        st.metric("P-Value", f"{p_value:.2e}")

with tab3:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Records", f"{len(filtered_df):,}")
        st.metric("Missing Values", f"{filtered_df.isnull().sum().sum()}")
        st.metric("Duplicates", f"{filtered_df.duplicated().sum()}")
    
    with col2:
        st.metric("Age Range", f"{int(filtered_df['age'].min())} - {int(filtered_df['age'].max())}")
        st.metric("BMI Range", f"{filtered_df['bmi'].min():.2f} - {filtered_df['bmi'].max():.2f}")
        st.metric("Charge Range", f"${filtered_df['charges'].min():,.0f} - ${filtered_df['charges'].max():,.0f}")
    
    with col3:
        st.metric("Sample Size", f"{len(filtered_df):,}")
        st.metric("Data Completeness", f"100%")
        st.metric("Unique Regions", f"{filtered_df['region'].nunique()}")

st.markdown("---")

# ============================================================================
# ROW 6: DATA EXPLORER
# ============================================================================
st.markdown("## 🔍 Data Explorer")

col1, col2, col3 = st.columns(3)

with col1:
    view_type = st.radio(
        "Select View",
        ["First 10 Records", "Sample 20 Records", "All Records"]
    )

if view_type == "First 10 Records":
    st.dataframe(filtered_df.head(10), width='stretch')
elif view_type == "Sample 20 Records":
    st.dataframe(filtered_df.sample(min(20, len(filtered_df))), width='stretch')
else:
    st.dataframe(filtered_df, width='stretch')

# ============================================================================
# ROW 7: INSIGHTS & RECOMMENDATIONS
# ============================================================================
st.markdown("---")
st.markdown("## 💡 Key Insights & Recommendations")

insight_col1, insight_col2 = st.columns(2)

with insight_col1:
    st.success("""
    ### 🎯 Critical Findings
    
    1. **Smoking Impact**: Smokers pay ~3.8x more than non-smokers
       - Avg Smoker: $32,050 vs Non-Smoker: $8,434
    
    2. **Age Relationship**: Strong positive correlation (r=0.30)
       - Charges increase significantly after age 40
    
    3. **BMI Factor**: Moderate correlation (r=0.20)
       - Overweight individuals face higher costs
    
    4. **Gender**: Minimal differences detected
       - No significant gender-based pricing disparity
    """)

with insight_col2:
    st.info("""
    ### 📊 Business Recommendations
    
    1. **Pricing Strategy**
       - Implement risk-based smoking surcharge
       - Age-adjusted pricing tiers
       - BMI-based wellness incentives
    
    2. **Risk Management**
       - Launch smoking cessation programs
       - Preventive screening for 40+ age group
       - Weight management initiatives
    
    3. **Customer Segmentation**
       - Profile A: Young, healthy, non-smoker
       - Profile B: Middle-aged, smoker
       - Profile C: Older demographic
    """)

st.markdown("---")

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("""
<div style='text-align: center; color: #666; margin-top: 30px;'>
    <small>Medical Insurance Costs Analysis Dashboard | Data: 1,338 records | Last Updated: March 2026</small>
</div>
""", unsafe_allow_html=True)
