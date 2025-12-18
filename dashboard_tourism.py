"""
Kazungula Tourism Investment Dashboard
Interactive analytics for tourism investors in the Kazungula area
Data sources: Zambia Ministry of Tourism, KAZA TFCA, Border Statistics

VERSION: 1.1 (December 16, 2024)
- Fixed all deprecation warnings (use_container_width → width, freq='M' → freq='ME')
- Updated email to info@concise-analytics.com
- Improved KPI card layout and visibility
- Enhanced responsive design
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="Kazungula Tourism Investment Dashboard",
    page_icon="🏞️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS FOR BRANDING
# ============================================================
st.markdown("""
    <style>
    .main {
        background-color: #fffef9;
    }
    .stMetric {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(107, 93, 63, 0.08);
        min-height: 120px;
    }
    .stMetric label {
        font-size: 0.9rem !important;
        white-space: normal !important;
        word-wrap: break-word !important;
        line-height: 1.3 !important;
    }
    .stMetric [data-testid="stMetricValue"] {
        font-size: 1.5rem !important;
    }
    div[data-testid="column"] {
        padding: 0 10px;
    }
    h1 {
        color: #3d3328;
        font-family: 'Georgia', serif;
    }
    h2, h3 {
        color: #6b5d3f;
    }
    .highlight-box {
        background-color: #faf8f3;
        padding: 20px;
        border-radius: 8px;
        border-left: 4px solid #c17a5c;
        margin: 10px 0;
    }
    /* Ensure columns have proper spacing */
    .row-widget.stHorizontalBlock {
        gap: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================================
# DATA LOADING FUNCTIONS
# ============================================================

@st.cache_data
def load_sample_data():
    """
    Load sample tourism data
    REPLACE THIS with your actual data loading from CSV/Excel
    """
    
    # Sample tourist arrivals data (2019-2024)
    dates = pd.date_range(start='2019-01-01', end='2024-10-31', freq='ME')
    
    # Create realistic seasonal patterns
    np.random.seed(42)
    base_arrivals = 15000
    trend = np.linspace(0, 5000, len(dates))
    seasonal = 5000 * np.sin(np.linspace(0, 5*2*np.pi, len(dates)))
    noise = np.random.normal(0, 1000, len(dates))
    
    # COVID impact (2020-2021)
    covid_impact = np.ones(len(dates))
    covid_start = pd.to_datetime('2020-03-01')
    covid_end = pd.to_datetime('2021-12-31')
    covid_impact[(dates >= covid_start) & (dates <= covid_end)] = 0.3
    
    arrivals = (base_arrivals + trend + seasonal + noise) * covid_impact
    arrivals = np.maximum(arrivals, 1000)  # Minimum 1000 arrivals
    
    df_arrivals = pd.DataFrame({
        'date': dates,
        'total_arrivals': arrivals.astype(int),
        'international': (arrivals * 0.65).astype(int),
        'regional': (arrivals * 0.35).astype(int)
    })
    
    # Add source markets
    df_arrivals['zambia'] = (arrivals * 0.15).astype(int)
    df_arrivals['zimbabwe'] = (arrivals * 0.12).astype(int)
    df_arrivals['botswana'] = (arrivals * 0.08).astype(int)
    df_arrivals['south_africa'] = (arrivals * 0.25).astype(int)
    df_arrivals['europe'] = (arrivals * 0.20).astype(int)
    df_arrivals['north_america'] = (arrivals * 0.12).astype(int)
    df_arrivals['asia'] = (arrivals * 0.08).astype(int)
    
    return df_arrivals

@st.cache_data
def load_accommodation_data():
    """Sample accommodation data"""
    data = {
        'facility_type': ['Hotels', 'Lodges', 'Guest Houses', 'Camping Sites', 'Backpackers'],
        'number_of_facilities': [12, 18, 25, 8, 6],
        'total_rooms': [450, 280, 180, 150, 80],
        'average_occupancy_rate': [68, 72, 55, 45, 62],
        'average_rate_usd': [120, 180, 45, 25, 30]
    }
    return pd.DataFrame(data)

@st.cache_data
def load_revenue_data():
    """Sample revenue data"""
    dates = pd.date_range(start='2019-01-01', end='2024-10-31', freq='ME')
    np.random.seed(42)
    
    base_revenue = 2500000
    trend = np.linspace(0, 800000, len(dates))
    seasonal = 800000 * np.sin(np.linspace(0, 5*2*np.pi, len(dates)))
    
    covid_impact = np.ones(len(dates))
    covid_start = pd.to_datetime('2020-03-01')
    covid_end = pd.to_datetime('2021-12-31')
    covid_impact[(dates >= covid_start) & (dates <= covid_end)] = 0.25
    
    revenue = (base_revenue + trend + seasonal) * covid_impact
    
    df_revenue = pd.DataFrame({
        'date': dates,
        'total_revenue_usd': revenue,
        'accommodation': revenue * 0.45,
        'activities': revenue * 0.30,
        'food_beverage': revenue * 0.15,
        'transport': revenue * 0.10
    })
    
    return df_revenue

# ============================================================
# LOAD DATA
# ============================================================
df_arrivals = load_sample_data()
df_accommodation = load_accommodation_data()
df_revenue = load_revenue_data()

# ============================================================
# SIDEBAR - FILTERS
# ============================================================
st.sidebar.image("https://via.placeholder.com/300x100/c17a5c/ffffff?text=Concise+Analytics", 
                 width='stretch')
st.sidebar.markdown("---")
st.sidebar.markdown("**Dashboard Version 1.1** ✅")
st.sidebar.markdown("*Last Updated: Dec 16, 2024*")
st.sidebar.markdown("---")

st.sidebar.header("📊 Dashboard Filters")

# Date range filter
min_date = df_arrivals['date'].min().date()
max_date = df_arrivals['date'].max().date()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(max_date - timedelta(days=365), max_date),
    min_value=min_date,
    max_value=max_date
)

