import streamlit as st
import pandas as pd
import pydeck as pdk
from datetime import datetime

# 1. 頁面配置 (全寬模式以展示 3D 地球)
st.set_page_config(page_title="Global Mission Tracker", layout="wide", initial_sidebar_state="collapsed")

# 2. 全新明亮風格 CSS
st.markdown("""
    <style>
    /* 全螢幕背景與明亮調 */
    .main { background-color: #f7f9fc; color: #1a1a1a; }
    [data-testid="stAppViewContainer"] { background-color: #f7f9fc; }
    
    /* 明亮 iOS 風格卡片 */
    .flight-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 15px;
        border: 1px solid rgba(0,0,0,0.05);
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    .count-down { font-size: 2.8rem; font-weight: 800; color: #1a1a1a; line-height: 1; letter-spacing: -2px; }
    .unit { color: #888; font-size: 0.8rem; text-transform: uppercase; font-weight: 700; margin-top: 4px; }
    .aly-info { font-weight: 700; color: #e3b341; font-size: 0.9rem; margin-bottom: 8px; }
    .airport-row { display: flex; align-items: center; margin: 10px 0; }
    .airport-code { font-size: 1.6rem; font-weight: 700; color: #1a1a1a; font-family: 'Helvetica Neue', sans-serif; }
    .arrow { color: #ccc; margin: 0 12px; font-size: 1rem; }
    .info-footer { display: flex; justify-content: space-between; color: #666; font-size: 0.85rem; }
    .transit-info { color: #ff9500; font-size: 0.8rem; margin-top: 5px; font-weight: bold;}
    </style>
    """, unsafe_allow_html=True)

# 3. 2026 年度完整行程數據 (共 14 航段)
# 座標說明: TPE[121.2, 25.0], TSA[121.5, 25.0], SHI[125.1, 24.8], HND[139.7, 35.5], KIX[135.2, 34.4], KMJ[130.8, 32.8], NRT[140.3, 35.7], MXP[9.1, 45.4], SIN[103.9, 1.3], CPH[12.6, 55.6]

today = datetime.now() # 假設今天是 2026-03-27

mission_data = [
    # --- MISSION: SHIMOJISHIMA (Apr) ---
    {"no": "JX 886", "date": "2026-04-16", "time": "07:20 - 09:40", "from": "TPE", "to": "SHI", "f_coord": [121.2, 25.0], "t_coord": [125.1, 24.8], "aly": "StarLux", "color": "#e3b341"},
    {"no": "JX 887", "date": "2026-04-21", "time": "10:40 - 11:00", "from": "SHI", "to": "TPE", "f_coord": [125.1, 24.8], "t_coord": [121.2, 25.0], "aly": "StarLux", "color": "#e3b341"},
    
    # --- MISSION: TOKYO & OSAKA (May) ---
    {"no": "BR 192", "date": "2026-05-03", "time": "07:20 - 11:30", "from": "TSA", "to": "HND", "f_coord": [121.5, 25.0], "t_coord": [139.7, 35.5], "aly": "EVA Air", "color": "#00d26a"},
    {"no": "BR 191", "date": "2026-05-05", "time": "12:40 - 15:05", "from": "HND", "to": "TSA", "f_coord": [139.7, 35.5], "t_coord": [121.5, 25.0], "aly": "EVA Air", "color": "#00d26a"},
    {"no": "JX 822", "date": "2026-05-29", "time": "10:15 - 14:00", "from": "TPE", "to": "KIX", "f_coord": [121.2, 25.0], "t_coord": [135.2, 34.4], "aly": "StarLux", "color": "#e3b341"},
    {"no": "JX 823", "date": "2026-06-01", "time": "15:10 - 17:05", "from": "KIX", "to": "TPE", "f_coord": [135.2, 34.4], "t_coord": [121.2, 25.0], "aly": "StarLux", "color": "#e3b341"},

    # --- MISSION: KUMAMOTO & TOKYO (Jul) ---
    {"no": "JX 846", "date": "2026-07-03", "time": "07:30 - 10:45", "from": "TPE", "to": "KMJ", "f_coord": [121.2, 25.0], "t_coord": [130.8, 32.8], "aly": "StarLux", "color": "#e3b341"},
    {"no": "JX 847", "date": "2026-07-05", "time": "11:55 - 13:20", "from": "KMJ", "to": "TPE", "f_coord": [130.8, 32.8], "t_coord": [121.2, 25.0], "aly": "StarLux", "color": "#e3b341"},
    {"no": "JX 800", "date": "2026-07-22", "time": "08:30 - 12:55", "from": "TPE", "to": "NRT", "f_coord": [121.2, 25.0], "t_coord": [140.3, 35.7], "aly": "StarLux", "color": "#e3b341"},
    {"no": "BR 183", "date": "2026-07-26", "time": "13:25 - 16:05", "from": "NRT", "to": "TPE", "f_coord": [140.3, 35.7], "t_coord": [121.2, 25.0], "aly": "EVA Air", "color": "#00d26a"},

    # --- MISSION: MILAN UTMB (Aug) ---
    {"no": "BR 95",  "date": "2026-08-21", "time": "23:55 - 07:35(+1)", "from": "TPE", "to": "MXP", "f_coord": [121.2, 25.0], "t_coord": [9.1, 45.4], "aly": "EVA Air", "color": "#00d26a"},
    {"no": "BR 96",  "date": "2026-08-31", "time": "11:15 - 06:05(+1)", "from": "MXP", "to": "TPE", "f_coord": [9.1, 45.4], "t_coord": [121.2, 25.0], "aly": "EVA Air", "color": "#00d26a"},

    # --- MISSION: COPENHAGEN HYROX (Sep) ---
    {"no": "SQ 877", "date": "2026-09-22", "time": "14:25 - 19:00", "from": "TPE", "to": "CPH", "f_coord": [121.2, 25.0], "t_coord": [12.6, 55.6], "aly": "Singapore Aly", "color": "#ff9500", "transit": "Connect at SIN"},
    {"no": "SQ 351", "date": "2026-10-05", "time": "11:55 - 13:10(+1)", "from": "CPH", "to": "TPE", "f_coord": [12.6, 55.6], "t_coord": [121.2, 25.0], "aly": "Singapore Aly", "color": "#ff9500", "transit": "Connect at SIN"},
]

