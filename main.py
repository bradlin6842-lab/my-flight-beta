import streamlit as st
import pandas as pd
import pydeck as pdk
import requests

# 1. 頁面配置與 Flighty 風格 CSS
st.set_page_config(page_title="Flighty Clone", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* 全螢幕背景與深色調 */
    .main { background-color: #0b0d10; }
    [data-testid="stAppViewContainer"] { background-color: #0b0d10; }
    
    /* 模擬 iOS 卡片 */
    .flight-card {
        background: rgba(30, 31, 35, 0.8);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 15px;
        border: 1px solid rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
    }
    .date-text { font-size: 2.5rem; font-weight: 800; color: #fff; line-height: 1; }
    .day-left { color: #888; font-size: 0.8rem; text-transform: uppercase; }
    .airport-code { font-weight: 700; color: #fff; font-size: 1.2rem; }
    .flight-time { color: #aaa; font-size: 0.9rem; }
    </style>
    """, unsafe_allow_html=True)

# 2. 模擬行程數據 (整合你接下來的 TSA-HND 與 下地島行程)
flights = [
    {"no": "JX 886", "from": "TPE", "to": "SHI", "date": "16 Apr", "days": "20", "from_coord": [121.23, 25.07], "to_coord": [125.14, 24.83], "time": "7:20 AM - 9:40 AM"},
    {"no": "JX 887", "from": "SHI", "to": "TPE", "date": "21 Apr", "days": "25", "from_coord": [125.14, 24.83], "to_coord": [121.23, 25.07], "time": "10:40 AM - 11:00 AM"},
    {"no": "BR 192", "from": "TSA", "to": "HND", "date": "03 May", "days": "37", "from_coord": [121.55, 25.06], "to_coord": [139.77, 35.54], "time": "7:20 AM - 11:30 AM"},
]

# 3. 繪製 3D 飛行地球 (Pydeck)
st.write("### Global Flight Path")

# 建立飛行路徑數據
arc_data = pd.DataFrame([
    {"name": f["no"], "source": f["from_coord"], "target": f["to_coord"]} for f in flights
])

layer = pdk.Layer(
    "ArcLayer",
    arc_data,
    get_source_position="source",
    get_target_position="target",
    get_source_color=[50, 150, 255, 160],
    get_target_color=[0, 200, 255, 200],
    get_width=3,
    pickable=True,
)

view_state = pdk.ViewState(latitude=25.0, longitude=130.0, zoom=3, pitch=45, bearing=0)

st.pydeck_chart(pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    map_style="mapbox://styles/mapbox/dark-v10", # 深色地圖
))

# 4. 模擬 My Flights 列表
st.write("#### My Flights")

for f in flights:
    st.markdown(f"""
    <div class="flight-card">
        <div style="display: flex; align-items: center;">
            <div style="flex: 0 0 80px;">
                <div class="date-text">{f['days']}</div>
                <div class="day-left">DAYS</div>
            </div>
            <div style="flex: 1; margin-left: 20px;">
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: #e3b341; font-weight: bold;">⚡ {f['no']}</span>
                    <span style="color: #888;">{f['date']}</span>
                </div>
                <div style="margin-top: 5px;">
                    <span class="airport-code">{f['from']}</span> 
                    <span style="color: #666; margin: 0 10px;">→</span>
                    <span class="airport-code">{f['to']}</span>
                </div>
                <div class="flight-time">🕒 {f['time']}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 5. 保留原本的 API 同步按鈕 (放在最下方或 Sidebar)
with st.expander("Update Current Flight Data"):
    input_no = st.text_input("Input Flight No to Sync", "JX886")
    if st.button("Sync Now"):
        st.write("Connecting to AviationStack...")
        # 這裡放入你原本的 API 呼叫代碼
