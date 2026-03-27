import streamlit as st
import requests
import datetime

# 設定 API
AVIATION_API_KEY = "你的_AviationStack_Key"
TG_TOKEN = "你的_Telegram_Token"
CHAT_ID = "你的_Chat_ID"

st.set_page_config(page_title="Personal Flight Sentry", layout="wide")

# 模擬 Leica 風格 CSS
st.markdown("""
    <style>
    .main { background-color: #000000; color: #ffffff; }
    .stMetric { border: 1px solid #333; padding: 10px; border-radius: 5px; }
    </style>
    """, unsafe_allow_index=True)

st.title("P.F.S. | Flight Tracker")

flight_num = st.text_input("ENTER FLIGHT NUMBER (e.g., BR192)", "BR192")

if st.button("SYNC DATA"):
    # 呼叫 API
    url = f"http://api.aviationstack.com/v1/flights?access_key={AVIATION_API_KEY}&flight_iata={flight_num}"
    res = requests.get(url).json()
    
    if res.get('data'):
        flight = res['data'][0]
        status = flight['flight_status']
        gate = flight['departure']['gate']
        est_arrival = flight['arrival']['estimated']
        
        # 顯示數據
        col1, col2 = st.columns(2)
        col1.metric("STATUS", status.upper())
        col2.metric("GATE", gate if gate else "TBD")
        
        st.write(f"ESTIMATED ARRIVAL: {est_arrival}")
        
        # 如果狀態改變，發送 Telegram 通知
        # requests.post(f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage", 
        #               data={"chat_id": CHAT_ID, "text": f"航班 {flight_num} 狀態更新: {status}"})