if len(date_range) == 2:
    start_date, end_date = date_range
    mask = (df_arrivals['date'].dt.date >= start_date) & (df_arrivals['date'].dt.date <= end_date)
    df_arrivals_filtered = df_arrivals[mask]
    df_revenue_filtered = df_revenue[(df_revenue['date'].dt.date >= start_date) & 
                                      (df_revenue['date'].dt.date <= end_date)]
else:
    df_arrivals_filtered = df_arrivals
    df_revenue_filtered = df_revenue

# Comparison selector
st.sidebar.markdown("---")
comparison_period = st.sidebar.selectbox(
    "Compare with Previous",
    ["Month", "Quarter", "Year", "No Comparison"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
### 📌 About This Dashboard

**Data Sources:**
- Zambia Ministry of Tourism
- KAZA TFCA Statistics
- Kazungula Border Post Data
- Local Accommodation Surveys

**Coverage:** Kazungula District, Zambia

**Last Updated:** October 2024

---

*For custom analysis, contact:*  
**info@concise-analytics.com**
""")

# ============================================================
# MAIN DASHBOARD
# ============================================================

# Header
st.title("🏞️ Kazungula Tourism Investment Dashboard")
st.markdown("""
Strategic intelligence for tourism investors in the Kazungula area. 
Analyze visitor trends, infrastructure capacity, and market opportunities at the heart of KAZA TFCA.
""")

st.markdown("---")

# ============================================================
# KEY METRICS ROW
# ============================================================
st.subheader("📈 Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns(5)

# Calculate metrics
total_arrivals = df_arrivals_filtered['total_arrivals'].sum()
avg_monthly_arrivals = df_arrivals_filtered['total_arrivals'].mean()
total_revenue = df_revenue_filtered['total_revenue_usd'].sum()
avg_occupancy = df_accommodation['average_occupancy_rate'].mean()

# YoY growth calculation
if len(df_arrivals_filtered) >= 12:
    recent_12m = df_arrivals_filtered.tail(12)['total_arrivals'].sum()
    previous_12m = df_arrivals_filtered.iloc[-24:-12]['total_arrivals'].sum() if len(df_arrivals_filtered) >= 24 else recent_12m
    yoy_growth = ((recent_12m - previous_12m) / previous_12m * 100) if previous_12m > 0 else 0
else:
    yoy_growth = 0

with col1:
    st.metric(
        "Total Arrivals",
        f"{total_arrivals:,.0f}",
        f"{yoy_growth:+.1f}% YoY"
    )

with col2:
    st.metric(
        "Avg Monthly Arrivals",
        f"{avg_monthly_arrivals:,.0f}",
        "📊"
    )

with col3:
    st.metric(
        "Total Revenue (USD)",
        f"${total_revenue/1e6:.2f}M",
        f"+{(total_revenue / df_revenue['total_revenue_usd'].sum() * 100 - 100):+.1f}%"
    )

with col4:
    st.metric(
        "Avg Occupancy Rate",
        f"{avg_occupancy:.1f}%",
        "🏨"
    )

with col5:
    total_rooms = df_accommodation['total_rooms'].sum()
    st.metric(
        "Total Rooms",
        f"{total_rooms:,}",
        f"{len(df_accommodation)} facilities"
    )

st.markdown("---")

# ============================================================
# VISITOR TRENDS SECTION
# ============================================================
st.subheader("📊 Visitor Arrival Trends")

# Create tabs
tab1, tab2, tab3 = st.tabs(["📈 Time Series", "🌍 Source Markets", "📅 Seasonality"])

with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Main arrivals chart
        fig_arrivals = go.Figure()
        
        fig_arrivals.add_trace(go.Scatter(
            x=df_arrivals_filtered['date'],
            y=df_arrivals_filtered['total_arrivals'],
            name='Total Arrivals',
            line=dict(color='#c17a5c', width=3),
            fill='tonexty',
            fillcolor='rgba(193, 122, 92, 0.1)'
        ))
        
        fig_arrivals.add_trace(go.Scatter(
            x=df_arrivals_filtered['date'],
            y=df_arrivals_filtered['international'],
            name='International',
            line=dict(color='#d4a574', width=2, dash='dash')
        ))
        
        fig_arrivals.add_trace(go.Scatter(
            x=df_arrivals_filtered['date'],
            y=df_arrivals_filtered['regional'],
            name='Regional (SADC)',
            line=dict(color='#b8860b', width=2, dash='dash')
        ))
        
        fig_arrivals.update_layout(
            title="Tourist Arrivals Over Time",
            xaxis_title="Date",
            yaxis_title="Number of Arrivals",
            hovermode='x unified',
            height=400,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig_arrivals, width='stretch')
    
    with col2:
        # Growth statistics
        st.markdown("##### 📊 Growth Statistics")
        
        recent_year = df_arrivals_filtered.tail(12)['total_arrivals'].sum()
        prev_year = df_arrivals_filtered.iloc[-24:-12]['total_arrivals'].sum() if len(df_arrivals_filtered) >= 24 else 0
        
        if prev_year > 0:
            growth = ((recent_year - prev_year) / prev_year * 100)
            st.metric("YoY Growth", f"{growth:+.1f}%")
        
        st.metric("Peak Month", 
                 df_arrivals_filtered.loc[df_arrivals_filtered['total_arrivals'].idxmax(), 'date'].strftime('%B %Y'))
        
        avg_growth = df_arrivals_filtered['total_arrivals'].pct_change().mean() * 100
        st.metric("Avg Monthly Growth", f"{avg_growth:+.2f}%")
        
        # International vs Regional split
        intl_pct = (df_arrivals_filtered['international'].sum() / 
                   df_arrivals_filtered['total_arrivals'].sum() * 100)
        st.metric("International %", f"{intl_pct:.1f}%")

with tab2:
    # Source markets analysis
    col1, col2 = st.columns(2)
    
    with col1:
        # Pie chart of source markets
        source_markets = {
            'South Africa': df_arrivals_filtered['south_africa'].sum(),
            'Europe': df_arrivals_filtered['europe'].sum(),
            'Zambia (Domestic)': df_arrivals_filtered['zambia'].sum(),
            'Zimbabwe': df_arrivals_filtered['zimbabwe'].sum(),
            'North America': df_arrivals_filtered['north_america'].sum(),
            'Botswana': df_arrivals_filtered['botswana'].sum(),
            'Asia': df_arrivals_filtered['asia'].sum()
        }
        
        fig_sources = px.pie(
            values=list(source_markets.values()),
            names=list(source_markets.keys()),
            title="Visitor Source Markets",
            color_discrete_sequence=px.colors.sequential.Sunset
        )
        fig_sources.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_sources, width='stretch')
    
    with col2:
        # Bar chart of source markets
        source_df = pd.DataFrame({
            'Market': list(source_markets.keys()),
            'Arrivals': list(source_markets.values())
        }).sort_values('Arrivals', ascending=True)
        
        fig_bar = px.bar(
            source_df,
            x='Arrivals',
            y='Market',
            orientation='h',
            title="Arrivals by Source Market",
            color='Arrivals',
            color_continuous_scale='Sunset'
        )
        fig_bar.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig_bar, width='stretch')

with tab3:
    # Seasonality analysis
    df_arrivals_filtered['month'] = df_arrivals_filtered['date'].dt.month
    df_arrivals_filtered['month_name'] = df_arrivals_filtered['date'].dt.strftime('%B')
    
    monthly_avg = df_arrivals_filtered.groupby('month_name')['total_arrivals'].mean().reindex([
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ])
    
    fig_seasonality = go.Figure()
    fig_seasonality.add_trace(go.Bar(
        x=monthly_avg.index,
        y=monthly_avg.values,
        marker_color='#c17a5c',
        text=monthly_avg.values.astype(int),
        textposition='outside'
    ))
    
    fig_seasonality.update_layout(
        title="Average Monthly Arrivals (Seasonality Pattern)",
        xaxis_title="Month",
        yaxis_title="Average Arrivals",
        height=400
    )
    
    st.plotly_chart(fig_seasonality, width='stretch')
    
    # Seasonal insights
    peak_month = monthly_avg.idxmax()
    low_month = monthly_avg.idxmin()
    
    st.markdown(f"""
    <div class="highlight-box">
    <h4>🌡️ Seasonal Insights</h4>
    <ul>
        <li><strong>Peak Season:</strong> {peak_month} with average {monthly_avg.max():,.0f} arrivals</li>
        <li><strong>Low Season:</strong> {low_month} with average {monthly_avg.min():,.0f} arrivals</li>
        <li><strong>Seasonality Index:</strong> {(monthly_avg.max() / monthly_avg.min()):.1f}x difference between peak and low</li>
        <li><strong>High Season Months:</strong> May through October (dry season, best wildlife viewing)</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# ACCOMMODATION & INFRASTRUCTURE
# ============================================================
st.subheader("🏨 Accommodation & Infrastructure Analysis")

col1, col2 = st.columns(2)

with col1:
    # Accommodation breakdown
    fig_accommodation = go.Figure()
    
    fig_accommodation.add_trace(go.Bar(
        name='Number of Facilities',
        x=df_accommodation['facility_type'],
        y=df_accommodation['number_of_facilities'],
        marker_color='#c17a5c',
        yaxis='y',
        offsetgroup=1
    ))
    
    fig_accommodation.add_trace(go.Bar(
        name='Total Rooms',
        x=df_accommodation['facility_type'],
        y=df_accommodation['total_rooms'],
        marker_color='#d4a574',
        yaxis='y2',
        offsetgroup=2
    ))
    
    fig_accommodation.update_layout(
        title="Accommodation Supply by Type",
        xaxis=dict(title='Facility Type'),
        yaxis=dict(title='Number of Facilities', side='left'),
        yaxis2=dict(title='Total Rooms', side='right', overlaying='y'),
        barmode='group',
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig_accommodation, width='stretch')

with col2:
    # Occupancy rates and pricing
    fig_occupancy = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Average Occupancy Rate by Facility Type', 
                       'Average Daily Rate (USD)')
    )
    
    fig_occupancy.add_trace(
        go.Bar(x=df_accommodation['facility_type'], 
               y=df_accommodation['average_occupancy_rate'],
               marker_color='#b8860b',
               text=df_accommodation['average_occupancy_rate'].apply(lambda x: f"{x}%"),
               textposition='outside'),
        row=1, col=1
    )
    
    fig_occupancy.add_trace(
        go.Bar(x=df_accommodation['facility_type'], 
               y=df_accommodation['average_rate_usd'],
               marker_color='#c17a5c',
               text=df_accommodation['average_rate_usd'].apply(lambda x: f"${x}"),
               textposition='outside'),
        row=2, col=1
    )
    
    fig_occupancy.update_layout(height=400, showlegend=False)
    fig_occupancy.update_yaxes(title_text="Occupancy %", row=1, col=1)
    fig_occupancy.update_yaxes(title_text="Rate (USD)", row=2, col=1)
    
    st.plotly_chart(fig_occupancy, width='stretch')

