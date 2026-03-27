import streamlit as st
import pandas as pd
import pydeck as pdk
from datetime import datetime

# 1. 頁面配置
st.set_page_config(page_title="Flighty Terminal", layout="wide", initial_sidebar_state="collapsed")

# 2. Flighty 風格精緻化 CSS (加入毛玻璃與漸層)
st.markdown("""
    <style>
    .main { background-color: #050505; }
    [data-testid="stAppViewContainer"] { background-color: #050505; }
    
    /* iOS 卡片設計 */
    .flight-card {
        background: linear-gradient(145deg, #1a1b1e, #121316);
        border-radius: 24px;
        padding: 24px;
        margin-bottom: 20px;
        border: 1px solid rgba(255,255,255,0.05);
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .count-down { font-size: 2.8rem; font-weight: 800; color: #ffffff; line-height: 1; letter-spacing: -2px; }
    .unit { color: #555; font-size: 0.7rem; font-weight: 700; margin-top: 4px; }
    .airline-tag { color: #e3b341; font-weight: 700; font-size: 0.9rem; margin-bottom: 8px; }
    .airport-row { display: flex; align-items: center; margin: 12px 0; }
    .airport-code { font-size: 1.6rem; font-weight: 700; color: #fff; }
    .arrow { color: #444; margin: 0 15px; font-size: 1.2rem; }
    .info-footer { display: flex; justify-content: space-between; color: #888; font-size: 0.85rem; }
    </style>
    """, unsafe_allow_html=True)

# 3. 行程數據 (包含你 2026 年的關鍵航段)
today = datetime.now()
flight_list = [
    {"no": "JX 886", "from": "TPE", "to": "SHI", "date": "2026-04-16", "f_coord": [121.23, 25.07], "t_coord": [125.14, 24.83], "time": "07:20 - 09:40", "type": "StarLux"},
    {"no": "JX 887", "from": "SHI", "to": "TPE", "date": "2026-04-21", "f_coord": [125.14, 24.83], "t_coord": [121.23, 25.07], "time": "10:40 - 11:00", "type": "StarLux"},
    {"no": "BR 192", "from": "TSA", "to": "HND", "date": "2026-05-03", "f_coord": [121.55, 25.06], "t_coord": [139.77, 35.54], "time": "07:20 - 11:30", "type": "EVA Air"},
    {"no": "CX 233", "from": "TPE", "to": "MXP", "date": "2026-08-25", "f_coord": [121.23, 25.07], "t_coord": [9.19, 45.46], "time": "Mission: Milan", "type": "Cathay"},
]

# 4. 3D 地球視覺化 (修正底圖問題)
st.write("### Global Flight Map")

arc_df = pd.DataFrame([
    {"source": f["f_coord"], "target": f["t_coord"]} for f in flight_list
])

# 繪製弧線層
layer = pdk.Layer(
    "ArcLayer",
    arc_df,
    get_source_position="source",
    get_target_position="target",
    get_source_color=[0, 122, 255, 180], # 經典飛行藍
    get_target_color=[255, 255, 255, 200],
    get_width=4,
    tilt=15,
)

# 設定視角：對準東亞起點
view_state = pdk.ViewState(
    latitude=30.0, longitude=135.0, zoom=2.5, pitch=40, bearing=0
)

st.pydeck_chart(pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    map_style="mapbox://styles/mapbox/dark-v10", # 如果沒 Token 會顯示預設深色
    tooltip=True
))

st.write("---")
st.write("#### MY MISSIONS")

# 5. 生成卡片
for f in flight_list:
    f_date = datetime.strptime(f['date'], "%2026-%m-%d")
    days_left = (f_date - today).days
    
    # 根據航空公司調整圖示顏色
    icon_color = "#e3b341" if f['type'] == "StarLux" else "#00d26a"
    
    st.markdown(f"""
    <div class="flight-card">
        <div style="display: flex; align-items: flex-start;">
            <div style="flex: 0 0 100px;">
                <div class="count-down">{days_left if days_left > 0 else "NOW"}</div>
                <div class="unit">DAYS LEFT</div>
            </div>
            <div style="flex: 1; margin-left: 10px;">
                <div class="airline-tag" style="color: {icon_color};">⚡ {f['no']}</div>
                <div class="airport-row">
                    <span class="airport-code">{f['from']}</span>
                    <span class="arrow">→</span>
                    <span class="airport-code">{f['to']}</span>
                </div>
                <div class="info-footer">
                    <span>{f['date']}</span>
                    <span>{f['time']}</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 6. 側邊欄快速工具
with st.sidebar:
    st.title("SENTRY CONTROL")
    st.write("2026 Mission Tracker")
    if st.button("Update All Syncs"):
        st.toast("Syncing with Global Data...")
