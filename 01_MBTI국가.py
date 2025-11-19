import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# -----------------------
# 기본 설정
# -----------------------
st.set_page_config(
    page_title="국가별 MBTI 대시보드",
    page_icon="🌍",
    layout="wide",
)

st.title("🌍 국가별 MBTI 분포 대시보드")
st.caption("국가를 선택하면 해당 국가의 MBTI 비율을 인터랙티브 그래프로 보여줄게요 😄")

# -----------------------
# 데이터 불러오기
# -----------------------
@st.cache_data
def load_data():
    # 같은 폴더에 있는 CSV 파일
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

df = load_data()

# 컬럼 분리
country_col = "Country"
mbti_cols = [c for c in df.columns if c != country_col]

# -----------------------
# 사이드바: 국가 선택
# -----------------------
st.sidebar.header("⚙️ 설정")
selected_country = st.sidebar.selectbox(
    "국가를 선택해 주세요:",
    sorted(df[country_col].unique())
)

st.sidebar.markdown("선택한 국가의 MBTI 분포를 아래 그래프로 확인해 보세요 👀")

# -----------------------
# 선택한 국가의 MBTI 분포 준비
# -----------------------
country_row = df[df[country_col] == selected_country].iloc[0]

mbti_values = country_row[mbti_cols]
mbti_df = (
    mbti_values
    .reset_index()
    .rename(columns={"index": "MBTI", 0: "Value"})
)

# 내림차순 정렬 (1등 찾기)
mbti_df = mbti_df.sort_values("Value", ascending=False).reset_index(drop=True)

# -----------------------
# 색상 설정: 1등은 빨간색, 나머지는 그라데이션
# -----------------------
n = len(mbti_df)

# 파란 계열 그라데이션 색상 생성
gradient_colors = px.colors.sample_colorscale(
    "Blues",
    [i / (n - 1) for i in range(n)]
)

colors = gradient_colors.copy()
# 1등 막대는 붉은색으로 강조
colors[0] = "#FF4B4B"

# -----------------------
# Plotly 그래프 생성
# -----------------------
fig = go.Figure(
    data=go.Bar(
        x=mbti_df["MBTI"],
        y=mbti_df["Value"],
        marker_color=colors,
        text=mbti_df["Value"].round(2),
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>값: %{y}<extra></extra>",
    )
)

fig.update_layout(
    title={
        "text": f"🇺🇳 {selected_country} 의 MBTI 분포",
        "x": 0.5,
        "xanchor": "center",
        "yanchor": "top",
    },
    xaxis_title="MBTI 유형",
    yaxis_title="값 (비율 또는 점수)",
    yaxis=dict(tickformat=".2f"),
    template="simple_white",
    margin=dict(l=40, r=40, t=80, b=40),
)

# -----------------------
# 화면에 출력
# -----------------------
st.plotly_chart(fig, use_container_width=True)

# -----------------------
# 부가 정보 텍스트
# -----------------------
top_type = mbti_df.iloc[0]["MBTI"]
top_value = mbti_df.iloc[0]["Value"]

st.markdown("---")
st.subheader("📌 요약 정보")

st.markdown(
    f"""
- 선택한 국가: **{selected_country}**
- 가장 비율이 높은 MBTI: **{top_type}** 🔴 (값: **{top_value:.2f}**)
- 나머지 유형들은 파란색 계열 그라데이션으로 표시했어요 💙  
- 막대 위 숫자와, 마우스를 올렸을 때 나오는 툴팁으로 값을 자세히 확인할 수 있어요!
"""
)

st.info("필요하면 나중에 I/E, N/S, F/T, J/P 축별로 합쳐서 비교하는 그래프도 추가해 볼 수 있어요 😊")
