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
# CSS (간단 디자인)
# ----------------------------------------
CSS = (
    "<style>"
    "body, .stApp {"
    "  background-color: #020617;"
    "  color: #e5e7eb;"
    "  font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',system-ui,sans-serif;"
    "}"
    ".card {"
    "  background-color: #020617;"
    "  border-radius: 16px;"
    "  border: 1px solid #4b5563;"
    "  padding: 16px 18px;"
    "  box-shadow: 0 16px 40px rgba(0,0,0,0.65);"
    "}"
    ".title-main {font-size: 24px; font-weight: 700; margin-bottom: 4px;}"
    ".title-sub {font-size: 13px; color:#9ca3af;}"
    "</style>"
)
st.markdown(CSS, unsafe_allow_html=True)

# ----------------------------------------
# 위험도 계산 함수
# ----------------------------------------
def compute_risk_score(deposit, rent, contract_type, memo=""):
    """단순 점수 모델: 보증금·계약형태·메모(곰팡이, 누수 등) 반영."""
    if deposit <= 0:
        return 0, []

    score = 40

    # 보증금 크기
    if deposit < 2000:
        score += 0
    elif deposit < 5000:
        score += 15
    elif deposit < 8000:
        score += 30
    else:
        score += 45

    # 계약 형태
    if contract_type == "전세":
        score += 10
    elif contract_type == "반전세":
        score += 5

    # 월세 적으면 (전세에 가까우면) 살짝 가산
    if rent <= 5:
        score += 5

    # 메모에서 위험 키워드 감지
    issues = []
    memo = memo or ""
    keywords = {
        "곰팡": (10, "곰팡이"),
        "누수": (10, "누수"),
        "하자": (6, "하자"),
        "악취": (6, "악취"),
        "냄새": (4, "냄새"),
        "소음": (6, "소음"),
        "벌레": (6, "벌레"),
        "층간소음": (6, "층간소음"),
        "바퀴벌레": (8, "벌레"),
        "누전": (10, "전기·누전"),
        "균열": (4, "균열"),
        "벽균열": (6, "벽 균열"),
        "귀신": (3, "이상한 소문"),
    }
    for key, (w, name) in keywords.items():
        if key in memo:
            score += w
            issues.append(name)

    score = max(0, min(100, score))
    issues = sorted(set(issues))
    return score, issues


def risk_label(score):
    "
