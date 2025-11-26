import streamlit as st

# ----------------------------------------
# 기본 설정
# ----------------------------------------
st.set_page_config(
    page_title="깡통체크 | 전·월세 보증금 위험도 스캔",
    page_icon="🏠",
    layout="wide",
)

# ----------------------------------------
# CSS (디자인용)
# ----------------------------------------
st.markdown(
    """
<style>
    .stApp {
        background: radial-gradient(circle at top, #1f2937 0, #020617 55%, #020617 100%);
        color: #e5e7eb;
        font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",system-ui,sans-serif;
    }
    .card {
        background: radial-gradient(circle at top left,#111827 0,#020617 55%,#020617 100%);
        border-radius: 18px;
        border: 1px solid rgba(148,163,184,0.28);
        box-shadow: 0 18px 42px rgba(15,23,42,0.8);
        padding: 18px 20px 20px;
    }
    .header-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 12px;
        margin-bottom: 12px;
    }
    .logo-wrap {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .logo-mark {
        width: 40px;
        height: 40px;
        border-radius: 14px;
        background: conic-gradient(from 210deg,#38bdf8,#4ade80,#22c55e,#0ea5e9);
        display:flex;
        align-items:center;
        justify-content:center;
        box-shadow:0 12px 28px rgba(56,189,248,.7);
        position:relative;
        overflow:hidden;
    }
    .logo-mark::after{
        content:"";
        position:absolute;
        inset:5px;
        border-radius:12px;
        background:rgba(15,23,42,.92);
