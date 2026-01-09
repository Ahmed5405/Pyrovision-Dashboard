import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import requests

# --- Telegram Notification Function ---
def send_telegram_alert(message):
    token = "8525068051:AAHheDTQ-PIXEWvvIIcokuKF3pwyHr0gPwE"
    chat_id = "1655340743" 
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
    try:
        requests.get(url, timeout=5)
    except Exception:
        pass

# 1. Page Configuration
st.set_page_config(
    page_title="PyroVision AI | Command Center",
    page_icon="🦅",
    layout="wide"
)

# 2. Professional CSS (Cyberpunk & Clean UI)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    h1, h2, h3 { color: #e6e6e6; font-family: 'Segoe UI', sans-serif; }
    .stMetric { background-color: #1f2937; border-radius: 10px; padding: 15px; border: 1px solid #374151; }
    .stAlert { background-color: #7f1d1d; color: white; }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar
with st.sidebar:
    st.title("🎛️ Neural Control")
    st.write(f"**System Time:** {datetime.now().strftime('%H:%M:%S')}")
    mode = st.radio("Operation Mode:", ["🟢 ACTIVE SCANNING", "🚨 EMERGENCY DETECTED"])
    st.divider()
    enable_tg = st.toggle("Telegram Alerts", value=True)
    st.info("📍 Location: Ismailia, Egypt")

# 4. Main Dashboard Header
st.title("🛡️ PyroVision AI: Advanced Fire Defense System")

# 5. Top KPIs (Key Performance Indicators)
k1, k2, k3, k4 = st.columns(4)
k1.metric("Active Sensors", "142 Nodes", "+5 New")
k2.metric("System Latency", "24ms", "-12ms")
k3.metric("Wind Speed", "14 km/h", "North-East")
if mode == "🚨 EMERGENCY DETECTED":
    k4.metric("Threat Level", "CRITICAL", "High Risk", delta_color="inverse")
else:
    k4.metric("Threat Level", "STABLE", "Safe", delta_color="normal")

st.divider()

# 6. Advanced Map & Live Trends
col_map, col_trend = st.columns([1.5, 1])

with col_map:
    st.subheader("🗺️ Geospatial Live Tracking")
    
    # Coordinates for Ismailia Locations
    data = {
        'lat': [30.621, 30.597, 30.622],
        'lon': [32.289, 32.275, 32.268],
        'location': ['Sheikh Zayed', 'Nemra 6', 'University Area'],
        'status': ['Safe', 'Safe', 'Safe']
    }
    
    # Emergency Logic
    if mode == "🚨 EMERGENCY DETECTED":
        data['status'][0] = 'CRITICAL FIRE'
        # Telegram Alert
        if enable_tg:
            send_telegram_alert("🚨 URGENT: Fire detected in Sheikh Zayed District! Immediate action required.")
            st.toast("Alert Sent to Telegram Command!", icon="🚀")
    
    df_map = pd.DataFrame(data)
    
    # Professional Map (Fixes Arabic text issues by using English labels or Clean Dots)
    fig_map = px.scatter_mapbox(
        df_map, 
        lat="lat", lon="lon", 
        color="status",
        size=[20, 15, 15],
        color_discrete_map={'Safe': '#00ff00', 'CRITICAL FIRE': '#ff0000'},
        zoom=13,
        hover_name="location",
        mapbox_style="carto-darkmatter"  # This is the "Cool Dark Mode" map
    )
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor="#0e1117")
    st.plotly_chart(fig_map, use_container_width=True)

with col_trend:
    st.subheader("📈 Live Sensor Fusion")
    # Generating fake data for the chart
    chart_data = pd.DataFrame({
        'Time': list(range(10)),
        'Temperature (°C)': np.random.randint(20, 35, 10) if mode == "🟢 ACTIVE SCANNING" else [30,35,40,55,70,85,95,100,110,120],
        'Smoke Levels (%)': np.random.randint(0, 5, 10) if mode == "🟢 ACTIVE SCANNING" else [5,10,25,40,60,75,80,90,95,99]
    })
    
    fig_trend = px.area(
        chart_data, x='Time', y=['Temperature (°C)', 'Smoke Levels (%)'],
        color_discrete_sequence=['#ff4b4b', '#808080'],
        template="plotly_dark"
    )
    fig_trend.update_layout(height=350, bg_color='rgba(0,0,0,0)')
    st.plotly_chart(fig_trend, use_container_width=True)

st.divider()

# 7. The NEW "Exciting" Dashboard Section (Donut Charts & Bars)
st.subheader("📊 Analytics & System Health (Annual Report)")

col1, col2, col3 = st.columns(3)

with col1:
    # Chart 1: Donut Chart for Sensor Status
    st.caption("📡 Sensor Network Status")
    labels = ['Online', 'Maintenance', 'Offline']
    values = [120, 15, 7]
    fig_pie = px.pie(values=values, names=labels, hole=0.6, 
                     color_discrete_sequence=['#00cc96', '#fabc09', '#ef553b'],
                     template="plotly_dark")
    fig_pie.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0), height=200)
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    # Chart 2: Bar Chart for Fire Causes
    st.caption("🔥 Fire Incidents by Cause (2025)")
    causes_df = pd.DataFrame({
        'Cause': ['Electrical', 'Gas Leak', 'Human Error', 'Nature'],
        'Incidents': [45, 30, 80, 10]
    })
    fig_bar = px.bar(causes_df, x='Cause', y='Incidents', 
                     color='Incidents', color_continuous_scale='Magma',
                     template="plotly_dark")
    fig_bar.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=200)
    st.plotly_chart(fig_bar, use_container_width=True)

with col3:
    # Chart 3: Gauge Chart (Battery Health)
    st.caption("🔋 Main Battery Backup Health")
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = 88,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Charge %"},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': "#00ffcc"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 50], 'color': '#ff4b4b'},
                {'range': [50, 100], 'color': '#1f2937'}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90}}))
    fig_gauge.update_layout(paper_bgcolor = "rgba(0,0,0,0)", font = {'color': "white", 'family': "Arial"}, height=200, margin=dict(t=30, b=0, l=20, r=20))
    st.plotly_chart(fig_gauge, use_container_width=True)

st.divider()
st.markdown("<center>Developed by <b>Ahmed & The Team</b> | WE School Ismailia © 2026</center>", unsafe_allow_html=True)
