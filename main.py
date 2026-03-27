import streamlit as st
import requests
import datetime

# 1. 頁面配置 (Leica 極簡風格)
st.set_page_config(page_title="FLIGHT SENTRY", layout="centered")

# 2. 自定義 CSS (Leica Monochrom 風格：純黑背景、白字、無圓角)
st.markdown("""
    <style>
    .main { background-color: #000000; color: #ffffff; }
    [data-testid="stAppViewContainer"] { background-color: #000000; }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    .stTextInput>div>div>input {
        background-color: #111; color: #fff; border: 1px solid #333; border-radius: 0px;
    }
    .stButton>button {
        background-color: #ffffff; color: #000000; border-radius: 0px; 
        font-weight: bold; width: 100%; border: none;
    }
    .stMetric { border: 1px solid #222; padding: 15px; }
    [data-testid="stMetricValue"] { color: #ffffff; font-family: 'Courier New', monospace; }
    [data-testid="stMetricLabel"] { color: #888; }
    h1, h2, h3 { color: #ffffff; font-family: 'Helvetica Neue', sans-serif; letter-spacing: 2px; }
    </style>
    """, unsafe_allow_html=True)

# 3. 讀取 Secrets
try:
    API_KEY = st.secrets["AVIATION_KEY"]
    TG_TOKEN = st.secrets["TG_TOKEN"]
    CHAT_ID = st.secrets["TG_CHAT_ID"]
except Exception as e:
    st.error("Secrets 尚未設定完整，請檢查 Streamlit Cloud Settings。")
    st.stop()

# 4. 主介面
st.title("FLIGHT SENTRY")
st.caption("ULTRA-MINIMALIST DATA TERMINAL v1.0")
st.divider()

# 輸入航班號 (例如 TSA-HND 的 BR192)
flight_no = st.text_input("INPUT FLIGHT IATA", value="BR192").upper().replace(" ", "")

def get_flight_data(flight_code):
    """從 AviationStack 抓取數據"""
    url = f"http://api.aviationstack.com/v1/flights?access_key={API_KEY}&flight_iata={flight_code}"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if 'data' in data and len(data['data']) > 0:
            return data['data'][0]
        return None
    except Exception as e:
        return f"Error: {str(e)}"

# 5. 執行按鈕
if st.button("EXECUTE SYNC"):
    with st.spinner("COMMUNICATING WITH SATELLITE..."):
        flight = get_flight_data(flight_no)
        
        if flight:
            # 建立兩欄顯示數據
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric(label="STATUS", value=flight['flight_status'].upper())
                st.write(f"**DEP:** {flight['departure']['airport']}")
                st.write(f"**GATE:** {flight['departure']['gate'] or 'TBD'}")
            
            with col2:
                # 抓取預計抵達時間 (取字串中的時間部分)
                est_time = flight['arrival']['estimated'][11:16] if flight['arrival']['estimated'] else "N/A"
                st.metric(label="EST. ARRIVAL", value=est_time)
                st.write(f"**ARR:** {flight['arrival']['airport']}")
                st.write(f"**TERM:** {flight['arrival']['terminal'] or 'N/A'}")
            
            st.divider()
            
            # 6. Telegram 推播測試
            if st.button("SEND ALERT TO TELEGRAM"):
                msg = (f"✈️ SENTRY ALERT\n"
                       f"Flight: {flight_no}\n"
                       f"Status: {flight['flight_status'].upper()}\n"
                       f"Gate: {flight['departure']['gate'] or 'N/A'}\n"
                       f"Est. Arrival: {est_time}")
                
                tg_url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
                tg_res = requests.post(tg_url, data={"chat_id": CHAT_ID, "text": msg})
                
                if tg_res.status_code == 200:
                    st.success("TELEGRAM NOTIFICATION SENT.")
                else:
                    st.error("TELEGRAM FAILED. CHECK TOKEN/ID.")
        else:
            st.warning("NO ACTIVE DATA FOUND FOR THIS FLIGHT.")

st.sidebar.markdown("### MISSION LOG")
st.sidebar.write("Tracking active for Aug Milan & Sep Copenhagen missions.")
