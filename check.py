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
# 상단: 입력 + 결과
# ----------------------------------------
col_input, col_result = st.columns([1.15, 1])

with col_input:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("보증금 스캔 입력")
    st.markdown(
        "<p style='font-size:12px;color:#9ca3af;'>주소와 계약 조건, 집 상태 메모를 입력하면, 전·월세 보증금이 어느 정도 위험한지 한 번에 확인할 수 있습니다.</p>",
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
        - 중개업소가 **정식 등록된 공인중개사무소**인지(등록번호, 명함) 확인하기  

        **2. 돈과 계약 조건**
        - 주변 시세(매매가·전세가)와 비교해 **전세가율**이 너무 높지 않은지 확인하기  
        - 관리비 구조, 공용전기·수도·난방 등 **관리비 폭탄**이 나오지 않을지 물어보기  
        - 보증금 반환 책임, 하자 발생 시 수리 주체 등은 **특약**으로 계약서에 명시하기  

        **3. 집 내부 상태(곰팡이·누수·하자 등)**
        - 벽·천장·창틀 주변에 **곰팡이, 누수 자국, 누런 얼룩**이 없는지 자세히 보기  
        - 창문·현관문이 잘 닫히는지, 바닥이 울렁거리지는 않는지, 벽에 **균열**은 없는지 확인하기  
        - 전기 콘센트, 배선, 두꺼비집 등에서 **타는 냄새·열감**이 느껴지지 않는지 확인하기  
        - 화장실·배수구 냄새, 하수구 역류 여부 등 **악취** 문제는 없는지 체크하기  

        **4. 주변 환경과 생활 편의**
        - 낮/밤에 다시 가서 **소음(층간소음, 도로 소음, 술집 소리)** 정도 확인하기  
        - 치안, CCTV, 가로등, 골목 분위기 등 **야간 안전** 살펴보기  
        - 엘리베이터, 주차장, 분리수거 장소 등 공용 시설 상태도 함께 확인하기  

        **5. 이사·전입신고 계획**
        - 계약 후 언제 **전입신고 + 확정일자**를 받을 수 있는지, 이사 날짜와 함께 미리 계산하기  
        - 기존 세입자가 언제 정확히 나가는지, 공실 기간이 겹치지 않는지 확인하기  
        """
    )

with tab_after:
    st.markdown("#### 🚨 분쟁 발생 시 대응 플로우 & 신고처")
    st.markdown(
        """
        **1단계. 증거 싹 모으기**
        - 임대인과 주고받은 문자, 카카오톡, 전화 녹취, 계좌이체 내역, 계약서 원본 등  
          **모든 증거를 캡처·PDF로 백업**해 둡니다.

        **2단계. 내용증명 보내기**
        - “언제까지 보증금을 돌려달라”는 요구를 정리해서 **내용증명 우편**으로 발송합니다.  
        - 이때, 계약서 사본·계좌이체 내역 등도 함께 정리해 두면 이후 절차에 도움이 됩니다.

        **3단계. 공식 상담 기관 활용**
        - **한국법률구조공단**: 무료 또는 저렴한 비용으로 법률 상담, 소송 지원 여부 문의  
        - **주택도시보증공사(HUG)**: 전세보증보험 가입 여부, 보증금 반환 보증 청구 가능성 확인  
        - **지자체 주거복지센터·전월세 지원센터**: 지방자치단체에서 운영하는 전세피해 상담 창구 활용  

        **4단계. 신고·고소 검토 (사기 의심 시)**
        - 고의적인 전세사기(깡통전세, 갭투기 등)가 의심된다면  
          - **경찰(112는 긴급, 평시에는 관할 경찰서 민원실)** 에 사기 혐의로 신고/고소 상담  
          - 불법 중개가 의심되면 **관할 시·군·구청(부동산 담당 부서)** 또는  
            **국토교통부 전세사기·불법중개 신고센터**에 신고를 검토합니다.

        **5단계. 법적 절차 진행**
        - 상황에 따라 변호사·법률구조공단과 상의해  
          - **임차권 등기명령 신청** (집을 비워도 ‘대항력’과 ‘우선변제권’을 유지하기 위해)  
          - **보증금 반환 청구 소송**, **강제집행** 등 절차를 검토합니다.

        깡통체크는 이 과정을 “어떤 순서로 움직여야 하는지” 정리해 주는 역할이고,  
        실제 신고·소송은 반드시 전문가와 상의해야 합니다.
        """
    )

with tab_share:
    st.markdown("#### 👪 가족·공동세입자와 함께 보는 화면 (예시)")
    st.markdown("**엄마** : 보증금이 조금 높은 편이라, 월세를 조정하는 게 좋을 것 같아.")
    st.markdown("**나린** : 회사까지 20분이면 출퇴근은 괜찮을 듯! 대신 보증보험은 꼭 들어야겠어.")
    st.markdown("**룸메** : 층간소음이 심한지 실제로 가서 한 번 들어보고 결정하자.")

with tab_sim:
    st.markdown("#### 🔍 조건 시뮬레이션 (가상)")
    sim_col1, sim_col2 = st.columns(2)
    with sim_col1:
        sim_deposit = st.slider(
            "가상의 보증금 (만원)",
            500,
            10000,
            5000,
            500,
            key="sim_deposit",
        )
        sim_rent = st.slider(
            "가상의 월세 (만원)",
            0,
            100,
            40,
            5,
            key="sim_rent",
        )
        sim_type = st.selectbox(
            "가상의 계약 형태",
            ["전세", "반전세", "월세"],
            key="sim_contract_type",
        )
    with sim_col2:
        sim_score, _ = compute_risk_score(sim_deposit, sim_rent, sim_type, memo="")
        sim_level, _, sim_caption, _, _ = risk_color_and_label(sim_score)
        st.markdown(f"**시뮬레이션 점수: {sim_score} / 100점 · {sim_level}**")
        st.progress(sim_score / 100.0)
        st.markdown(
            f"> 보증금을 `{sim_deposit}만 원`, 월세를 `{sim_rent}만 원`, "
            f"계약 형태를 `{sim_type}`으로 가정했을 때의 위험도입니다."
        )
        st.caption(sim_caption)

st.write("")
st.caption("© 2025 깡통체크(가상 서비스) · 전세사기 예방 교육용 프로토타입")
