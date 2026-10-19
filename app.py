"""
MarineSense — Marine Sensor Monitoring Dashboard
=================================================
A beginner-friendly demo dashboard inspired by marine monitoring systems.

IMPORTANT:
- This project uses SIMULATED data. It is not connected to a real ship or sensor.
- It is a portfolio/learning demo, not a certified safety or navigation system.
- Many comments are included to help you explain the code during a conversation.

Run locally:
    python -m pip install -r requirements.txt
    python -m streamlit run app.py
"""

from datetime import datetime, timedelta
import random
import time

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ---------------------------------------------------------------------------
# 1. PAGE SETUP
# ---------------------------------------------------------------------------
# Streamlit turns this Python file into a web dashboard.
# "wide" gives our charts and metric cards more horizontal room.
st.set_page_config(
    page_title="MarineSense | Sensor Monitoring",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------------------------
# 2. VISUAL THEME (CSS)
# ---------------------------------------------------------------------------
# This CSS is only presentation. The actual dashboard logic is still Python.
st.markdown(
    """
    <style>
      .stApp { background: linear-gradient(180deg, #071525 0%, #0a1d30 100%); }
      [data-testid="stSidebar"] { background: #0c2033; }
      h1, h2, h3, p, label { color: #e9f3fb; }
      div[data-testid="stMetric"] {
        background: rgba(19, 47, 70, 0.88);
        border: 1px solid #234761;
        padding: 16px;
        border-radius: 14px;
      }
      div[data-testid="stMetricLabel"] { color: #9db9cc; }
      div[data-testid="stMetricValue"] { color: #ffffff; }
      .small-note { color: #9db9cc; font-size: 0.9rem; }
      .status-pill {
        display: inline-block; padding: 5px 10px; border-radius: 999px;
        background: #123b3b; color: #7ff0d0; font-weight: 700;
        border: 1px solid #1b6a62;
      }
      .warning-pill {
        display: inline-block; padding: 5px 10px; border-radius: 999px;
        background: #4b2c15; color: #ffd28b; font-weight: 700;
        border: 1px solid #946022;
      }
      section[data-testid="stMain"] .block-container { padding-top: 1.8rem; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# 3. SIMULATED SENSOR DATA
# ---------------------------------------------------------------------------
# In a real system, these values could arrive from physical sensors, an API,
# a message broker such as MQTT, or a file. For this demo, random values make
# the dashboard feel alive without needing any hardware or internet access.
def generate_sensor_reading(previous=None):
    """Create one realistic-looking (but fictional) sensor reading."""
    previous = previous or {"roll": 2.0, "pitch": 1.0, "heave": 0.25, "accel": 0.15}

    # Small changes from the previous reading make the line chart smoother
    # than completely random numbers on every update.
    roll = max(-18.0, min(18.0, previous["roll"] + random.uniform(-2.4, 2.4)))
    pitch = max(-12.0, min(12.0, previous["pitch"] + random.uniform(-1.6, 1.6)))
    heave = max(-2.0, min(2.0, previous["heave"] + random.uniform(-0.22, 0.22)))
    accel = max(0.0, min(2.5, previous["accel"] + random.uniform(-0.18, 0.18)))

    # Occasionally add a simulated event so you can demonstrate the alarm UI.
    # This is deliberately rare: most readings should remain in a normal range.
    if random.random() < 0.06:
        roll = random.choice([-1, 1]) * random.uniform(10.5, 16.5)
        accel = random.uniform(1.4, 2.2)

    return {
        "timestamp": datetime.now(),
        "roll": round(roll, 2),       # rotation from side to side, in degrees
        "pitch": round(pitch, 2),     # rotation forward/backward, in degrees
        "heave": round(heave, 2),     # vertical movement, in metres (demo label)
        "accel": round(accel, 2),     # acceleration, in m/s² (demo label)
        "temperature": round(random.uniform(18.0, 24.0), 1),
    }


def make_history(number_of_points=60):
    """Build historical fictional readings for the first dashboard load."""
    rows = []
    previous = {"roll": 2.0, "pitch": 1.0, "heave": 0.25, "accel": 0.15}
    start = datetime.now() - timedelta(minutes=number_of_points - 1)

    for index in range(number_of_points):
        reading = generate_sensor_reading(previous)
        # Give history points timestamps in the past, one minute apart.
        reading["timestamp"] = start + timedelta(minutes=index)
        rows.append(reading)
        previous = reading

    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# 4. SESSION STATE
# ---------------------------------------------------------------------------
# Streamlit reruns this script after user interactions. Session State keeps
# our generated readings available between those reruns.
if "sensor_history" not in st.session_state:
    st.session_state.sensor_history = make_history(60)

if "is_live" not in st.session_state:
    st.session_state.is_live = False

if "last_reading" not in st.session_state:
    st.session_state.last_reading = st.session_state.sensor_history.iloc[-1].to_dict()


# ---------------------------------------------------------------------------
# 5. SIDEBAR CONTROLS
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🌊 MarineSense")
    st.caption("MARINE SENSOR MONITORING • DEMO")
    st.divider()

    vessel_name = st.selectbox(
        "Demo vessel",
        ["MV Northstar", "MV Blue Horizon", "MV Ocean Pioneer"],
        help="These vessel names are fictional and only used for the demo.",
    )

    # The thresholds are adjustable so a presenter can trigger an alarm live.
    roll_limit = st.slider(
        "Roll warning threshold (°)",
        min_value=5,
        max_value=18,
        value=12,
        help="A warning is shown when the absolute roll angle reaches this value.",
    )
    accel_limit = st.slider(
        "Acceleration warning (m/s²)",
        min_value=0.5,
        max_value=2.5,
        value=1.5,
        step=0.1,
    )

    st.divider()
    st.markdown("### Demo controls")
    if st.button("🔄 Generate new reading", use_container_width=True):
        new_reading = generate_sensor_reading(st.session_state.last_reading)
        st.session_state.last_reading = new_reading
        st.session_state.sensor_history = pd.concat(
            [st.session_state.sensor_history, pd.DataFrame([new_reading])],
            ignore_index=True,
        ).tail(180)
        st.rerun()

    live_toggle = st.toggle("Live simulation (refresh every 3 sec)", value=st.session_state.is_live)
    st.session_state.is_live = live_toggle

    st.caption("Data source: simulated readings — no real sensors connected.")


# ---------------------------------------------------------------------------
# 6. CALCULATE CURRENT STATUS
# ---------------------------------------------------------------------------
# The latest row is the most recent sensor reading in our table.
history = st.session_state.sensor_history.copy()
latest = st.session_state.last_reading

# Use absolute roll because a large negative angle can also be significant.
roll_warning = abs(float(latest["roll"])) >= roll_limit
accel_warning = float(latest["accel"]) >= accel_limit
has_warning = roll_warning or accel_warning

# Status text is derived from the data; it isn't manually hard-coded.
if has_warning:
    status_text = "WARNING — CHECK SENSOR VALUES"
    status_icon = "⚠️"
else:
    status_text = "NOMINAL — VALUES WITHIN DEMO LIMITS"
    status_icon = "✅"


# ---------------------------------------------------------------------------
# 7. DASHBOARD HEADER
# ---------------------------------------------------------------------------
left, right = st.columns([3, 1])
with left:
    st.markdown("# 🌊 MarineSense")
    st.markdown("### Marine motion & sensor monitoring")
    st.markdown(
        f"<span class='small-note'>VESSEL: <b>{vessel_name}</b> &nbsp; • &nbsp; "
        f"LAST UPDATE: {latest['timestamp'].strftime('%H:%M:%S')}</span>",
        unsafe_allow_html=True,
    )
with right:
    if has_warning:
        st.markdown(f"<span class='warning-pill'>{status_icon} {status_text}</span>", unsafe_allow_html=True)
    else:
        st.markdown(f"<span class='status-pill'>{status_icon} {status_text}</span>", unsafe_allow_html=True)

st.info(
    "Portfolio demo only: the measurements are simulated and must not be used "
    "for navigation, cargo decisions, or real-world safety."
)


# ---------------------------------------------------------------------------
# 8. KPI / METRIC CARDS
# ---------------------------------------------------------------------------
# Metric cards give a quick overview before someone studies the charts.
m1, m2, m3, m4 = st.columns(4)
m1.metric("Roll angle", f"{latest['roll']:.2f}°", help="Side-to-side rotation in this fictional data set.")
m2.metric("Pitch angle", f"{latest['pitch']:.2f}°", help="Forward/backward rotation.")
m3.metric("Heave", f"{latest['heave']:.2f} m", help="Vertical movement — demo unit.")
m4.metric("Acceleration", f"{latest['accel']:.2f} m/s²", help="Acceleration — demo unit.")

st.write("")


# ---------------------------------------------------------------------------
# 9. TIME-SERIES CHARTS
# ---------------------------------------------------------------------------
# Plotly charts are interactive: the viewer can hover, zoom, and toggle lines.
chart_left, chart_right = st.columns(2)

with chart_left:
    st.subheader("Vessel motion")
    motion_fig = go.Figure()
    motion_fig.add_trace(go.Scatter(
        x=history["timestamp"], y=history["roll"], mode="lines",
        name="Roll (°)", line=dict(width=2, color="#4cc9f0")
    ))
    motion_fig.add_trace(go.Scatter(
        x=history["timestamp"], y=history["pitch"], mode="lines",
        name="Pitch (°)", line=dict(width=2, color="#f4a261")
    ))
    # Dashed lines show the warning thresholds to make the alarm logic visible.
    motion_fig.add_hline(y=roll_limit, line_dash="dash", line_color="#ff6b6b",
                         annotation_text="Roll limit")
    motion_fig.add_hline(y=-roll_limit, line_dash="dash", line_color="#ff6b6b")
    motion_fig.update_layout(
        template="plotly_dark", height=360, margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        xaxis_title="Time", yaxis_title="Angle (degrees)",
    )
    st.plotly_chart(motion_fig, use_container_width=True)

with chart_right:
    st.subheader("Vertical movement & acceleration")
    data_fig = go.Figure()
    data_fig.add_trace(go.Scatter(
        x=history["timestamp"], y=history["heave"], mode="lines",
        name="Heave (m)", line=dict(width=2, color="#80ed99")
    ))
    data_fig.add_trace(go.Scatter(
        x=history["timestamp"], y=history["accel"], mode="lines",
        name="Acceleration (m/s²)", yaxis="y2", line=dict(width=2, color="#c77dff")
    ))
    data_fig.update_layout(
        template="plotly_dark", height=360, margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        xaxis_title="Time",
        yaxis=dict(title="Heave (m)"),
        yaxis2=dict(title="Acceleration (m/s²)", overlaying="y", side="right"),
    )
    st.plotly_chart(data_fig, use_container_width=True)


# ---------------------------------------------------------------------------
# 10. ALARM PANEL
# ---------------------------------------------------------------------------
st.subheader("🚨 Alarm panel")
alarm_rows = []

if roll_warning:
    alarm_rows.append({
        "Severity": "HIGH",
        "Sensor": "Roll angle",
        "Current value": f"{latest['roll']:.2f}°",
        "Rule": f"Absolute roll ≥ {roll_limit}°",
        "Suggested action": "Review the reading and verify sensor quality",
    })

if accel_warning:
    alarm_rows.append({
        "Severity": "HIGH",
        "Sensor": "Acceleration",
        "Current value": f"{latest['accel']:.2f} m/s²",
        "Rule": f"Acceleration ≥ {accel_limit:.1f} m/s²",
        "Suggested action": "Review the reading and verify sensor quality",
    })

if alarm_rows:
    st.dataframe(pd.DataFrame(alarm_rows), use_container_width=True, hide_index=True)
else:
    st.success("No demo threshold exceeded in the latest reading.")

st.caption(
    "Alarm thresholds are illustrative and user-adjustable. They are not validated "
    "engineering limits and do not imply that a vessel is safe or unsafe."
)


# ---------------------------------------------------------------------------
# 11. RAW DATA + CSV EXPORT
# ---------------------------------------------------------------------------
with st.expander("🔎 Inspect raw sensor data"):
    st.markdown(
        "This table shows the values behind the charts. In a real project, "
        "you would also document sensor units, calibration, missing values, and data quality."
    )
    st.dataframe(history.sort_values("timestamp", ascending=False), use_container_width=True, hide_index=True)

# CSV is a simple way to share data with Excel or other analysis tools.
csv_data = history.to_csv(index=False).encode("utf-8")
st.download_button(
    label="⬇️ Download sensor history (CSV)",
    data=csv_data,
    file_name="marinesense_sensor_history.csv",
    mime="text/csv",
)

# Small footer explains the architecture in plain language.
st.divider()
st.markdown("**Demo architecture:** Python → simulated sensor readings → Pandas → Plotly charts → Streamlit UI")
st.caption("Built as a learning/portfolio project. Replace the simulator with a verified data source before any real deployment.")


# ---------------------------------------------------------------------------
# 12. OPTIONAL LIVE REFRESH
# ---------------------------------------------------------------------------
# This intentionally refreshes only while the user enables the toggle.
# A refresh creates one new fictional reading, then Streamlit reruns the app.
if st.session_state.is_live:
    time.sleep(3)
    new_reading = generate_sensor_reading(st.session_state.last_reading)
    st.session_state.last_reading = new_reading
    st.session_state.sensor_history = pd.concat(
        [st.session_state.sensor_history, pd.DataFrame([new_reading])],
        ignore_index=True,
    ).tail(180)
    st.rerun()
