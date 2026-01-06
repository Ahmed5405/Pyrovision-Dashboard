import streamlit as st
import pandas as pd
import numpy as np
import time

# 1. Page Configuration
st.set_page_config(
    page_title="PyroVision 360 | Ismailia AI Command",
    page_icon="🔥",
    layout="wide"
)

# Custom Styling
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Ismailia Geographical Data
ismailia_locations = {
    "Sector 1": "Nemra 6 - Canal Region",
    "Sector 2": "Sheikh Zayed District",
    "Sector 3": "Ard El Gamyat",
    "Sector 4": "Suez Canal University Campus",
    "Sector 5": "El Forsan Area"
}

# 3. Sidebar Navigation
st.sidebar.title("🎮 Control Center")
st.sidebar.subheader("System Configuration")
mode = st.sidebar.radio("Operation Mode:", ["🟢 NORMAL OPERATION", "🔴 FIRE EMERGENCY"])

st.sidebar.divider()
st.sidebar.info("""
**System Info:**
- **Location:** Ismailia, Egypt
- **AI Model:** Pyro-Neural v4.2
- **Hardware:** Active (360° Cam)
""")

# 4. AI Processing Logic
if mode == "🟢 NORMAL OPERATION":
    status_label = "SECURE"
    ai_confidence = np.random.uniform(0.01, 0.50)
    temperature = np.random.uniform(22.0, 26.5)
    selected_zone = "All Sectors Clear"
    image_url = "https://images.unsplash.com/photo-1590247813693-5541d1c609fd?w=800"
    log_color = "green"
else:
    status_label = "CRITICAL"
    ai_confidence = np.random.uniform(99.20, 99.99)
    temperature = np.random.uniform(88.5, 130.0)
    # Randomly pick a danger zone in Ismailia
    zone_id = np.random.choice(list(ismailia_locations.keys()))
    selected_zone = ismailia_locations[zone_id]
    image_url = "https://images.unsplash.com/photo-1505244781280-94a338600fdd?w=800"
    log_color = "red"
    st.error(f"🚨 AI ALERT: Fire Detected in {selected_zone}!")

# 5. Header Section
st.title("🔥 PyroVision 360 - AI Detection Dashboard")
st.write("Developed by: **WE Ismailia Team** | Smart Safety Solutions")
st.divider()

# 6. Real-time Metrics
m1, m2, m3, m4 = st.columns(4)
m1.metric("System Status", status_label, delta=None if mode=="🟢 NORMAL OPERATION" else "- DANGER")
m2.metric("AI Confidence", f"{ai_confidence:.2f}%")
m3.metric("Avg. Temperature", f"{temperature:.1f} °C", delta=f"{temperature-24:.1f} °C")
m4.metric("Response Latency", "0.78s", delta="-0.02s")

# 7. Main Visuals
st.divider()
left_col, right_col = st.columns([2, 1])

with left_col:
    st.subheader("📹 AI Neural Network Live Feed")
    st.image(image_url, caption="Real-time Visual Analysis", use_container_width=True)
    
    if mode == "🔴 FIRE EMERGENCY":
        st.warning(f"📍 INCIDENT LOCATION: {selected_zone}")
        # Generating realistic coordinates for Ismailia
        lat = 30.60 + np.random.uniform(0.01, 0.05)
        lon = 32.27 + np.random.uniform(0.01, 0.05)
        st.code(f"GPS COORDS: {lat:.5f} N, {lon:.5f} E | PRIORITY: LEVEL 1", language="bash")

with right_col:
    st.subheader("📊 Thermal Analytics")
    # Dynamic graph
    chart_data = pd.DataFrame(
        np.random.randn(20, 1) + temperature, 
        columns=['Heat Trend']
    )
    st.area_chart(chart_data, color="#ff4b4b" if mode=="🔴 FIRE EMERGENCY" else "#29b09d")
    
    st.write("📝 **System Logs:**")
    with st.container(border=True):
        if mode == "🟢 NORMAL OPERATION":
            st.write("✔️ 21:00:01 - Scanning Pixels...")
            st.write("✔️ 21:00:05 - Visual Signatures: Stable")
            st.write("✔️ 21:00:10 - No Threats Found.")
        else:
            st.write("⚠️ 21:05:12 - Flame Signature Found!")
            st.write(f"⚠️ 21:05:13 - Validating: {ai_confidence:.2f}% Match")
            st.write(f"🚨 21:05:15 - Alerts Sent to {selected_zone}")

st.divider()
st.caption("© 2026 PyroVision 360 | WE Applied Technology School - Ismailia")