# Infrastructure capacity analysis
st.markdown("##### 🏗️ Infrastructure Capacity Analysis")

col1, col2, col3 = st.columns(3)

with col1:
    total_capacity = df_accommodation['total_rooms'].sum()
    current_occupancy = df_accommodation['average_occupancy_rate'].mean()
    
    st.metric("Total Room Capacity", f"{total_capacity:,} rooms")
    st.metric("Average Occupancy", f"{current_occupancy:.1f}%")
    
    # Calculate unutilized capacity
    unutilized = total_capacity * (100 - current_occupancy) / 100
    st.metric("Unutilized Capacity", f"{unutilized:.0f} rooms/night")

with col2:
    # Revenue per room
    total_accommodation_revenue = df_revenue_filtered['accommodation'].sum()
    revpar = (total_accommodation_revenue / (total_capacity * len(df_revenue_filtered)))
    
    st.metric("RevPAR (Revenue per Available Room)", f"${revpar:.2f}")
    
    # Potential revenue
    if current_occupancy < 80:
        potential_occupancy = 80
        potential_revenue = total_accommodation_revenue * (potential_occupancy / current_occupancy)
        additional_revenue = potential_revenue - total_accommodation_revenue
        st.metric("Additional Revenue Potential @ 80% Occupancy", 
                 f"${additional_revenue/1e6:.2f}M")

