"""
Professional Medical Insurance Costs Analysis Dashboard
=========================================================
Interactive Streamlit dashboard for comprehensive EDA and insights
Theme: Premium Dark Edition (Fully Verified for v1.35.0+)
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats

# ============================================================================
# 1. PAGE CONFIGURATION & PREMIUM DARK THEME INJECTION
# ============================================================================
st.set_page_config(
    page_title="Insurance Costs Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Deep Custom CSS to inject GitHub-like Dark/Slate Theme aesthetics cleanly
st.markdown("""
    <style>
    /* Global App Container */
    .stApp {
        background-color: #0E1117;
        color: #E0E2E6;
    }
    /* Sidebar styling overrides */
    section[data-testid="stSidebar"] {
        background-color: #161B22 !important;
        border-right: 1px solid #30363D;
    }
    /* Metric Display Blocks */
    div[data-testid="stMetricSimpleValue"] {
        font-size: 1.9rem !important;
        font-weight: 700 !important;
        color: #00D2FF !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #9BA1A6 !important;
        font-size: 0.95rem !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    /* Corporate Styled Content Info Boxes */
    .insight-card-green {
        background-color: #161B22; 
        padding: 20px; 
        border-radius: 8px; 
        border: 1px solid #30363D;
        border-left: 5px solid #10AC84;
        margin-bottom: 15px;
    }
    .insight-card-blue {
        background-color: #161B22; 
        padding: 20px; 
        border-radius: 8px; 
        border: 1px solid #30363D;
        border-left: 5px solid #00D2FF;
        margin-bottom: 15px;
    }
    /* Streamlit Native Elements Theme Fixes */
    button[data-baseweb="tab"] {
        color: #8B949E !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #00D2FF !important;
        border-bottom-color: #00D2FF !important;
    }
    hr {
        border-color: #21262D !important;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# 2. DATA LOADING & CACHING PIPELINE (MUTATION PROOF)
# ============================================================================
@st.cache_data
def load_raw_data():
    """Single point of data ingestion cached safely to prevent memory fragmentation"""
    return pd.read_csv('insurance.csv')

def get_processed_data():
    """Process data on a clean memory copy to completely isolate cached elements"""
    try:
        df = load_raw_data().copy()
    except FileNotFoundError:
        st.error("❌ Critical Error: 'insurance.csv' file not found in execution directory.")
        st.stop()
    except Exception as e:
        st.error(f"❌ Error initializing dataset pipeline: {str(e)}")
        st.stop()
    
    # Enforcing strict data-type safety boundaries
    df['sex'] = df['sex'].astype(str).astype('category')
    df['smoker'] = df['smoker'].astype(str).astype('category')
    df['region'] = df['region'].astype(str).astype('category')
    
    # Statistical demographic partitioning
    df['age_group'] = pd.cut(df['age'], bins=[0, 25, 35, 50, 100], 
                             labels=['18-25', '26-35', '36-50', '50+'])
    
    df['bmi_category'] = pd.cut(df['bmi'], bins=[0, 18.5, 25, 30, 100],
                                labels=['Underweight', 'Normal', 'Overweight', 'Obese'])
    return df

# Main Dataframe Instance
df = get_processed_data()

# ============================================================================
# 3. ENTERPRISE SIDEBAR FILTERS CONTROL CENTER
# ============================================================================
st.sidebar.title("🎯 Control Panel & Filters")
st.sidebar.markdown("Use the elements below to slice the underlying operational data.")

# Parsing safe list representations for multi-select engines
unique_smokers = [str(x) for x in df['smoker'].unique().tolist()]
unique_regions = [str(x) for x in df['region'].unique().tolist()]

smoker_filter = st.sidebar.multiselect(
    "Select Smoker Status",
    options=unique_smokers,
    default=unique_smokers
)

region_filter = st.sidebar.multiselect(
    "Select Geographical Regions",
    options=unique_regions,
    default=unique_regions
)

# Numeric Continuous Range Selectors
age_range = st.sidebar.slider(
    "Target Age Cohort",
    min_value=int(df['age'].min()),
    max_value=int(df['age'].max()),
    value=(int(df['age'].min()), int(df['age'].max()))
)

bmi_range = st.sidebar.slider(
    "Target BMI Distribution Range",
    min_value=float(df['bmi'].min()),
    max_value=float(df['bmi'].max()),
    value=(float(df['bmi'].min()), float(df['bmi'].max()))
)

# Dynamic Logical Slice Query execution
filtered_df = df[
    (df['smoker'].isin(smoker_filter)) &
    (df['region'].isin(region_filter)) &
    (df['age'] >= age_range[0]) &
    (df['age'] <= age_range[1]) &
    (df['bmi'] >= bmi_range[0]) &
    (df['bmi'] <= bmi_range[1])
]

st.sidebar.markdown("---")
# Dynamic Runtime Data Analytics Reporting inside Sidebar Dashboard Canvas
if len(filtered_df) == 0:
    st.sidebar.warning("⚠️ No database records match the selected slice vectors.")
    st.sidebar.info(f"📊 Active Records: 0 / {len(df):,}")
else:
    st.sidebar.info(f"📊 Active Records Matrix: {len(filtered_df):,} / {len(df):,}")

# ============================================================================
# 4. PLOTLY CANVAS GLOBAL STYLING FACTORY
# ============================================================================
def apply_dark_theme(fig):
    """Enforces premium uniform enterprise typography, coloring and layout on all charts"""
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#161B22",
        plot_bgcolor="#161B22",
        font=dict(color="#E0E2E6", family="Inter, system-ui, sans-serif"),
        margin=dict(l=50, r=40, t=60, b=50),
        legend=dict(
            bgcolor="rgba(22,27,34,0.8)",
            bordercolor="#30363D",
            borderwidth=1
        )
    )
    # Ensure axes lines look pristine across high-res dashboards
    fig.update_xaxes(showgrid=True, gridcolor="#21262D", zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor="#21262D", zeroline=False)
    return fig

# ============================================================================
# 5. HEADER COMPONENT
# ============================================================================
st.markdown("<h1 style='text-align: center; color: #00D2FF; margin-bottom: 0; font-weight: 800;'>💰 Medical Insurance Costs Analysis Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8B949E; font-size: 1.15em; margin-top: 5px;'>Production-Grade Enterprise Analytics & Biostatistics Framework</p><br>", unsafe_allow_html=True)

# Halt executing plots gracefully if filtered dataframe collapses to zero rows
if len(filtered_df) == 0:
    st.warning("⚠️ Active dataset segment contains no records. Please widen your sidebar dashboard filters to populate graph views.")
    st.stop()

# ============================================================================
# 6. HIGH LEVEL INDUSTRIAL KPI METRICS BAR
# ============================================================================
kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5 = st.columns(5)

with kpi_col1:
    st.metric(
        label="Total Sample Size",
        value=f"{len(filtered_df):,}",
        delta=f"{len(filtered_df) - len(df):,}" if len(filtered_df) != len(df) else None
    )

with kpi_col2:
    current_avg_charge = filtered_df['charges'].mean()
    st.metric(
        label="Avg Premium Charges",
        value=f"${current_avg_charge:,.2f}",
        delta=f"${current_avg_charge - df['charges'].mean():,.2f}" if len(filtered_df) != len(df) else None
    )

with kpi_col3:
    st.metric(
        label="Median Premium Cost",
        value=f"${filtered_df['charges'].median():,.2f}"
    )

with kpi_col4:
    active_smoker_ratio = (filtered_df['smoker'] == 'yes').sum() / len(filtered_df) * 100
    st.metric(
        label="Smoker Ratio %",
        value=f"{active_smoker_ratio:.1f}%"
    )

with kpi_col5:
    current_avg_age = filtered_df['age'].mean()
    st.metric(
        label="Mean Cohort Age",
        value=f"{current_avg_age:.1f} yrs",
        delta=f"{current_avg_age - df['age'].mean():.1f} yrs" if len(filtered_df) != len(df) else None
    )

st.markdown("<hr>", unsafe_allow_html=True)

# ============================================================================
# 7. ROW 1: MATHEMATICAL DATA DISTRIBUTIONS
# ============================================================================
st.markdown("### 📈 Mathematical Core Data Distributions")
dist_col1, dist_col2 = st.columns(2)

with dist_col1:
    fig_hist_charges = px.histogram(
        filtered_df, x='charges', nbins=40,
        title='Probability Distribution Density of Insurance Charges',
        labels={'charges': 'Charges ($)', 'count': 'Frequency'},
        color_discrete_sequence=['#00D2FF']
    )
    st.plotly_chart(apply_dark_theme(fig_hist_charges), use_container_width=True)

with dist_col2:
    fig_hist_age = px.histogram(
        filtered_df, x='age', nbins=30,
        title='Demographic Distribution Density of Cohort Age',
        labels={'age': 'Age (Years)', 'count': 'Frequency'},
        color_discrete_sequence=['#FF9F43']
    )
    st.plotly_chart(apply_dark_theme(fig_hist_age), use_container_width=True)

# Sub-row for categorical subplots and continuous BMI distributions
dist_col3, dist_col4 = st.columns(2)

with dist_col3:
    fig_hist_bmi = px.histogram(
        filtered_df, x='bmi', nbins=35,
        title='Biometric Distribution Density of Body Mass Index (BMI)',
        labels={'bmi': 'BMI Metric Value', 'count': 'Frequency'},
        color_discrete_sequence=['#10AC84']
    )
    st.plotly_chart(apply_dark_theme(fig_hist_bmi), use_container_width=True)

with dist_col4:
    # Safe categorical share mapping via a Plotly Subplot Matrix
    fig_pie_matrix = make_subplots(
        rows=1, cols=3,
        specs=[[{'type':'pie'}, {'type':'pie'}, {'type':'pie'}]],
        subplot_titles=('Gender Breakdown', 'Smoking Cohorts', 'Geographical Regions')
    )
    
    brand_palette = ['#00D2FF', '#FF9F43', '#10AC84', '#EE5253']
    
    sex_values = filtered_df['sex'].value_counts()
    fig_pie_matrix.add_trace(go.Pie(labels=sex_values.index.tolist(), values=sex_values.values.tolist(), marker=dict(colors=brand_palette), hole=0.3), row=1, col=1)
    
    smoker_values = filtered_df['smoker'].value_counts()
    fig_pie_matrix.add_trace(go.Pie(labels=smoker_values.index.tolist(), values=smoker_values.values.tolist(), marker=dict(colors=brand_palette), hole=0.3), row=1, col=2)
    
    region_values = filtered_df['region'].value_counts()
    fig_pie_matrix.add_trace(go.Pie(labels=region_values.index.tolist(), values=region_values.values.tolist(), marker=dict(colors=brand_palette), hole=0.3), row=1, col=3)
    
    fig_pie_matrix.update_layout(height=380, showlegend=True)
    st.plotly_chart(apply_dark_theme(fig_pie_matrix), use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ============================================================================
# 8. ROW 2: ADVANCED FEATURE INTERACTION & REGRESSION MATRIX
# ============================================================================
st.markdown("### 🔗 Bivariate Feature Interactions & Ordinary Least Squares (OLS) Trendlines")
interact_col1, interact_col2 = st.columns(2)

with interact_col1:
    fig_scat_age = px.scatter(
        filtered_df, x='age', y='charges', color='smoker',
        title='Linear Co-progression Analysis: Age vs Premium Charges',
        labels={'age': 'Age (Years)', 'charges': 'Charges ($)', 'smoker': 'Smoker Status'},
        color_discrete_map={'yes': '#EE5253', 'no': '#10AC84'},
        opacity=0.75, trendline='ols', trendline_color_override='#00D2FF'
    )
    st.plotly_chart(apply_dark_theme(fig_scat_age), use_container_width=True)

with interact_col2:
    fig_scat_bmi = px.scatter(
        filtered_df, x='bmi', y='charges', color='smoker',
        title='Risk Escalation Analysis: BMI vs Premium Charges',
        labels={'bmi': 'Body Mass Index', 'charges': 'Charges ($)', 'smoker': 'Smoker Status'},
        color_discrete_map={'yes': '#EE5253', 'no': '#10AC84'},
        opacity=0.75, trendline='ols', trendline_color_override='#FF9F43'
    )
    st.plotly_chart(apply_dark_theme(fig_scat_bmi), use_container_width=True)

# Additional Bivariate Categorical Box Plots to observe distribution spread/outliers
interact_col3, interact_col4 = st.columns(2)

with interact_col3:
    fig_box_children = px.box(
        filtered_df, x='children', y='charges', color='smoker',
        title='Impact Assessment: Dependent Family Count Variance vs Premium Tolls',
        labels={'children': 'Number of Dependent Children', 'charges': 'Charges ($)'},
        color_discrete_map={'yes': '#EE5253', 'no': '#10AC84'}
    )
    st.plotly_chart(apply_dark_theme(fig_box_children), use_container_width=True)

with interact_col4:
    fig_box_smoker = px.box(
        filtered_df, x='smoker', y='charges', color='smoker',
        title='Statistical Variance: Quantile Dispersion of Smoker Premium Costs',
        labels={'smoker': 'Smoker Cohort Type', 'charges': 'Charges ($)'},
        color_discrete_map={'yes': '#EE5253', 'no': '#10AC84'}
    )
    st.plotly_chart(apply_dark_theme(fig_box_smoker), use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ============================================================================
# 9. ROW 3: DEEP STATISTICAL DEMOGRAPHIC SEGMENTATION
# ============================================================================
st.markdown("### 🎯 Categorical Deep Demographic Aggregations")
segment_col1, segment_col2 = st.columns(2)

with segment_col1:
    sex_metrics = filtered_df.groupby('sex', observed=True)['charges'].agg(['mean', 'median', 'count']).reset_index()
    fig_bar_sex = px.bar(
        sex_metrics, x='sex', y='mean',
        title='Cost Disparity: Mean Financial Premium Demands by Sex',
        labels={'sex': 'Gender Category', 'mean': 'Mean Charge Rate ($)'},
        text='mean', color='sex', color_discrete_map={'male': '#00D2FF', 'female': '#FF9F43'}
    )
    # Fix potential layout overlapping with y-axis scaling adjustments
    fig_bar_sex.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
    fig_bar_sex.update_yaxes(range=[0, sex_metrics['mean'].max() * 1.25])
    st.plotly_chart(apply_dark_theme(fig_bar_sex), use_container_width=True)

with segment_col2:
    region_metrics = filtered_df.groupby('region', observed=True)['charges'].agg(['mean', 'count']).reset_index().sort_values('mean', ascending=False)
    fig_bar_region = px.bar(
        region_metrics, x='region', y='mean',
        title='Geographical Risk Vector Metrics: Region Cost Layout',
        labels={'region': 'Geographic Cluster', 'mean': 'Mean Charge Rate ($)'},
        text='mean', color='mean', color_continuous_scale='Turbo'
    )
    fig_bar_region.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
    fig_bar_region.update_yaxes(range=[0, region_metrics['mean'].max() * 1.25])
    st.plotly_chart(apply_dark_theme(fig_bar_region), use_container_width=True)

segment_col3, segment_col4 = st.columns(2)

with segment_col3:
    age_grp_metrics = filtered_df.groupby('age_group', observed=True)['charges'].agg(['mean', 'count']).reset_index()
    fig_bar_agegp = px.bar(
        age_grp_metrics, x='age_group', y='mean',
        title='Stratified Cohort Analysis: Age Categories vs Cost Impact',
        labels={'age_group': 'Generational Segment', 'mean': 'Mean Charge Rate ($)'},
        text='mean', color='mean', color_continuous_scale='Viridis'
    )
    fig_bar_agegp.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
    fig_bar_agegp.update_yaxes(range=[0, age_grp_metrics['mean'].max() * 1.25])
    st.plotly_chart(apply_dark_theme(fig_bar_agegp), use_container_width=True)

with segment_col4:
    bmi_grp_metrics = filtered_df.groupby('bmi_category', observed=True)['charges'].agg(['mean', 'count']).reset_index()
    fig_bar_bmigp = px.bar(
        bmi_grp_metrics, x='bmi_category', y='mean',
        title='Biometric Classification Analysis: BMI Category Weight Metrics',
        labels={'bmi_category': 'Clinical Categorization', 'mean': 'Mean Charge Rate ($)'},
        text='mean', color='mean', color_continuous_scale='Cividis'
    )
    fig_bar_bmigp.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
    fig_bar_bmigp.update_yaxes(range=[0, bmi_grp_metrics['mean'].max() * 1.25])
    st.plotly_chart(apply_dark_theme(fig_bar_bmigp), use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ============================================================================
# 10. ROW 4: MATHEMATICAL CORRELATION MATRIX HEATMAPS
# ============================================================================
st.markdown("### 📊 Correlation Linear Heatmap Architecture")
corr_col1, corr_col2 = st.columns([1.2, 1])

# Isolate numeric metrics safely to support Pandas 2.2.2 requirements
numeric_features = filtered_df.select_dtypes(include=[np.number])
correlation_matrix = numeric_features.corr()

with corr_col1:
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=correlation_matrix.values,
        x=correlation_matrix.columns.tolist(),
        y=correlation_matrix.columns.tolist(),
        colorscale='Electric',
        zmin=-1, zmax=1,
        text=correlation_matrix.values.round(3),
        texttemplate='%{text}',
        textfont={"size": 12, "weight": "bold"}
    ))
    fig_heatmap.update_layout(title='Full Multi-Feature Linear Association Matrix', height=450)
    st.plotly_chart(apply_dark_theme(fig_heatmap), use_container_width=True)

with corr_col2:
    target_association = correlation_matrix['charges'].drop('charges').sort_values(ascending=False)
    fig_target_bar = px.bar(
        x=target_association.values, y=target_association.index, orientation='h',
        title='Direct Lineal Component Correlation with Insurance Premium Costs',
        labels={'x': 'Pearson Correlation Metric Score (r)', 'y': 'Dataset Feature Header'},
        color=target_association.values, color_continuous_scale='Bluered_r',
        text=target_association.values.round(3)
    )
    fig_target_bar.update_traces(textposition='outside')
    fig_target_bar.update_layout(height=450)
    st.plotly_chart(apply_dark_theme(fig_target_bar), use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ============================================================================
# 11. ROW 5: ADVANCED STATISTICAL COMPUTATION ENGINE (HYPOTHESIS TESTING)
# ============================================================================
st.markdown("### 📋 Advanced Industrial Biostatistics Validation Summary")
tab_desc, tab_hypothesis, tab_integrity = st.tabs([
    "Descriptive Aggregation Engine", 
    "Hypothesis Testing (Biostatistics Verification)", 
    "Data Pipeline Pipeline Audit Log"
])

with tab_desc:
    # Render descriptive matrix with clean styling formatting
    st.dataframe(filtered_df.describe().round(2).T, use_container_width=True)

with tab_hypothesis:
    smoker_cohort_charges = filtered_df[filtered_df['smoker'] == 'yes']['charges']
    non_smoker_cohort_charges = filtered_df[filtered_df['smoker'] == 'no']['charges']
    
    stat_col1, stat_col2, stat_col3 = st.columns(3)
    
    with stat_col1:
        st.markdown("**Smokers Cohort Parameters**")
        st.metric("Total Sample Size ($N_1$)", f"{len(smoker_cohort_charges)}")
        if len(smoker_cohort_charges) > 0:
            st.metric("Sample Mean ($\mu_1$)", f"${smoker_cohort_charges.mean():,.2f}")
            st.metric("Sample Variance ($\sigma^2_1$)", f"{smoker_cohort_charges.var():,.2f}")

    with stat_col2:
        st.markdown("**Non-Smokers Cohort Parameters**")
        st.metric("Total Sample Size ($N_2$)", f"{len(non_smoker_cohort_charges)}")
        if len(non_smoker_cohort_charges) > 0:
            st.metric("Sample Mean ($\mu_2$)", f"${non_smoker_cohort_charges.mean():,.2f}")
            st.metric("Sample Variance ($\sigma^2_2$)", f"{non_smoker_cohort_charges.var():,.2f}")

    with stat_col3:
        st.markdown("**Inferential Hypothesis Machine**")
        # Run robust validation check to verify data integrity before running scipy distributions
        if len(smoker_cohort_charges) > 1 and len(non_smoker_cohort_charges) > 1 and smoker_cohort_charges.nunique() > 1 and non_smoker_cohort_charges.nunique() > 1:
            # Welch's T-Test calculation handling unequal group variance safely
            t_statistic, computation_p_value = stats.ttest_ind(smoker_cohort_charges, non_smoker_cohort_charges, equal_var=False)
            st.metric("Welch's T-Statistic Score", f"{t_statistic:.4f}")
            st.metric("Calculated P-Value Output", f"{computation_p_value:.4e}")
            
            if computation_p_value < 0.05:
                st.success("✔ Analysis Matrix Verdict: Rejection of Null Hypothesis. Variance is highly statistically significant.")
            else:
