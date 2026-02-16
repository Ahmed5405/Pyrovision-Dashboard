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
    page_icon="🛡️",
    layout="wide"
)

# 2. Professional & Eye-Friendly UI (Light/Soft Mode)
# تم تعديل الألوان هنا لتكون خلفية رمادية فاتحة مريحة وعناوين واضحة
st.markdown("""
    <style>
    /* خلفية الصفحة الرئيسية */
    .main { background-color: #f8fafc; }
    
    /* لون العناوين الرئيسية */
    h1, h2, h3 { color: #1e293b; font-family: 'Segoe UI', sans-serif; font-weight: 700; }
    
    /* تنسيق صناديق الأرقام (Metrics) لتكون بيضاء بظلال خفيفة */
    [data-testid="stMetric"] {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 15px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    
    /* شريط القائمة الجانبية باللون الكحلي الاحترافي */
    [data-testid="stSidebar"] {
        background-color: #1e293b;
    }
    
    /* تنبيهات الطوارئ */
    .stAlert { background-color: #fee2e2; color: #991b1b; border: 1px solid #f87171; }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar
with st.sidebar:
    st.markdown("<h2 style='color: white;'>🎛️ Neural Control</h2>", unsafe_allow_html=True)
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
    
    if mode == "🚨 EMERGENCY DETECTED":
        data['status'][0] = 'CRITICAL FIRE'
        if enable_tg:
            send_telegram_alert("🚨 URGENT: Fire detected in Sheikh Zayed District! Immediate action required.")
            st.toast("Alert Sent to Telegram Command!", icon="🚀")
    
    df_map = pd.DataFrame(data)
    
    # تم تعديل الخريطة لتكون فاتحة لتناسب التصميم المريح للعين
    fig_map = px.scatter_mapbox(
        df_map, 
        lat="lat", lon="lon", 
        color="status",
        size=[20, 15, 15],
        color_discrete_map={'Safe': '#22c55e', 'CRITICAL FIRE': '#ef4444'},
        zoom=13,
        hover_name="location",
        mapbox_style="carto-positron"  # خريطة فاتحة وواضحة جداً
    )
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig_map, use_container_width=True)

with col_trend:
    st.subheader("📈 Live Sensor Fusion")
    chart_data = pd.DataFrame({
        'Time': list(range(10)),
        'Temperature (°C)': np.random.randint(20, 35, 10) if mode == "🟢 ACTIVE SCANNING" else [30,35,40,55,70,85,95,100,110,120],
        'Smoke Levels (%)': np.random.randint(0, 5, 10) if mode == "🟢 ACTIVE SCANNING" else [5,10,25,40,60,75,80,90,95,99]
    })
    
    # تم تغيير السمة إلى الرسم الفاتح
    fig_trend = px.area(
        chart_data, x='Time', y=['Temperature (°C)', 'Smoke Levels (%)'],
        color_discrete_sequence=['#ef4444', '#64748b'],
        template="plotly_white"
    )
    fig_trend.update_layout(height=350, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_trend, use_container_width=True)

st.divider()

# 7. Analytics Section (Donut, Bar, Gauge)
st.subheader("📊 Analytics & System Health (Annual Report)")

col1, col2, col3 = st.columns(3)

with col1:
    st.caption("📡 Sensor Network Status")
    labels = ['Online', 'Maintenance', 'Offline']
    values = [120, 15, 7]
    fig_pie = px.pie(values=values, names=labels, hole=0.6, 
                     color_discrete_sequence=['#10b981', '#f59e0b', '#ef4444'],
                     template="plotly_white")
    fig_pie.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0), height=200)
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    st.caption("🔥 Fire Incidents by Cause (2025)")
    causes_df = pd.DataFrame({
        'Cause': ['Electrical', 'Gas Leak', 'Human Error', 'Nature'],
        'Incidents': [45, 30, 80, 10]
    })
    fig_bar = px.bar(causes_df, x='Cause', y='Incidents', 
                     color='Incidents', color_continuous_scale='Reds',
                     template="plotly_white")
    fig_bar.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=200)
    st.plotly_chart(fig_bar, use_container_width=True)

with col3:
    st.caption("🔋 Main Battery Backup Health")
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = 88,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Charge %", 'font': {'size': 14}},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#1e293b"},
            'bar': {'color': "#3b82f6"},
            'bgcolor': "white",
            'borderwidth': 1,
            'bordercolor': "#e2e8f0",
            'steps': [
                {'range': [0, 30], 'color': '#fee2e2'},
                {'range': [30, 100], 'color': '#f1f5f9'}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90}}))
    fig_gauge.update_layout(paper_bgcolor = "rgba(0,0,0,0)", font = {'color': "#1e293b", 'family': "Segoe UI"}, height=200, margin=dict(t=30, b=0, l=20, r=20))
    st.plotly_chart(fig_gauge, use_container_width=True)

st.divider()
st.markdown("<center style='color: #64748b;'>Developed by <b>Ahmed & The Team</b> | WE School Ismailia ©️ 2026</center>", unsafe_allow_html=True)
