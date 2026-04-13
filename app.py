import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- Page Configuration ---
st.set_page_config(page_title="RFM Analytics", page_icon="📈", layout="wide", initial_sidebar_state="expanded")

# --- Load Data ---
@st.cache_data
def load_data():
    file_path = "data/rfm_data.csv"
    if not os.path.exists(file_path):
        return None
    return pd.read_csv(file_path)

df = load_data()

if df is None:
    st.error("Data not found. Please run `rfm_engine.py` first to generate the data.")
    st.stop()

# --- Theme Engine ---
# value=False ensures the toggle defaults to Light Mode
dark_mode = st.sidebar.toggle("🌙 Enable Dark Theme", value=False)

# Dynamic Theme Variables
if dark_mode:
    bg_color = "#121212"         
    card_bg = "#1e1e1e"          
    text_color = "#e0e0e0"       
    grid_color = "#333333"       
    PRIMARY_COLOR = "#00E5FF"    # Neon Cyan
    TAG_TEXT_COLOR = "#121212"   
    TOGGLE_BG = "#00E5FF"        # Toggle is Neon Cyan when ON
    PALETTE = ["#00E5FF", "#18FFFF", "#84FFFF", "#00B8D4", "#006064"]
    plot_template = "plotly_dark"
else:
    bg_color = "#f4f7f6"         
    card_bg = "#ffffff"          
    text_color = "#2b2b2b"       
    grid_color = "#e9ecef"       
    PRIMARY_COLOR = "#2f5972"    # Azure
    TAG_TEXT_COLOR = "#ffffff"   
    TOGGLE_BG = "#121212"        # 🔴 Toggle is solid Black when OFF
    PALETTE = ["#2f5972", "#457b9d", "#6a9ebf", "#98c1d9", "#e0fbfc"]
    plot_template = "plotly_white"

# Render Sidebar Header dynamically
st.sidebar.markdown(f"<h2 style='color: {PRIMARY_COLOR}; font-weight: 700;'>⚙️ Controls</h2>", unsafe_allow_html=True)

# --- Inject Master CSS ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    /* Global Font and Main Background */
    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif !important;
    }}
    [data-testid="stAppViewContainer"] {{
        background-color: {bg_color};
        color: {text_color};
    }}

    /* Sidebar Background */
    [data-testid="stSidebar"] {{
        background-color: {card_bg} !important;
        border-right: 1px solid {grid_color};
    }}
    
    /* FIX 1: Force all sidebar text to use our dynamic text_color */
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] label p,
    section[data-testid="stSidebar"] span {{
        color: {text_color} !important;
    }}

    /* FIX 2: Hijack the Multiselect Dropdown container */
    div[data-baseweb="select"] > div {{
        background-color: {card_bg} !important;
        border: 1px solid {grid_color} !important;
    }}

    /* FIX 3: Hijack the Multiselect Tags */
    span[data-baseweb="tag"] {{
        background-color: {PRIMARY_COLOR} !important;
        border: none !important;
    }}
    span[data-baseweb="tag"] span {{
        color: {TAG_TEXT_COLOR} !important; 
        font-weight: 600 !important;
    }}
    span[data-baseweb="tag"] svg {{
        fill: {TAG_TEXT_COLOR} !important;
    }}

    /* FIX 4: Hijack the Multiselect Popover Menu */
    div[data-baseweb="popover"] > div {{
        background-color: {card_bg} !important;
        border: 1px solid {grid_color} !important;
    }}
    ul[role="listbox"] li {{
        background-color: {card_bg} !important;
        color: {text_color} !important;
    }}
    ul[role="listbox"] li:hover {{
        background-color: {PRIMARY_COLOR} !important;
        color: {TAG_TEXT_COLOR} !important;
    }}

    /* 🔴 FIX 5: High-Contrast Toggle Button */
    div[data-testid="stToggle"] div[data-baseweb="checkbox"] > div:first-of-type {{
        background-color: {TOGGLE_BG} !important;
    }}

    /* Headers */
    h1, h2, h3 {{
        color: {PRIMARY_COLOR} !important;
        font-weight: 700 !important;
    }}

    /* KPI Cards */
    .metric-card {{
        background-color: {card_bg};
        border: 1px solid {grid_color};
        border-top: 4px solid {PRIMARY_COLOR}; 
        border-radius: 8px;
        padding: 24px 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        text-align: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    .metric-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
    }}
    .metric-value {{
        font-size: 2.4rem;
        font-weight: 700;
        margin: 12px 0;
        color: {PRIMARY_COLOR};
    }}
    .metric-label {{
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        color: {text_color};
        font-weight: 600;
        opacity: 0.8;
    }}
    </style>
