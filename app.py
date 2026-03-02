import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# --- 簡單的登入密碼檢查 ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False
    
    if st.session_state.password_correct:
        return True

    st.title("🔐 請登入以訪問")
    password = st.text_input("輸入密碼：", type="password")
    if st.button("登入"):
        if password == "1234": # <--- 這裡可以改成你想要的密碼
            st.session_state.password_correct = True
            st.rerun()
        else:
            st.error("密碼錯誤！")
    return False

# 執行檢查
if check_password():
    # --- 這裡開始是原本的投資程式碼 ---
    st.set_page_config(page_title="私人投資助手", layout="wide")
    st.title("🏹 Pentagon Oracle 9.0 Pro")
    
    target = st.text_input("🔍 輸入股票代號 (例如 NVDA 或 0700.HK)", value="NVDA").upper()
    
    # 數據獲取與顯示 (與之前提供的邏輯相同)
    @st.cache_data(ttl=600)
    def get_data(symbol):
        try:
            data = yf.download(symbol, period='1y')
            if data.empty: return None
            if isinstance(data.columns, pd.MultiIndex):
                data.columns = data.columns.get_level_values(0)
            return data
        except: return None

    df = get_data(target)
    if df is not None:
        st.metric("當前價格", f"${df['Close'].iloc[-1]:.2f}")
        fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
        fig.update_layout(template="plotly_dark", height=500, xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("請輸入正確的代號。")
