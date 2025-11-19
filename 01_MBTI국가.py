import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="MBTI by Country", layout="wide")

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

df = load_data()

st.title("🌍 국가별 MBTI 분포 인터랙티브 대시보드")
st.write("원하는 국가를 선택하면 MBTI 16유형 비율을 Plotly로 시각화해줍니다.")

# 국가 선택
country_list = df["Country"].sort_values().tolist()
selected_country = st.selectbox("국가 선택", country_list)

# 선택한 국가 데이터 추출
row = df[df["Country"] == selected_country].iloc[0]
mbti_cols = [c for c in df.columns if c != "Country"]

values = row[mbti_cols].values
max_idx = np.argmax(values)

# 색 구성: 최대값 = 빨강, 나머지는 회색 그라데이션
colors = []
for i, v in enumerate(values):
    if i == max_idx:
        colors.append("red")
    else:
        # 회색 그라데이션 (밝은색→진한색)
        intensity = 0.8 - (v / max(values)) * 0.6  
        colors.append(f"rgba(100,100,100,{round(intensity,2)})")

# Plotly 그래프 생성
fig = go.Figure()

fig.add_trace(go.Bar(
    x=mbti_cols,
    y=values,
    marker_color=colors
))

fig.update_layout(
    title=f"{selected_country} MBTI Distribution",
    xaxis_title="MBTI Type",
    yaxis_title="Proportion",
    template="plotly_white",
    width=900,
    height=600
)

st.plotly_chart(fig, use_container_width=True)
