import streamlit as st
import requests

# 1. 頁面配置
st.set_page_config(page_title="FLIGHT SENTRY", layout="centered")

# 2. 極簡黑白 CSS (移除可能報錯的複雜選擇器)
st.markdown("""
    <style>
    body, .main, [data-testid="stAppViewContainer"] {
        background-color: #000000 !important;
        color: #ffffff !important;
    }
    input {
        background-color: #111 !important;
        color: #fff !important;
        border: 1px solid #333 !important;
    }
    button {
        background-color: #fff !important;
        color: #000 !important;
        border-radius: 0px !important;
    }
    div[data-testid="stMetric"] {
        background-color: #000;
        border: 1px solid #222;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 讀取 Secrets
try:
    API_KEY = st.secrets["AVIATION_KEY"]
    TG_TOKEN = st.secrets["TG_TOKEN"]
    CHAT_ID = st.secrets["TG_CHAT_ID"]
except Exception:
    st.error("Secrets missing. Check Streamlit Cloud Settings.")
    st.stop()

# 4. 主介面
st.title("FLIGHT SENTRY")
st.caption("ULTRA-MINIMALIST TERMINAL")

flight_no = st.text_input("FLIGHT ID", value="BR192").upper().strip()

if st.button("EXECUTE SYNC"):
    url = f"http://api.aviationstack.com/v1/flights?access_key={API_KEY}&flight_iata={flight_no}"
    with st.spinner("SYNCING..."):
        try:
            r = requests.get(url, timeout=10).json()
            if 'data' in r and len(r['data']) > 0:
                f = r['data'][0]
                
                c1, c2 = st.columns(2)
                c1.metric("STATUS", f['flight_status'].upper())
                c2.metric("GATE", f['departure']['gate'] or "TBD")
                
                st.write(f"**FROM:** {f['departure']['airport']}")
                st.write(f"**TO:** {f['arrival']['airport']}")
                
                # 自動發送 Telegram 通知
                msg = f"✈️ SENTRY: {flight_no} is {f['flight_status'].upper()}. Gate: {f['departure']['gate'] or 'TBD'}"
                requests.post(f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage", 
                             data={"chat_id": CHAT_ID, "text": msg})
                st.success("TELEGRAM NOTIFIED.")
            else:
                st.warning("NO DATA FOUND.")
        except Exception as e:
            st.error(f"SYNC ERROR: {e}")