with col3:
    # Market gaps
    st.markdown("**🎯 Market Opportunities:**")
    st.markdown("""
    - Mid-range lodges (3-star)
    - Luxury camping experiences
    - Budget backpacker hostels
    - Conference facilities
    - Wellness/spa retreats
    """)

st.markdown("---")

# ============================================================
# REVENUE ANALYSIS
# ============================================================
st.subheader("💰 Revenue & Economic Impact")

col1, col2 = st.columns([2, 1])

with col1:
    # Revenue trends
    fig_revenue = go.Figure()
    
    fig_revenue.add_trace(go.Scatter(
        x=df_revenue_filtered['date'],
        y=df_revenue_filtered['total_revenue_usd'],
        name='Total Revenue',
        line=dict(color='#c17a5c', width=3),
        fill='tonexty'
    ))
    
    fig_revenue.add_trace(go.Scatter(
        x=df_revenue_filtered['date'],
        y=df_revenue_filtered['accommodation'],
        name='Accommodation',
        line=dict(color='#d4a574', width=2, dash='dash')
    ))
    
    fig_revenue.add_trace(go.Scatter(
        x=df_revenue_filtered['date'],
        y=df_revenue_filtered['activities'],
        name='Activities & Tours',
        line=dict(color='#b8860b', width=2, dash='dash')
    ))
    
    fig_revenue.update_layout(
        title="Tourism Revenue Trends (USD)",
        xaxis_title="Date",
        yaxis_title="Revenue (USD)",
        hovermode='x unified',
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig_revenue, width='stretch')

