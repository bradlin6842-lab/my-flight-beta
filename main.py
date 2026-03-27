import streamlit as st
import pandas as pd
import pydeck as pdk
from datetime import datetime

# 1. 頁面配置
st.set_page_config(page_title="2026 Mission Tracker", layout="wide")

# 2. 基本樣式
st.markdown("""
    <style>
    .stMetric { background-color: #ffffff; border: 1px solid #eeeeee; padding: 15px; border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# 3. 2026 年度完整行程數據 (14 航段)
today = datetime(2026, 3, 27)

missions = [
    {"no": "JX 886", "date": "2026-04-16", "time": "07:20-09:40", "from": "TPE", "to": "SHI", "f_coord": [121.2, 25.0], "t_coord": [125.1, 24.8], "color": [227, 179, 65]},
    {"no": "JX 887", "date": "2026-04-21", "time": "10:40-11:00", "from": "SHI", "to": "TPE", "f_coord": [125.1, 24.8], "t_coord": [121.2, 25.0], "color": [227, 179, 65]},
    {"no": "BR 192", "date": "2026-05-03", "time": "07:20-11:30", "from": "TSA", "to": "HND", "f_coord": [121.5, 25.0], "t_coord": [139.7, 35.5], "color": [0, 210, 106]},
    {"no": "BR 191", "date": "2026-05-05", "time": "12:40-15:05", "from": "HND", "to": "TSA", "f_coord": [139.7, 35.5], "t_coord": [121.5, 25.0], "color": [0, 210, 106]},
    {"no": "JX 822", "date": "2026-05-29", "time": "10:15-14:00", "from": "TPE", "to": "KIX", "f_coord": [121.2, 25.0], "t_coord": [135.2, 34.4], "color": [227, 179, 65]},
    {"no": "JX 823", "date": "2026-06-01", "time": "15:10-17:05", "from": "KIX", "to": "TPE", "f_coord": [135.2, 34.4], "t_coord": [121.2, 25.0], "color": [227, 179, 65]},
    {"no": "JX 846", "date": "2026-07-03", "time": "07:30-10:45", "from": "TPE", "to": "KMJ", "f_coord": [121.2, 25.0], "t_coord": [130.8, 32.8], "color": [227, 179, 65]},
    {"no": "JX 847", "date": "2026-07-05", "time": "11:55-13:20", "from": "KMJ", "to": "TPE", "f_coord": [130.8, 32.8], "t_coord": [121.2, 25.0], "color": [227, 179, 65]},
    {"no": "JX 800", "date": "2026-07-22", "time": "08:30-12:55", "from": "TPE", "to": "NRT", "f_coord": [121.2, 25.0], "t_coord": [140.3, 35.7], "color": [227, 179, 65]},
    {"no": "BR 183", "date": "2026-07-26", "time": "13:25-16:05", "from": "NRT", "to": "TPE", "f_coord": [140.3, 35.7], "t_coord": [121.2, 25.0], "color": [0, 210, 106]},
    {"no": "BR 95",  "date": "2026-08-21", "time": "23:55-07:35", "from": "TPE", "to": "MXP", "f_coord": [121.2, 25.0], "t_coord": [9.1, 45.4], "color": [0, 210, 106]},
    {"no": "BR 96",  "date": "2026-08-31", "time": "11:15-06:05", "from": "MXP", "to": "TPE", "f_coord": [9.1, 45.4], "t_coord": [121.2, 25.0], "color": [0, 210, 106]},
    {"no": "SQ 877", "date": "2026-09-22", "time": "14:25-19:00", "from": "TPE", "to": "SIN", "f_coord": [121.2, 25.0], "t_coord": [103.9, 1.3], "color": [255, 149, 0]},
    {"no": "SQ 352", "date": "2026-09-23", "time": "00:05-07:10", "from": "SIN", "to": "CPH", "f_coord": [103.9, 1.3], "t_coord": [12.6, 55.6], "color": [255, 149, 0]},
]

# 4. 3D 地圖展示
st.subheader("2026 Global Mission Map")
layer = pdk.Layer(
    "ArcLayer",
    pd.DataFrame(missions),
    get_source_position="f_coord",
    get_target_position="t_coord",
    get_source_color="color",
    get_target_color=[200, 200, 200],
    get_width=4,
)

st.pydeck_chart(pdk.Deck(
    layers=[layer],
    initial_view_state=pdk.ViewState(latitude=30, longitude=80, zoom=1.2, pitch=30),
    map_style=None
))

st.divider()

# 5. 任務列表 (原生 Streamlit 組件，拒絕標籤溢出)
st.subheader("UPCOMING MISSIONS")
for m in missions:
    with st.container():
        d_left = (datetime.strptime(m['date'], "%Y-%m-%d") - today).days
        c1, c2, c3 = st.columns([1, 2, 2])
        c1.metric("DAYS", d_left)
        c2.write(f"**{m['no']}**")
        c2.write(f"{m['from']} → {m['to']}")
        c3.write(f"📅 {m['date']}")
        c3.write(f"🕒 {m['time']}")
        st.divider()
