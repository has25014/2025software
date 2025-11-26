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
CSS = """
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
    }
    .logo-mark span{
        position:relative;
        font-weight:700;
        font-size: 18px;
        letter-spacing:1px;
        color:#e5e7eb;
    }
    .logo-title h1 {
        font-size: 22px;
        font-weight: 700;
        letter-spacing: 0.04em;
        margin: 0;
    }
    .logo-title p {
        font-size: 12px;
        color: #9ca3af;
        margin: 2px 0 0 0;
    }
    .pill {
        font-size: 11px;
        color:#9ca3af;
        padding:6px 12px;
        border-radius:999px;
        border:1px solid rgba(148,163,184,.5);
        background:rgba(15,23,42,.8);
        display:flex;
        align-items:center;
        gap:6px;
        backdrop-filter:blur(8px);
    }
    .pill-dot{
        width:7px;height:7px;border-radius:999px;
        background:#4ade80;box-shadow:0 0 8px #22c55e;
    }
    .risk-score {
        font-size: 28px;
        font-weight: 700;
        letter-spacing: 0.06em;
        margin-bottom: 2px;
    }
    .risk-label {
        font-size: 14px;
        font-weight: 500;
        margin-bottom: 4px;
    }
    .risk-msg {
        font-size: 13px;
        font-weight: 500;
        margin-bottom: 8px;
    }
    .risk-bar {
        position: relative;
        height: 10px;
        border-radius: 999px;
        background: linear-gradient(90deg,#22c55e,#facc15,#f97373);
        opacity: 0.9;
        overflow: hidden;
        margin-bottom: 10px;
    }
    .risk-cursor {
        position:absolute;
        top:50%;
        width:4px;
        height:18px;
        border-radius:999px;
        background:#e5e7eb;
        transform:translate(-50%,-50%);
        box-shadow:0 0 12px rgba(255,255,255,.9);
    }
    .chip-row {
        display:flex;
        flex-wrap:wrap;
        gap:6px;
        margin: 4px 0 10px 0;
    }
    .chip {
        font-size:11px;
        padding:5px 9px;
        border-radius:999px;
        border:1px solid rgba(148,163,184,.35);
        background:rgba(15,23,42,.9);
        color:#9ca3af;
    }
    .chip strong {
        color:#e5e7eb;
        font-weight:500;
    }
    .risk-badge {
        display:inline-flex;
        align-items:center;
        gap:6px;
        border-radius:999px;
        padding:3px 10px;
        font-size:11px;
        background:rgba(15,23,42,.92);
        border:1px solid rgba(148,163,184,.45);
        margin-bottom:8px;
    }
    .risk-dot {
        width:9px;
        height:9px;
        border-radius:999px;
        box-shadow:0 0 10px;
    }
    .risk-dot.safe { background:#22c55e; }
    .risk-dot.warn { background:#facc15; }
    .risk-dot.danger { background:#f97373; }
    .small-label {
        font-size:11px;
        color:#9ca3af;
        margin-bottom:4px;
    }
    .contact-box {
        font-size:11px;
        padding:9px 11px;
        border-radius:12px;
        border:1px dashed rgba(148,163,184,.7);
        background:rgba(15,23,42,.88);
    }
    @media (max-width: 768px) {
        .header-row {
            flex-direction: column;
            align-items: flex-start;
        }
    }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ----------------------------------------
# 헤더
# ----------------------------------------
st.markdown(
    """
<div class="header-row">
  <div class="logo-wrap">
    <div class="logo-mark"><span>K</span></div>
    <div class="logo-title">
      <h1>깡통체크</h1>
      <p>전·월세 보증금 위험도 스캔 & 초보 세입자 가이드</p>
    </div>
  </div>
  <div class="pill">
    <span class="pill-dot"></span>
    <span>내 집을 처음 구하는 세입자를 위한 안전 매니저</span>
  </div>