""", unsafe_allow_html=True)

# --- Sidebar Filters ---
st.sidebar.divider()
selected_segments = st.sidebar.multiselect(
    "Filter by Customer Segment:",
    options=df['Customer_Profile'].unique(),
    default=df['Customer_Profile'].unique()
)

filtered_df = df[df['Customer_Profile'].isin(selected_segments)]

# --- Main Layout ---
st.title("Customer Segmentation Overview")
st.markdown(f"<p style='color: {text_color}; opacity: 0.8; font-size: 1.1rem;'>Analyzing <b>{len(filtered_df):,}</b> active customers via Recency, Frequency, and Monetary scoring.</p>", unsafe_allow_html=True)

# --- KPI Row ---
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

total_rev = filtered_df['Monetary'].sum()
avg_orders = filtered_df['Frequency'].mean()
avg_recency = filtered_df['Recency'].mean()

col1.markdown(f'<div class="metric-card"><div class="metric-label">Total Customers</div><div class="metric-value">{len(filtered_df):,}</div></div>', unsafe_allow_html=True)
col2.markdown(f'<div class="metric-card"><div class="metric-label">Gross Revenue</div><div class="metric-value">${total_rev:,.0f}</div></div>', unsafe_allow_html=True)
col3.markdown(f'<div class="metric-card"><div class="metric-label">Avg Orders / User</div><div class="metric-value">{avg_orders:.1f}</div></div>', unsafe_allow_html=True)
col4.markdown(f'<div class="metric-card"><div class="metric-label">Avg Recency (Days)</div><div class="metric-value">{avg_recency:.0f}</div></div>', unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# --- Chart Configuration Helper ---
def apply_chart_styling(fig):
    fig.update_layout(
        template=plot_template,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter", color=text_color),
        title_font=dict(size=18, color=PRIMARY_COLOR, family="Inter", weight="bold"),
        margin=dict(t=50, l=20, r=20, b=20)
    )
    fig.update_xaxes(showgrid=True, gridcolor=grid_color, gridwidth=1, zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor=grid_color, gridwidth=1, zeroline=False)
    return fig

# --- Dashboard Tabs ---
tab1, tab2 = st.tabs(["📊 Executive Dashboard", "📋 Raw Data"])

with tab1:
    r1c1, r1c2 = st.columns([1.2, 1])
    
    with r1c1:
        fig_tree = px.treemap(
            filtered_df, 
            path=[px.Constant("All Segments"), 'Customer_Profile'],
            values='Monetary',
            color='Monetary',
            color_continuous_scale="Blues" if not dark_mode else "Teal",
            title="Revenue Proportion by Segment"
        )
        fig_tree = apply_chart_styling(fig_tree)
        fig_tree.update_traces(marker=dict(line=dict(color=card_bg, width=2))) 
        st.plotly_chart(fig_tree, use_container_width=True)

    with r1c2:
        fig_scatter = px.scatter(
            filtered_df, 
            x='Recency', 
            y='Monetary', 
            color='Customer_Profile',
            size='Frequency',
            color_discrete_sequence=PALETTE,
            title="Customer Value vs. Recency"
        )
        fig_scatter = apply_chart_styling(fig_scatter)
        fig_scatter.update_xaxes(autorange="reversed", title="Days Since Last Purchase")
        fig_scatter.update_yaxes(title="Total Spent ($)")
        fig_scatter.update_layout(legend_title_text='')
        st.plotly_chart(fig_scatter, use_container_width=True)

    r2c1, r2c2 = st.columns(2)

    with r2c1:
        segment_counts = filtered_df['Customer_Profile'].value_counts().reset_index()
        segment_counts.columns = ['Segment', 'Count']
        
        fig_bar = px.bar(
            segment_counts, 
            x='Segment', 
            y='Count', 
            color='Segment',
            color_discrete_sequence=PALETTE,
            title="Population Count per Segment"
        )
        fig_bar = apply_chart_styling(fig_bar)
        fig_bar.update_layout(showlegend=False, xaxis_title="", yaxis_title="Number of Customers")
        st.plotly_chart(fig_bar, use_container_width=True)

    with r2c2:
        fig_hist = px.histogram(
            filtered_df, 
            x='Monetary', 
            nbins=30,
            color_discrete_sequence=[PRIMARY_COLOR],
            title="Distribution of Customer Spend"
        )
        fig_hist = apply_chart_styling(fig_hist)
        fig_hist.update_layout(xaxis_title="Total Spent ($)", yaxis_title="Count of Customers")
        st.plotly_chart(fig_hist, use_container_width=True)

with tab2:
    st.markdown(f"<h3 style='color: {PRIMARY_COLOR};'>Dataset Explorer</h3>", unsafe_allow_html=True)
    st.dataframe(filtered_df[['CustomerID', 'Recency', 'Frequency', 'Monetary', 'RFM_Score', 'Customer_Profile']], use_container_width=True)