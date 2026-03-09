import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ---------------- PAGE CONFIGURATION ----------------
st.set_page_config(
    page_title="PyroVision AI | Fire Detection Dashboard",
    page_icon="🔥",
    layout="wide"
)

# ---------------- CUSTOM LIGHT THEME STYLING ----------------
st.markdown(
    """
    <style>
    .main { background-color: #f8fafc; }
    h1, h2, h3 { color: #1e293b; font-family: 'Segoe UI', sans-serif; font-weight: 700; }
    [data-testid="stMetric"] {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 15px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    [data-testid="stSidebar"] { background-color: #1e293b; }
    .stAlert { background-color: #fee2e2; color: #991b1b; border: 1px solid #f87171; }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("<h2 style='color: white;'>🎛️ Detection Control</h2>", unsafe_allow_html=True)
    st.write(f"**System Time:** {datetime.now().strftime('%H:%M:%S')}")
    mode = st.radio("Detection Mode:", ["🟢 Normal Scanning", "🚨 Fire Detected"], index=0)
    st.divider()
    st.info("📍 Monitoring Area: Ismailia, Egypt")

# ---------------- HEADER ----------------
st.title("🧠 PyroVision AI: Intelligent Fire Detection Dashboard")

# ---------------- TOP METRICS ----------------
m1, m2, m3, m4 = st.columns(4)
m1.metric("🔥 Temperature", f"{np.random.randint(25, 85)} °C")
m2.metric("💨 Smoke Levels", f"{np.random.randint(5, 95)} %")
m3.metric("⚡ Sensor Nodes Active", "142", "+4")
if mode == "🚨 Fire Detected":
    m4.metric("🚩 Fire Risk Status", "CRITICAL", "High Alert!", delta_color="inverse")
else:
    m4.metric("🚩 Fire Risk Status", "NORMAL", "Stable", delta_color="normal")

st.divider()

# ---------------- MAP AND SENSOR DATA ----------------
col1, col2 = st.columns([1.5, 1])

with col1:
    st.subheader("🗺️ Real-Time Geospatial Detection Map")

    # Sample location data for visualization
    data = {
        'lat': [30.621, 30.597, 30.622],
        'lon': [32.289, 32.275, 32.268],
        'location': ['Sheikh Zayed', 'Nemra 6', 'University Area'],
        'temperature': np.random.randint(25, 100, 3),
        'smoke': np.random.randint(5, 95, 3)
    }
    df_map = pd.DataFrame(data)

    df_map['Risk'] = ['🔥 High' if (t > 70 or s > 70) else '🟢 Low' for t, s in zip(df_map['temperature'], df_map['smoke'])]

    fig_map = px.scatter_mapbox(
        df_map,
        lat='lat', lon='lon', color='Risk',
        hover_name='location',
        size='temperature',
        color_discrete_map={'🟢 Low': '#22c55e', '🔥 High': '#ef4444'},
        zoom=13, mapbox_style="carto-positron"
    )
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig_map, use_container_width=True)

with col2:
    st.subheader("📈 Live Sensor Trends")

    # Simulated sensor data over time
    chart_data = pd.DataFrame({
        'Time': list(range(10)),
        'Temperature (°C)': np.random.randint(25, 100, 10),
        'Smoke (%)': np.random.randint(5, 95, 10)
    })

    fig_trend = px.line(
        chart_data, x='Time', y=['Temperature (°C)', 'Smoke (%)'],
        color_discrete_sequence=['#ef4444', '#64748b'],
        template='plotly_white'
    )
    fig_trend.update_layout(height=350, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_trend, use_container_width=True)

st.divider()

# ---------------- AI ANALYSIS SECTION ----------------
st.subheader("🤖 AI Risk Analysis")
current_temperature = chart_data['Temperature (°C)'].iloc[-1]
current_smoke = chart_data['Smoke (%)'].iloc[-1]
risk_score = (current_temperature * 0.6 + current_smoke * 0.4) / 1.5

colA, colB, colC = st.columns(3)
colA.metric("Current Temperature", f"{current_temperature} °C")
colB.metric("Current Smoke Level", f"{current_smoke} %")
colC.metric("Computed Fire Risk Index", f"{risk_score:.2f}")

if risk_score > 70:
    st.error("🔥 High Fire Probability detected – Immediate attention advised.")
elif risk_score > 40:
    st.warning("⚠️ Moderate fire risk developing.")
else:
    st.success("✅ Area stable, no fire indications detected.")

st.divider()

# ---------------- ANALYTICS ----------------
st.subheader("📊 Detection Data Overview")
col1, col2 = st.columns(2)

with col1:
    st.caption("🔥 Temperature & Smoke Average")
    avg_data = pd.DataFrame({
        'Metric': ['Temperature', 'Smoke Levels'],
        'Average': [chart_data['Temperature (°C)'].mean(), chart_data['Smoke (%)'].mean()]
    })
    fig_bar = px.bar(avg_data, x='Metric', y='Average', color='Metric',
                     color_discrete_sequence=['#ef4444', '#818cf8'], template='plotly_white')
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    st.caption("🔥 Temperature Distribution")
    fig_hist = px.histogram(chart_data, x='Temperature (°C)', nbins=10, color_discrete_sequence=['#f97316'], template='plotly_white')
    st.plotly_chart(fig_hist, use_container_width=True)

st.divider()

# ---------------- FOOTER ----------------
st.markdown(
    "<center style='color: #64748b;'>Developed by <b>Ahmed, Eyad, Habiba, Jana, Rodina</b> | WE School Ismailia ©️ 2026</center>",
    unsafe_allow_html=True
)