</div>
""",
    unsafe_allow_html=True,
)
st.caption("※ 실제 부동산·법률 서비스를 대신하지 않으며, 전세사기를 예방하기 위한 교육용 프로토타입입니다.")
st.write("")

# ----------------------------------------
# 위험도 계산 함수
# ----------------------------------------
def compute_risk_score(deposit, rent, contract_type, memo: str = ""):
    """
    보증금이 클수록, 전세에 가까울수록 위험도가 높다고 가정한 간단 모형 +
    메모에 곰팡이/누수/하자/귀신 등 안 좋은 요소가 있으면 가산점.
    """
    if deposit <= 0:
        return 0, []

    base = 40
    # 보증금 크기
    if deposit < 2000:
        base += 0
    elif deposit < 5000:
        base += 15
    elif deposit < 8000:
        base += 30
    else:
        base += 45

    # 계약 형태
    if contract_type == "전세":
        base += 10
    elif contract_type == "반전세":
        base += 5

    # 월세 거의 없으면(전세에 가까움) 약간 가산
    if rent <= 5:
        base += 5

    # 메모 내용 반영
    memo = (memo or "").strip()
    memo_issues = []
    if memo:
        text = memo.lower()
        issue_keywords = {
            "곰팡": (10, "곰팡이"),
            "누수": (10, "누수"),
            "하자": (6, "하자"),
            "악취": (6, "악취"),
            "냄새": (4, "냄새"),
            "소음": (6, "소음"),
            "층간소음": (6, "층간소음"),
            "벌레": (6, "벌레"),
            "바퀴벌레": (8, "벌레"),
            "누전": (10, "전기·누전"),
            "벽균열": (6, "벽 균열"),
            "균열": (4, "균열"),
            "귀신": (3, "이상한 소문"),
        }
        for key, (weight, label) in issue_keywords.items():
            if key in memo:
                base += weight
                memo_issues.append(label)

    base = max(0, min(100, base))
    memo_issues = sorted(set(memo_issues))
    return base, memo_issues


def risk_color_and_label(score: int):
    """
    점수에 따라:
      - 레벨
      - 색상 클래스
      - 설명
      - 바 위치
      - 짧은 멘트
    """
    if score < 45:
        level = "안전"
        color_class = "safe"
        caption = (
            "전세가율이 비교적 낮고, 보증보험·대출 조건도 무난할 가능성이 높습니다. "
            "그래도 등기부등본과 계약서 특약을 끝까지 확인하는 것이 좋습니다."
        )
        pos = 20
        msg = "😊 이 집은 비교적 안전해 보여요. 그래도 체크리스트 한 번씩은 꼭 확인해요!"
    elif score < 70:
        level = "보통 (주의 필요)"
        color_class = "warn"
        caption = (
            "시세 대비 보증금이 다소 높거나, 계약 형태상 세입자에게 불리한 조건이 섞여 있을 수 있습니다. "
            "보증금을 조정하거나, 다른 매물과 비교해 보는 것이 좋습니다."
        )
        pos = 55
        msg = "😐 조건이 살짝 애매해요. 다른 집과 비교하면서 한 번 더 고민해 보세요."
    else:
        level = "경고 (고위험)"
        color_class = "danger"
        caption = (
            "전세가율이 매우 높거나, 등기부등본 상 권리가 복잡할 가능성이 있습니다. "
            "전문가 상담 없이 계약을 진행하는 것은 매우 위험합니다."
        )
        pos = 82
        msg = "🚨 헉, 얼른 다른 집도 같이 알아보세요! 전문가 상담 없이는 계약하면 안 돼요."

    return level, color_class, caption, pos, msg


# ----------------------------------------
# 주변 교통 요약 (예시용 함수)
# ----------------------------------------
def get_transit_summary_text(address: str) -> str:
    """실제 서비스라면 지도 API로 계산, 여기서는 주소 키워드 기반 예시 텍스트."""
    addr = (address or "").strip()
    if not addr:
        return ""

    lines = []
    # 지역별 예시
    lower = addr.lower()

    if "은평" in addr:
        lines.append("**예시) 서울 은평구 기준**")
        lines.append("- 지하철: 3호선 구파발역 도보 7분 거리 (예시)")
        lines.append("- 버스: 통일로 ○○ 정류장 도보 3분, 시내·광역버스 다수 (예시)")
        lines.append("- 도로: 내부순환로·통일로 진입이 가까워 자가용 이동이 편리한 편 (예시)")
    elif "강남" in addr or "서초" in addr:
        lines.append("**예시) 강남권 기준**")
        lines.append("- 지하철: 2호선/신분당선 환승역까지 도보 5~10분 (예시)")
        lines.append("- 버스: 간선·광역버스가 매우 많고 심야버스도 운행 (예시)")
        lines.append("- 도로: 경부고속도로·올림픽대로 진입이 쉬워 차량 이동도 편리 (예시)")
    elif "대전" in addr:
        lines.append("**예시) 대전시 기준**")
        lines.append("- 철도: 대전역/서대전역까지 시내버스로 15~25분 (예시)")
        lines.append("- 버스: 광역시 버스 노선이 많아 환승이 편리 (예시)")
        lines.append("- 도로: 경부고속도로·호남고속도로 IC 접근성이 보통 이상 (예시)")
    else:
        lines.append(f"**입력한 주소 기준 주변 교통 정보 (예시)**")
        lines.append("- 지하철/기차역: 실제 서비스에서는 지도 API를 통해 가장 가까운 역과 도보 시간을 계산합니다.")
        lines.append("- 버스 정류장: 반경 300m 이내 버스 정류장과 주요 노선을 자동으로 정리합니다.")
        lines.append("- 주요 도로/고속도로: 가까운 IC, 간선도로 접근성을 요약해서 보여줍니다.")

    lines.append("")
    lines.append("※ 현재 버전은 시연용으로, 실제 교통 정보가 아닌 **구조만 보여주는 예시**입니다.")
    return "\n".join(lines)


# ----------------------------------------
# 상단: 입력 + 결과
# ----------------------------------------
col_input, col_result = st.columns([1.15, 1])

with col_input:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("보증금 스캔 입력")
    st.markdown(
        "<p style='font-size:12px;color:#9ca3af;'>주소와 계약 조건, 집 상태 메모, 등기부등본을 입력하면, 전·월세 보증금이 어느 정도 위험한지 한 번에 확인할 수 있습니다.</p>",
        unsafe_allow_html=True,
    )

    address = st.text_input(
        "집 주소",
        placeholder="예) 서울시 ○○구 ○○로 123, 302호",
        key="main_address",
    )

    c1, c2 = st.columns(2)
    with c1:
        deposit = st.number_input(
            "보증금 (만원)",
            min_value=0,
            step=100,
            key="main_deposit",
        )
    with c2:
        rent = st.number_input(
            "월세 (만원)",
            min_value=0,
            step=5,
            key="main_rent",
        )

    c3, c4 = st.columns(2)
    with c3:
        contract_type = st.selectbox(
            "계약 형태",
            ["전세", "반전세", "월세"],
            key="main_contract_type",
        )
    with c4:
        tenant_type = st.selectbox(
            "세입자 유형",
            ["학생·청년", "1인 가구", "가족 세대", "외국인 세입자"],
            key="main_tenant_type",
        )

    memo = st.text_area(
        "메모 (선택)",
        placeholder="예) 벽에 곰팡이가 조금 있음, 천장에서 누수 자국, 옆집 소음 심함, 귀신 나온다는 소문 있음 등",
        height=80,
        key="main_memo",
    )

    st.markdown(
        "<p style='font-size:11px;color:#6b7280;'>※ 메모에 적은 곰팡이·누수·소음·귀신 소문 같은 요소도 위험도 계산에 반영됩니다.</p>",
        unsafe_allow_html=True,
    )

    # 등기부등본 업로드
    reg_file = st.file_uploader(
        "등기부등본 사진 또는 PDF 업로드 (선택)",
        type=["png", "jpg", "jpeg", "pdf"],
        key="main_reg_file",
        help="실제 서비스라면 등기부를 자동 인식하여 소유자·근저당·가압류 등을 분석합니다.",
    )

    scan_clicked = st.button("위험도 스캔하기", key="main_scan_btn")
    st.markdown("</div>", unsafe_allow_html=True)

with col_result:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("현재 조건 기준 위험도 요약")

    if scan_clicked and deposit > 0:
        score, memo_issues = compute_risk_score(deposit, rent, contract_type, memo)
    elif deposit > 0:
        score, memo_issues = compute_risk_score(deposit, rent, contract_type, memo)
    else:
        score = None
        memo_issues = []

    if score is None:
        st.markdown(
            """
            <div class="risk-badge">
              <div class="risk-dot warn"></div>
              <span>아직 스캔 전입니다</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("<div class='risk-score'>-- / 100점</div>", unsafe_allow_html=True)
        st.markdown("<div class='risk-label'>전·월세 위험도 미계산</div>", unsafe_allow_html=True)
        st.markdown(
            "<div class='risk-bar'><div class='risk-cursor' style='left:10%;'></div></div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<p style='font-size:11px;color:#9ca3af;'>왼쪽에 조건을 입력하고 <strong>위험도 스캔하기</strong> 버튼을 누르면 여기에서 결과가 표시됩니다.</p>",
            unsafe_allow_html=True,
        )
        st.markdown("<p class='small-label'>핵심 요약 지표</p>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class="chip-row">
              <span class="chip"><strong>전세가율</strong> -</span>
              <span class="chip"><strong>보증보험</strong> -</span>
              <span class="chip"><strong>등기부 위험요소</strong> -</span>
              <span class="chip"><strong>내부 상태</strong> -</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        level, color_class, caption, pos, msg = risk_color_and_label(score)
        st.markdown(
            f"""
            <div class="risk-badge">
              <div class="risk-dot {color_class}"></div>
              <span>현재 조건 기준 위험도 분석 완료</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(f"<div class='risk-score'>{score} / 100점</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='risk-label'>전·월세 위험 수준: {level}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='risk-msg'>{msg}</div>", unsafe_allow_html=True)
        st.markdown(
            f"<div class='risk-bar'><div class='risk-cursor' style='left:{pos}%;'></div></div>",
            unsafe_allow_html=True,
        )

        extra_caption = caption
        if memo_issues:
            joined = "·".join(memo_issues)
            extra_caption += f" 또한 메모에 적어 둔 **{joined}** 등의 내부 하자/위험 요소도 점수에 반영되었습니다."
        st.markdown(
            f"<p style='font-size:11px;color:#9ca3af;'>{extra_caption}</p>",
            unsafe_allow_html=True,
        )

        st.markdown("<p class='small-label'>핵심 요약 지표</p>", unsafe_allow_html=True)
        est_ratio = min(110, score + 5)

        if memo_issues:
            internal_chip = f"<span class='chip'><strong>내부 상태</strong> { '·'.join(memo_issues) } 위험 요소 감지</span>"
        else:
            internal_chip = "<span class='chip'><strong>내부 상태</strong> 특이사항 없음</span>"

        st.markdown(
            f"""
            <div class="chip-row">
              <span class="chip"><strong>전세가율</strong> 약 {est_ratio}% (추정)</span>
              <span class="chip"><strong>보증보험</strong> 가입 {'필수 권장' if score >= 70 else '권장'}</span>
              <span class="chip"><strong>등기부 위험요소</strong> {'상세 확인 필요' if score >= 45 else '특이사항 가능성 낮음'}</span>
              {internal_chip}
            </div>
            """,
            unsafe_allow_html=True,
        )

    # 주변 교통 요약 (주소 기반 예시)
    if address and address.strip():
        st.markdown("---")
        st.markdown("#### 주변 교통 요약 (예시)")
        transit_md = get_transit_summary_text(address)
        st.markdown(transit_md)

    # 등기부등본 자동 해석(예시)
    st.markdown("---")
    st.markdown("#### 등기부등본 자동 해석 (예시)")

    if reg_file is not None:
        if reg_file.type in ["image/png", "image/jpeg", "image/jpg"]:
            st.image(reg_file, caption="업로드한 등기부등본 (일부 화면 예시)", use_column_width=True)
        else:
            st.caption("PDF 형식의 등기부등본이 업로드되었습니다. (시연용이므로 내용은 실제로 분석되지 않습니다.)")

        st.markdown(
            """
- ※ 현재 버전은 데모로, 등기부의 실제 내용을 읽어들이지는 않습니다.  
- 실제 서비스라면 다음과 같은 정보를 자동으로 뽑아서 보여줍니다.

1. **소유자 정보**: 등기부 상 소유자 이름, 공유 지분 여부  
2. **근저당권**: 은행명, 채권최고액, 설정일, 순위  
3. **가압류·가처분**: 채권자, 금액, 설정일  
4. **세입자 입장에서 핵심 포인트**
   - 선순위 근저당 채권최고액 합계가 시세에 비해 너무 크지 않은지  
   - 가압류·가처분이 여러 건 잡혀 있지는 않은지  
   - 전입·확정일자를 언제 받아야 가장 안전한지  
            """
        )
    else:
        st.caption("왼쪽에서 등기부등본 이미지를 업로드하면, 이 자리에서 권리관계를 요약해서 보여주는 화면입니다. (현재는 시연용 텍스트만 표시)")

    st.markdown(
        """
        <div class="contact-box">
          <strong>※ 실제 문제가 의심되나요?</strong><br>
          깡통체크는 전·월세 사기 가능성을 미리 생각해 보는 교육용 도구이며,<br>
          실제 법률 자문·신고 절차는 한국법률구조공단, 주택도시보증공사(HUG), 지자체 주거 상담 창구 등과 반드시 상의해야 합니다.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------
# 추가 탭들
# ----------------------------------------
st.write("")
st.markdown("### 추가 기능 · 세부 화면")

tab_analysis, tab_checklist, tab_after, tab_share, tab_sim = st.tabs(
    ["상세 분석", "계약 전 체크리스트", "분쟁 발생 시 대응", "가족·공동세입자 공유", "조건 시뮬레이션"]
)

with tab_analysis:
    st.markdown(
        """
        #### 📊 상세 분석 (전세가율 + 등기부 해석 + 보증보험)
        - **전세가율**: 주변 비슷한 매물의 매매가와 비교해, 보증금이 얼마나 높은지 비율로 표시한다고 가정합니다.  
        - **등기부등본 위험요소**: 근저당·가압류·가처분 등 권리가 많은 집일수록 세입자가 마지막에 보증금을 돌려받기 어려워질 수 있습니다.  
        - **보증보험 가능 여부**: 주택도시보증공사(HUG) 보증보험 가입이 가능한지, 예상 보험료는 얼마인지 안내합니다.
        """
    )
    easy_mode = st.checkbox("어려운 용어를 쉬운 말로 보기", value=True, key="analysis_easy_mode")
    if easy_mode:
        st.info(
            "👉 **쉬운 말 버전**\n\n"
            "- 전세가율이 높다 = 집 값 거의 대부분을 내가 떠안고 있는 구조라, 집값이 떨어지면 내가 손해를 볼 수 있다는 뜻이에요.\n"
            "- 등기부에 근저당이 많다 = 집이 이미 여러 군데에 담보로 잡혀 있어서, 문제가 생기면 세입자에게 돈이 마지막에 돌아올 수 있어요.\n"
            "- 보증보험 = 보증금을 못 돌려받는 상황이 생겼을 때, 대신 돈을 돌려받을 수 있게 도와주는 보험이에요."
        )
    else:
        st.info(
            "👉 **법률 용어 포함 버전**\n\n"
            "- 전세가율 = 전세보증금 ÷ 시세(매매가). 보통 80%를 넘으면 위험 신호로 보기도 합니다.\n"
            "- 근저당·가압류·가처분은 집에 설정된 권리로, 선순위 권리자가 먼저 보상을 받고 세입자는 뒤로 밀릴 수 있습니다.\n"
            "- 전세보증보험은 임대인이 보증금을 반환하지 못할 경우 보증기관이 대신 지급하는 제도입니다."
        )

with tab_checklist:
    st.markdown("#### ✅ 계약 전 체크리스트 (집 보기 전에 꼭 확인할 것들)")
    st.markdown(
        """
        **1. 기본 정보·법적 사항**
        - 등기부등본으로 **집주인 실명**과 소유자, 계약서 상 임대인이 같은 사람인지 확인하기  
        - 근저당, 가압류, 가처분 등 권리가 과도하게 잡혀 있지 않은지 확인하기  
        - 임대인이 개인인지, 법인·회사인지 구분하고, 법인인 경우 회사 존속 상태 확인하기  
        - 중개업소가 **정식 등록된 공인중개사무소**인지(등록번호, 명함, 자격증 비치 여부) 확인하기  

        **2. 돈과 계약 조건**
        - 주변 시세(매매가·전세가)와 비교해 **전세가율**이 너무 높지 않은지 확인하기  
        - 관리비 구조, 공용전기·수도·난방 등 **관리비 폭탄**이 나오지 않을지 꼼꼼히 물어보기  
        - 보증금 반환 책임, 하자 발생 시 수리 주체, 중도 해지 시 위약금 등을 **특약**으로 계약서에 명시하기  
        - 전세보증보험 가입 가능 여부, 보험료, 누가 부담하는지(임대인/임차인) 미리 협의하기  

        **3. 집 내부 상태(곰팡이·누수·하자 등)**
        - 벽·천장·창틀 주변에 **곰팡이, 누수 자국, 누런 얼룩**이 없는지 자세히 보기  
        - 창문·현관문이 잘 닫히는지, 바닥이 울렁거리지는 않는지, 벽에 **균열**은 없는지 확인하기  
        - 전기 콘센트, 배선, 두꺼비집 등에서 **타는 냄새·열감**이 느껴지지 않는지 확인하기  
        - 화장실·배수구 냄새, 하수구 역류 여부 등 **악취** 문제는 없는지 체크하기  
        - 겨울철 결로가 심할 것 같은 구조(북향·환기 안 됨 등)인지, 창문 주변에 곰팡이 흔적이 없는지 살펴보기  

        **4. 주변 환경과 생활 편의**
        - 낮/밤에 다시 가서 **소음(층간소음, 도로 소음, 술집 소리)** 정도 확인하기  
        - 치안, CCTV, 가로등, 골목 분위기 등 **야간 안전** 살펴보기  
        - 엘리베이터, 주차장, 분리수거 장소, 우편함 등 공용 시설 상태도 함께 확인하기  
        - 편의점, 마트, 병원, 학교, 카페 등 일상 생활에 필요한 시설이 너무 멀지 않은지 체크하기  

        **5. 이사·전입신고 계획**
        - 계약 후 언제 **전입신고 + 확정일자**를 받을 수 있는지, 이사 날짜와 함께 미리 계산하기  
        - 기존 세입자가 언제 정확히 나가는지, 공실 기간이 겹치지 않는지 확인하기  
        - 전입신고를 어디서 할지(주민센터 위치), 확정일자는 어떻게 받는지