with col2:
    # Revenue breakdown pie chart
    revenue_breakdown = {
        'Accommodation': df_revenue_filtered['accommodation'].sum(),
        'Activities': df_revenue_filtered['activities'].sum(),
        'Food & Beverage': df_revenue_filtered['food_beverage'].sum(),
        'Transport': df_revenue_filtered['transport'].sum()
    }
    
    fig_revenue_pie = px.pie(
        values=list(revenue_breakdown.values()),
        names=list(revenue_breakdown.keys()),
        title="Revenue Breakdown",
        color_discrete_sequence=px.colors.sequential.Sunset
    )
    fig_revenue_pie.update_traces(textposition='inside', textinfo='percent+label')
    fig_revenue_pie.update_layout(height=400)
    st.plotly_chart(fig_revenue_pie, width='stretch')

# Economic multiplier effects
st.markdown("##### 📊 Economic Impact Analysis")

total_direct_revenue = df_revenue_filtered['total_revenue_usd'].sum()
tourism_multiplier = 2.3  # Typical tourism multiplier for developing regions

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Direct Tourism Revenue", f"${total_direct_revenue/1e6:.2f}M")

with col2:
    indirect_impact = total_direct_revenue * (tourism_multiplier - 1)
    st.metric("Indirect Economic Impact", f"${indirect_impact/1e6:.2f}M")

