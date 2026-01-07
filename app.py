import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import requests
from sklearn.linear_model import LogisticRegression
import seaborn as sns
import matplotlib.pyplot as plt

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
    page_title="PyroVision AI | Neural Command Suite",
    page_icon="🛡️",
    layout="wide"
)

# 2. Professional CSS Styling (Dark Mode)
st.markdown("""
<style>
.main { background-color: #0d1117; color: #e1e1e1; }
.stMetric {
    border: 1px solid #30363d;
    padding: 20px;
    border-radius: 15px;
    background: linear-gradient(145deg, #161b22, #0d1117);
}
.fire-text {
    color: #ff4b4b;
    font-weight: bold;
    text-shadow: 0 0 10px #ff4b4b;
    animation: blinker 1.5s linear infinite;
}
@keyframes blinker { 50% { opacity: 0.3; } }
</style>
""", unsafe_allow_html=True)

# 3. Sidebar Neural Control
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2500/2500191.png", width=80)
    st.title("Neural Center v2.1")
    st.write("🛰️ **Satellite Status:** Active")
    mode = st.radio("Detection Protocol:", ["🟢 SCANNING MODE", "🚨 FIRE EMERGENCY"])
    st.divider()
    enable_tg = st.toggle("Enable Telegram Gateway", value=True)
    st.info("Linked to: @Pyrovision_Alter_Bot")
    st.caption("Deployment: WE School - Ismailia")

# 4. Header Section
st.markdown(f"## 🛡️ PyroVision 360: AI Multi-Sensor Hub")
st.write(f"**Current System Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (GMT+2)")

# 5. Dashboard Metrics
m1, m2, m3, m4 = st.columns(4)

if mode == "🚨 FIRE EMERGENCY":
    risk_val, conf_val, color_delta = "98%", "99.4%", "inverse"
    status_msg = "CRITICAL"
else:
    risk_val, conf_val, color_delta = "12%", "84.5%", "normal"
    status_msg = "SECURE"

m1.metric("Risk Level", risk_val, delta="+40%" if mode == "🚨 FIRE EMERGENCY" else "-2%", delta_color=color_delta)
m2.metric("AI Confidence", conf_val)
m3.metric("System Integrity", status_msg)
m4.metric("Neural Latency", "0.42ms")

st.divider()

# 6. Main Content: Map and Charts
col_left, col_right = st.columns([1.3, 1])

with col_left:
    st.subheader("🌐 Geospatial AI Analysis (Ismailia)")
    ismailia_zones = {
        "Sheikh Zayed": [30.621, 32.289],
        "Nemra 6": [30.597, 32.275],
        "University": [30.622, 32.268]
    }

    if mode == "🚨 FIRE EMERGENCY":
        target = "Sheikh Zayed District"
        st.markdown(f"### ⚠️ <span class='fire-text'>INCIDENT DETECTED: {target}</span>", unsafe_allow_html=True)

        if enable_tg:
            alert_text = f"🚨 PYROVISION ALERT:\nFire detected in {target}!\nTime: {datetime.now().strftime('%H:%M:%S')}"
            send_telegram_alert(alert_text)
            st.toast("Emergency alert sent to Telegram!", icon="📲")

        df_map = pd.DataFrame([ismailia_zones["Sheikh Zayed"]], columns=['lat', 'lon'])
        st.map(df_map, zoom=15, color='#ff4b4b')
    else:
        st.success("✅ SYSTEM STATUS: All Sectors in Ismailia are Clear")
        df_all = pd.DataFrame(ismailia_zones.values(), columns=['lat', 'lon'])
        st.map(df_all, zoom=12)

with col_right:
    st.subheader("📊 Sensor Fusion Stream")

    # Simulated realistic data
    base_temp = 25 if mode == "🟢 SCANNING MODE" else 80
    heat_values = np.cumsum(np.random.normal(0.3 if mode == "🚨 FIRE EMERGENCY" else 0.05, 0.2, 10)) + base_temp
    smoke_values = np.cumsum(np.random.normal(0.4 if mode == "🚨 FIRE EMERGENCY" else 0.05, 0.15, 10)) + (5 if mode == "🟢 SCANNING MODE" else 60)

    chart_data = pd.DataFrame({
        'Time': pd.date_range(datetime.now(), periods=10, freq='S'),
        'Heat Index (°C)': heat_values,
        'Smoke Density (%)': smoke_values
    })

    # Plotly chart
    fig = px.line(chart_data, x='Time', y=['Heat Index (°C)', 'Smoke Density (%)'],
                  template="plotly_dark", color_discrete_sequence=['#00ffcc', '#ff4b4b'])
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

    # 🔍 Seaborn Heat Map
    st.subheader("Seaborn Heat Map")
    fig2, ax = plt.subplots()
    sns.heatmap(chart_data[['Heat Index (°C)', 'Smoke Density (%)']], cmap="coolwarm", annot=True, ax=ax)
    st.pyplot(fig2)

    # 💾 Save data to CSV
    if st.button("💾 Save Sensor Data"):
        chart_data.to_csv('sensor_log.csv', index=False)
        st.success("Data saved to sensor_log.csv")

    # 🤖 Simple AI Prediction
    X = chart_data[['Heat Index (°C)', 'Smoke Density (%)']]
    y = np.where(chart_data['Heat Index (°C)'] > 50, 1, 0)
    model = LogisticRegression()
    model.fit(X, y)
    pred = model.predict([[chart_data['Heat Index (°C)'].iloc[-1], chart_data['Smoke Density (%)'].iloc[-1]]])[0]

    if pred == 1:
        st.error("🔥 AI Prediction: Potential Fire Risk Detected!", icon="🚨")
    else:
        st.success("✅ AI Prediction: System Normal", icon="🟢")

with st.expander("🛠️ Emergency Countermeasures"):
    if mode == "🚨 FIRE EMERGENCY":
        st.warning("1. Civil Defense Units Dispatched")
        if st.button("ACTIVATE SPRINKLERS"):
            st.snow()
            st.success("Sprinklers engaged in Sector B.")
    else:
        st.info("System on standby. All nodes reporting normal values.")

st.divider()
st.markdown("<center>© 2026 PyroVision AI - Ismailia WE Applied Technology School</center>", unsafe_allow_html=True)

