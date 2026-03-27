import streamlit as st
import pandas as pd
import pydeck as pdk
from datetime import datetime

st.set_page_config(page_title="2026 Flight Sentry", layout="wide")

# 極簡化 CSS，防止 HTML 溢出
st.markdown("""
    <style>
    .main { background-color: #050505; color: white; }
    .card {
        background: #1a1b1e;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
        border-left: 5px solid #e3b341;
    }
    .big-num { font-size: 30px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 行程數據 (保持你提供的 14 航段)
today = datetime(2026, 3, 27)
missions = [
    {"no": "JX 886", "date": "2026-04-16", "from": "TPE", "to": "SHI", "f_coord": [121.2, 25.0], "t_coord": [125.1, 24.8]},
    {"no": "JX 887", "date": "2026-04-21", "from": "SHI", "to": "TPE", "f_coord": [125.1, 24.8], "t_coord": [121.2, 25.0]},
    {"no": "BR 192", "date": "2026-05-03", "from": "TSA", "to": "HND", "f_coord": [121.5, 25.0], "t_coord": [139.7, 35.5]},
    # ... 其他行程依此類推
]

# 繪製地圖
st.write("### 2026 Global Map")
arc_layer = pdk.Layer(
    "ArcLayer",
    pd.DataFrame(missions),
    get_source_position="f_coord",
    get_target_position="t_coord",
    get_source_color=[0, 122, 255],
    get_target_color=[255, 255, 255],
    get_width=3,
)

st.pydeck_chart(pdk.Deck(
    layers=[arc_layer],
    initial_view_state=pdk.ViewState(latitude=30, longitude=110, zoom=1.5),
    map_style=None, # 修正全黑問題
))

# 顯示卡片
st.write("### Upcoming Missions")
for m in missions:
    d_left = (datetime.strptime(m['date'], "%Y-%m-%d") - today).days
    st.markdown(f"""
    <div class="card">
        <span class="big-num">{d_left}</span> DAYS LEFT | <b>{m['no']}</b><br>
        {m['from']} → {m['to']} ({m['date']})
    </div>
    """, unsafe_allow_html=True)