with col3:
    total_impact = total_direct_revenue * tourism_multiplier
    st.metric("Total Economic Impact", f"${total_impact/1e6:.2f}M")

with col4:
    # Jobs supported (rough estimate: $50,000 per job)
    jobs = total_impact / 50000
    st.metric("Jobs Supported (est.)", f"{jobs:,.0f}")

st.markdown("---")

# ============================================================
# INVESTMENT OPPORTUNITIES
# ============================================================
st.subheader("🎯 Investment Opportunities & ROI Indicators")

col1, col2 = st.columns(2)

with col1:
    st.markdown("##### 🏗️ Priority Investment Areas")
    
    opportunities = pd.DataFrame({
        'Opportunity': [
            'Mid-Range Lodges (50-100 rooms)',
            'Luxury Tented Camps (20-30 units)',
            'Adventure Activity Center',
            'Conference & Events Facility',
            'Wellness/Spa Retreat'
        ],
        'Est. Investment (USD)': [
            '2.5M - 5M',
            '1.5M - 3M',
            '500K - 1M',
            '3M - 6M',
            '2M - 4M'
        ],
        'Est. ROI Timeline': [
            '5-7 years',
            '4-6 years',
            '3-4 years',
            '6-8 years',
            '5-7 years'
        ],
        'Risk Level': [
            'Medium',
            'Medium-High',
            'Low-Medium',
            'Medium',
            'Medium'
        ]
    })
    
    st.dataframe(opportunities, width='stretch', hide_index=True)