# 4. 3D 全球航線圖 (明亮風格)
st.write("### 2026 Global Mission Map")

# 準備地圖數據
map_df = pd.DataFrame([
    {"source": f["f_coord"], "target": f["t_coord"], "color": f["color"]} for f in mission_data
])

# 轉換顏色格式為 pydeck 所需的 [R, G, B, A]
def hex_to_rgb(hx):
    hx = hx.lstrip('#')
    return [int(hx[i:i+2], 16) for i in (0, 2, 4)] + [180] # A=180

map_df['start_color'] = map_df['color'].apply(hex_to_rgb)
map_df['end_color'] = map_df['color'].apply(hex_to_rgb)

# 繪製弧線層
layer = pdk.Layer(
    "ArcLayer",
    map_df,
    get_source_position="source",
    get_target_position="target",
    get_source_color="start_color",
    get_target_color="end_color",
    get_width=3,
    tilt=10,
    pickable=True,
)

# 設定視角：拉高並微調角度，以同時看到亞洲與歐洲
view_state = pdk.ViewState(
    latitude=35.0, longitude=70.0, zoom=1.1, pitch=30, bearing=0
)

st.pydeck_chart(pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    # 修正：移除全黑底圖，使用明亮模式 (light)
    map_style="mapbox://styles/mapbox/light-v10", 
    tooltip=True
))

st.write("---")
st.write("#### UPCOMING MISSIONS")

# 5. 生成明亮 iOS 風格卡片
for f in mission_data:
    # 計算倒數天數
    f_date = datetime.strptime(f['date'], "%Y-%m-%d")
    days_left = (f_date - today).days
    
    # 建立卡片 HTML
    transit_html = f'<div class="transit-info">🛑 {f["transit"]}</div>' if "transit" in f else ""
    
    st.markdown(f"""
    <div class="flight-card">
        <div style="display: flex; align-items: flex-start;">
            <div style="flex: 0 0 100px;">
                <div class="count-down">{days_left if days_left > 0 else "NOW"}</div>
                <div class="unit">Days Left</div>
            </div>
            <div style="flex: 1; margin-left: 15px;">
                <div class="aly-info" style="color: {f['color']};">⚡ {f['no']} | {f['aly']}</div>
                <div class="airport-row">
                    <span class="airport-code">{f['from']}</span>
                    <span class="arrow">→</span>
                    <span class="airport-code">{f['to']}</span>
                </div>
                {transit_html}
                <div class="info-footer">
                    <span>{f['date']}</span>
                    <span>🕒 {f['time']}</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