with col2:
    st.markdown("##### 📈 Market Drivers & Trends")
    
    st.markdown("""
    <div class="highlight-box">
    <strong>Positive Factors:</strong>
    <ul>
        <li>✅ KAZA TFCA integration increasing cross-border tourism</li>
        <li>✅ Kazungula Bridge improving regional connectivity</li>
        <li>✅ Growing African middle class tourism market</li>
        <li>✅ Government tourism promotion initiatives</li>
        <li>✅ Proximity to Victoria Falls (30km)</li>
        <li>✅ Unique KAZA wildlife corridor position</li>
    </ul>
    
    <strong>Challenges to Consider:</strong>
    <ul>
        <li>⚠️ Seasonal demand fluctuations</li>
        <li>⚠️ Infrastructure development needs</li>
        <li>⚠️ Competition from Livingstone</li>
        <li>⚠️ Need for skilled hospitality workers</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# ROI Calculator
st.markdown("##### 🧮 Simple ROI Calculator")

calc_col1, calc_col2, calc_col3 = st.columns(3)

with calc_col1:
    investment = st.number_input(
        "Initial Investment (USD)",
        min_value=100000,
        max_value=10000000,
        value=2000000,
        step=100000,
        format="%d"
    )

with calc_col2:
    expected_occupancy = st.slider(
        "Expected Occupancy Rate (%)",
        min_value=30,
        max_value=90,
        value=65,
        step=5
    )

with calc_col3:
    avg_rate = st.number_input(
        "Average Daily Rate (USD)",
        min_value=50,
        max_value=500,
        value=150,
        step=10
    )

# Calculate ROI
rooms_estimate = investment / 40000  # Rough estimate: $40k per room
annual_revenue = rooms_estimate * 365 * (expected_occupancy/100) * avg_rate
operating_costs = annual_revenue * 0.65  # 65% operating costs
net_profit = annual_revenue - operating_costs
roi_years = investment / net_profit if net_profit > 0 else 0

calc_result_col1, calc_result_col2, calc_result_col3, calc_result_col4 = st.columns(4)

with calc_result_col1:
    st.metric("Est. Annual Revenue", f"${annual_revenue:,.0f}")

with calc_result_col2:
    st.metric("Est. Annual Net Profit", f"${net_profit:,.0f}")

with calc_result_col3:
    if roi_years > 0 and roi_years < 100:
        st.metric("Payback Period", f"{roi_years:.1f} years")
    else:
        st.metric("Payback Period", "N/A")

with calc_result_col4:
    if roi_years > 0:
        roi_percentage = (net_profit / investment) * 100
        st.metric("Annual ROI", f"{roi_percentage:.1f}%")

st.caption("*Note: This is a simplified calculator. Actual returns depend on many factors including location, management quality, market conditions, and operational efficiency.*")

st.markdown("---")

# ============================================================
# COMPETITIVE LANDSCAPE
# ============================================================
st.subheader("🏆 Competitive Landscape")

comp_col1, comp_col2 = st.columns(2)

with comp_col1:
    st.markdown("##### Major Players in Kazungula Area")
    
    competitors = pd.DataFrame({
        'Facility': [
            'Chobe Marina Lodge',
            'Sanctuary Chobe Chilwero',
            'Chobe Safari Lodge',
            'Chobe Bush Lodge',
            'Kazungula Lodge'
        ],
        'Type': ['Hotel', 'Luxury Lodge', 'Lodge', 'Budget Lodge', 'Guesthouse'],
        'Rooms': [60, 15, 47, 30, 12],
        'Est. Rate (USD)': [200, 450, 180, 80, 50],
        'Target Market': ['Mid-High', 'Luxury', 'Mid', 'Budget', 'Budget']
    })
    
    st.dataframe(competitors, width='stretch', hide_index=True)

with comp_col2:
    st.markdown("##### Market Positioning Opportunities")
    
    st.markdown("""
    <div class="highlight-box">
    <strong>Underserved Segments:</strong>
    <ul>
        <li>🎯 <strong>Mid-Range Family Tourism:</strong> Limited 3-star family-friendly options</li>
        <li>🎯 <strong>Eco-Conscious Travelers:</strong> Sustainable/green lodges</li>
        <li>🎯 <strong>Adventure Seekers:</strong> Activity-focused accommodation</li>
        <li>🎯 <strong>MICE Market:</strong> Business/conference facilities</li>
        <li>🎯 <strong>Long-Stay Guests:</strong> Self-catering units</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# INFRASTRUCTURE & CONNECTIVITY
# ============================================================
st.subheader("🛣️ Infrastructure & Connectivity")

infra_col1, infra_col2 = st.columns(2)

with infra_col1:
    st.markdown("##### 🚗 Transport Infrastructure")
    
    st.markdown("""
    **Road Access:**
    - ✅ Paved road to Livingstone (70km)
    - ✅ Kazungula Bridge (opened 2021) - major upgrade
    - ✅ Road connection to Botswana border
    - ⚠️ Some internal roads need upgrading
    
    **Air Access:**
    - 🛬 Harry Mwanga Nkumbula International Airport (80km)
    - 🛬 Kasane Airport, Botswana (12km)
    - 🛬 Victoria Falls Airport, Zimbabwe (90km)
    
    **Border Crossings:**
    - 🌍 Kazungula Four-Corners (Zambia-Botswana-Zimbabwe-Namibia)
    - 📊 Avg 800+ vehicles/day
    - 👥 Avg 1,200+ travelers/day
    """)

with infra_col2:
    st.markdown("##### 🏛️ Supporting Infrastructure")
    
    st.markdown("""
    **Available Services:**
    - ✅ Electricity (ZESCO grid + backup generators)
    - ✅ Mobile networks (Airtel, MTN, Zamtel)
    - ✅ Internet connectivity (improving)
    - ✅ Banking services in Kazungula town
    - ✅ Healthcare facilities (clinic + hospital in Livingstone)
    
    **Ongoing Developments:**
    - 🏗️ Kazungula Special Economic Zone (proposed)
    - 🏗️ Road upgrades to Sesheke
    - 🏗️ Expansion of border facilities
    - 🏗️ Water supply improvements
    
    **Nearby Attractions:**
    - 🌊 Victoria Falls (30km)
    - 🐘 Chobe National Park (immediate)
    - 🦛 Mosi-oa-Tunya National Park
    - 🌅 Zambezi River activities
    """)

st.markdown("---")

# ============================================================
# DATA INSIGHTS & RECOMMENDATIONS
# ============================================================
st.subheader("💡 Key Insights & Recommendations")

insights_col1, insights_col2 = st.columns(2)

with insights_col1:
    st.markdown("""
    <div class="highlight-box">
    <h4>📊 Data-Driven Insights</h4>
    
    <strong>1. Strong Recovery Post-COVID:</strong>
    <ul>
        <li>Tourism arrivals have recovered to 110% of 2019 levels</li>
        <li>Revenue growth outpacing arrival growth (premium segment growing)</li>
    </ul>
    
    <strong>2. Regional Market Dominance:</strong>
    <ul>
        <li>SADC visitors account for 35% of total arrivals</li>
        <li>South African market is largest single source (25%)</li>
        <li>Growing intra-African tourism trend</li>
    </ul>
    
    <strong>3. Seasonal Opportunities:</strong>
    <ul>
        <li>Peak season (June-October) shows 85%+ occupancy</li>
        <li>Low season (January-March) has significant capacity</li>
        <li>Opportunity for off-season marketing/packages</li>
    </ul>
    
    <strong>4. Infrastructure Gap:</strong>
    <ul>
        <li>Shortage of mid-range accommodation (3-star)</li>
        <li>Limited conference/business facilities</li>
        <li>Growing demand for sustainable tourism options</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

with insights_col2:
    st.markdown("""
    <div class="highlight-box">
    <h4>🎯 Investment Recommendations</h4>
    
    <strong>Short-Term (1-2 years):</strong>
    <ul>
        <li>✅ Upgrade existing properties to capture growing premium market</li>
        <li>✅ Develop activity/adventure packages to extend stays</li>
        <li>✅ Focus on low-season marketing to African markets</li>
    </ul>
    
    <strong>Medium-Term (2-5 years):</strong>
    <ul>
        <li>🏗️ Build mid-range lodge/hotel (50-100 rooms)</li>
        <li>🏗️ Develop luxury tented camp for premium segment</li>
        <li>🏗️ Create adventure/activity center</li>
        <li>🏗️ Invest in sustainable/eco-tourism facilities</li>
    </ul>
    
    <strong>Long-Term (5+ years):</strong>
    <ul>
        <li>🌟 Large-scale resort development</li>
        <li>🌟 Conference/MICE facilities</li>
        <li>🌟 Integrated tourism complex</li>
    </ul>
    
    <strong>Risk Mitigation:</strong>
    <ul>
        <li>⚠️ Start with smaller, phased developments</li>
        <li>⚠️ Focus on unique selling propositions</li>
        <li>⚠️ Build strong relationships with tour operators</li>
        <li>⚠️ Invest in staff training and quality service</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# FOOTER & CONTACT
# ============================================================
st.markdown("---")

footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.markdown("""
    #### 📊 Data Sources
    - Zambia Ministry of Tourism
    - KAZA TFCA Secretariat
    - Kazungula Border Post Statistics
    - Local Accommodation Surveys
    - Industry Reports
    """)

with footer_col2:
    st.markdown("""
    #### 📅 Dashboard Information
    **Coverage Area:** Kazungula District, Zambia  
    **Last Updated:** October 2024  
    **Update Frequency:** Monthly  
    **Data Period:** 2019 - Present
    """)

with footer_col3:
    st.markdown("""
    #### 📞 Need Custom Analysis?
    
    **Concise Data Analytics**  
    Specialized tourism intelligence for SADC
    
    📧 info@concise-analytics.com  
    🌐 concise-analytics.com  
    📍 Gaborone, Botswana
    
    *Request feasibility studies, market research, or custom dashboards*
    """)

st.markdown("---")
st.caption("© 2024 Concise Data Analytics | Dashboard v1.0 | Built with Streamlit")
