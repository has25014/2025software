import streamlit as st

# ---------------------------------------------------------
# 기본 설정
# ---------------------------------------------------------
st.set_page_config(
    page_title="보증가드 | 전·월세 보증금 위험도 스캔",
    page_icon="🏠",
    layout="wide",
)

# ---------------------------------------------------------
# 간단한 스타일 커스터마이징 (배경/카드 디자인)
# ---------------------------------------------------------
CUSTOM_CSS = """
<style>
    /* 전체 배경 */
    .stApp {
        background: radial-gradient(circle at top, #1f2937 0, #020617 55%, #020617 100%);
        color: #e5e7eb;
        font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",system-ui,sans-serif;
    }
    /* 카드처럼 보이는 컨테이너용 */
    .card {
        background: radial-gradient(circle at top left,#111827 0,#020617 55%,#020617 100%);
        border-radius: 18px;
        border: 1px solid rgba(148,163,184,0.28);
        box-shadow: 0 18px 42px rgba(15,23,42,0.8);
        padding: 18px 20px 20px;
    }
    /* 상단 라인 */
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

    /* 위험도 점수 스타일 */
    .risk-score {
        font-size: 32px;
        font-weight: 700;
        letter-spacing: 0.08em;
        margin-bottom: 4px;
    }
    .risk-label {
        font-size: 14px;
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
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------
# 세션 상태 기본값 세팅 (샘플 버튼용)
# ---------------------------------------------------------
default_sample = {
    "address": "서울시 ○○구 ○○로 123, 302호",
    "deposit": 5000,
    "rent": 40,
    "contract_type": "반전세",
    "tenant_type": "학생·청년",
    "memo": "부동산에서 신축이라고 설명했지만, 주변 시세보다 약간 비싼 편이라고 함."
}

for key, val in default_sample.items():
    st.session_state.setdefault(key, "" if key in ["address", "memo"] else 0)

# ---------------------------------------------------------
# 상단 헤더
# ---------------------------------------------------------
st.markdown(
    """
<div class="header-row">
  <div class="logo-wrap">
    <div class="logo-mark"><span>D</span></div>
    <div class="logo-title">
      <h1>보증가드</h1>
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

st.write("")  # 여백

# ---------------------------------------------------------
# 위험도 계산 함수 (간단한 모형)
# ---------------------------------------------------------
def compute_risk_score(deposit, rent, contract_type):
    """
    실제 데이터가 아니라, '보증금이 높을수록/전세에 가까울수록 위험도가 높다'는
    단순한 가정으로 점수를 만들어주는 함수.
    """
    if deposit <= 0:
        return 0

    base = 40  # 기본 점수
    # 보증금 크기에 따른 가산
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

    # 월세가 거의 없는 경우(전세에 가까움) 조금 더 위험하다고 가정
    if rent <= 5:
        base += 5

    # 점수 범위 (0~100)
    return max(0, min(100, base))


def risk_color_and_label(score: int):
    """점수에 따라 색/라벨/설명 텍스트를 나누는 함수"""
    if score < 45:
        level = "비교적 안전"
        color_class = "safe"
        caption = (
            "전세가율이 비교적 낮고, 보증보험·대출 조건도 무난할 가능성이 높습니다. "
            "그래도 등기부등본과 계약서 특약을 끝까지 확인하는 것이 좋습니다."
        )
        pos = 20
    elif score < 70:
        level = "주의 필요"
        color_class = "warn"
        caption = (
            "시세 대비 보증금이 다소 높거나, 계약 형태상 세입자에게 불리한 조건이 섞여 있을 수 있습니다. "
            "보증금을 조정하거나, 다른 매물과 비교해 보는 것이 좋습니다."
        )
        pos = 55
    else:
        level = "고위험 (깡통 전세 주의)"
        color_class = "danger"
        caption = (
            "전세가율이 매우 높거나, 등기부등본 상 권리가 복잡할 가능성이 있습니다. "
            "전문가 상담 없이 계약을 진행하는 것은 매우 위험합니다."
        )
        pos = 82
    return level, color_class, caption, pos


# ---------------------------------------------------------
# 상단: 입력 영역 + 결과 영역 (두 컬럼)
# ---------------------------------------------------------
col_input, col_result = st.columns([1.15, 1])

with col_input:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("보증금 스캔 입력")
    st.markdown(
        "<p style='font-size:12px;color:#9ca3af;'>"
        "주소와 계약 조건을 입력하면, 전·월세 보증금이 어느 정도 위험한지 한 번에 확인할 수 있습니다."
        "</p>",
        unsafe_allow_html=True,
    )

    # 샘플 불러오기 버튼
    if st.button("샘플 매물 불러오기"):
        for key, val in default_sample.items():
            st.session_state[key] = val
        st.experimental_rerun()

    # 입력 폼
    address = st.text_input("집 주소", key="address", placeholder="예) 서울시 ○○구 ○○로 123, 302호")
    c1, c2 = st.columns(2)
    with c1:
        deposit = st.number_input("보증금 (만원)", key="deposit", min_value=0, step=100)
    with c2:
        rent = st.number_input("월세 (만원)", key="rent", min_value=0, step=5)

    c3, c4 = st.columns(2)
    with c3:
        contract_type = st.selectbox("계약 형태", ["전세", "반전세", "월세"], key="contract_type")
    with c4:
        tenant_type = st.selectbox(
            "세입자 유형",
            ["학생·청년", "1인 가구", "가족 세대", "외국인 세입자"],
            key="tenant_type",
        )

    memo = st.text_area(
        "메모 (선택)",
        key="memo",
        placeholder="부동산에서 들은 조건이나 특이사항을 간단히 적어 두세요.",
        height=60,
    )

    st.markdown(
        "<p style='font-size:11px;color:#6b7280;'>※ 실제 시세·등기 데이터와 연동된다고 가정한 디자인/동작 예시입니다.</p>",
        unsafe_allow_html=True,
    )

    scan_clicked = st.button("위험도 스캔하기", type="primary")

    st.markdown("</div>", unsafe_allow_html=True)

with col_result:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("현재 조건 기준 위험도 요약")

    if scan_clicked and deposit > 0:
        score = compute_risk_score(deposit, rent, contract_type)
    elif deposit > 0:
        # 처음 로드할 때도 값이 있으면 자동 계산
        score = compute_risk_score(deposit, rent, contract_type)
    else:
        score = None

    if score is None:
        # 아직 스캔 안 했을 때
        st.markdown(
            """
            <div class="risk-badge">
              <div class="risk-dot warn"></div>
              <span>아직 스캔 전입니다</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('<div class="risk-score">--점</div>', unsafe_allow_html=True)
        st.markdown('<div class="risk-label">전·월세 위험도 미계산</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="risk-bar"><div class="risk-cursor" style="left:10%;"></div></div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            "<p style='font-size:11px;color:#9ca3af;'>왼쪽에 조건을 입력하고 "
            "<strong>위험도 스캔하기</strong> 버튼을 누르면 여기에 깡통 전세 및 보증금 회수 위험도가 표시됩니다.</p>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<p class='small-label'>핵심 요약 지표</p>", unsafe_allow_html=True
        )
        st.markdown(
            """
            <div class="chip-row">
              <span class="chip"><strong>전세가율</strong> -</span>
              <span class="chip"><strong>보증보험</strong> -</span>
              <span class="chip"><strong>등기부 위험요소</strong> -</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:
        # 점수 계산된 상태
        level, color_class, caption, pos = risk_color_and_label(score)

        st.markdown(
            f"""
            <div class="risk-badge">
              <div class="risk-dot {color_class}"></div>
              <span>현재 조건 기준 위험도 분석 완료</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(f"<div class='risk-score'>{score}점</div>", unsafe_allow_html=True)
        st.markdown(
            f"<div class='risk-label'>전·월세 위험도: {level}</div>", unsafe_allow_html=True
        )
        st.markdown(
            f"<div class='risk-bar'><div class='risk-cursor' style='left:{pos}%;'></div></div>",
            unsafe_allow_html=True,
        )

        st.markdown(
            f"<p style='font-size:11px;color:#9ca3af;'>{caption}</p>",
            unsafe_allow_html=True,
        )

        # 간단한 요약 지표 (모두 가짜값, 예시용)
        st.markdown("<p class='small-label'>핵심 요약 지표</p>", unsafe_allow_html=True)
        est_ratio = min(110, score + 5)
        st.markdown(
            f"""
            <div class="chip-row">
              <span class="chip"><strong>전세가율</strong> 약 {est_ratio}% (추정)</span>
              <span class="chip"><strong>보증보험</strong> 가입 {'필수 권장' if score >= 70 else '권장'}</span>
              <span class="chip"><strong>등기부 위험요소</strong> {'상세 확인 필요' if score >= 45 else '특이사항 가능성 낮음'}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # 항상 보여주는 안내 박스
    st.markdown(
        """
        <div class="contact-box">
          <strong>※ 실제 문제가 의심되나요?</strong><br>
          보증가드는 전·월세 사기 가능성을 미리 생각해 보는 교육용 도구이며,<br>
          실제 법률 자문·신고 절차는 한국법률구조공단, 주택도시보증공사(HUG), 지자체 상담 창구 등과 반드시 상의해야 합니다.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 추가 기능 섹션 (시뮬레이션, 체크리스트, 분쟁 대응, 공유 등)
# ---------------------------------------------------------

st.write("")
st.markdown("### 추가 기능 · 세부 화면")

# 탭 구성
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
    easy_mode = st.checkbox("어려운 용어를 쉬운 말로 보기", value=True)

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
    st.markdown("#### ✅ 계약 전 체크리스트")
    st.write("전·월세 계약을 하기 전에, 최소한 아래 단계는 꼭 확인한다고 가정합니다.")
    st.markdown(
        """
        1. **집주인 실명 확인**  
           - 등기부등본에 적힌 소유자 이름과, 계약서에 적힌 임대인 이름이 같은지 확인합니다.
        2. **전세가율 확인**  
           - 주변 시세(매매가)와 비교해 전세가율이 너무 높지 않은지 확인합니다.
        3. **전입신고·확정일자 가능일 계산**  
           - 계약 후 언제 전입신고와 확정일자를 받을 수 있는지, 이사 날짜와 함께 미리 계획합니다.
        4. **집 상태 점검**  
           - 누수, 곰팡이, 결로, 창문·문짝 상태, 전기·가스 안전 등을 직접 눈으로 확인합니다.
        5. **특약 사항 정리**  
           - 보일러·누수 등 하자가 생겼을 때 수리 책임이 누구에게 있는지, 문장으로 계약서에 남깁니다.
        """
    )

with tab_after:
    st.markdown("#### 🚨 분쟁 발생 시 대응 플로우")
    st.write("보증금 반환이 지연되거나, 명백한 전세사기가 의심될 때의 예시 플로우입니다.")
    st.markdown(
        """
        1. **증거 수집**  
           - 임대인과 주고받은 문자, 카카오톡, 계좌이체 내역, 계약서 원본 등을 안전한 곳에 백업합니다.
        2. **내용증명 발송**  
           - 보증금 반환 요청 내용증명을 우편으로 보내, 공식적으로 ‘요청했다’는 기록을 남깁니다.
        3. **상담 기관 문의**  
           - 한국법률구조공단, 주택도시보증공사(HUG) 등 공공기관에 상담을 신청합니다.
        4. **임차권 등기명령·소송 검토**  
           - 상황에 따라 임차권 등기명령, 강제집행, 손해배상 청구 등 법적 절차를 검토합니다.
        """
    )
    st.warning(
        "⚠️ 이 앱은 실제 법률 자문을 대신할 수 없습니다. "
        "실제 분쟁 상황에서는 반드시 변호사나 공공기관과 상담해야 합니다."
    )

with tab_share:
    st.markdown("#### 👪 가족·공동세입자와 함께 보는 화면")
    st.write("검토 중인 집 정보를 가족·룸메와 함께 보면서 의견을 나누는 상황을 가정한 디자인입니다.")

    # 간단한 댓글 시뮬레이션 (세션에 저장)
    if "comments" not in st.session_state:
        st.session_state["comments"] = [
            ("엄마", "보증금이 조금 높은 편이라, 월세를 조정하는 게 좋을 것 같아."),
            ("나린", "회사까지 20분이면 출퇴근은 괜찮을 듯! 대신 보증보험은 꼭 들어야겠어."),
            ("룸메", "층간소음이 심한지 실제로 가서 한 번 들어보고 결정하자."),
        ]

    for who, text in st.session_state["comments"]:
        st.markdown(f"**{who}** : {text}")

    st.write("---")
    st.write("✏️ 여기서 예시로 의견을 하나 더 적어볼 수 있어요. (실제 저장이 중요한 건 아니고, UX 느낌만 보여 주는 용도)")
    new_who = st.text_input("이름", value="", key="new_who")
    new_text = st.text_input("의견", value="", key="new_text")
    if st.button("의견 추가(예시)"):
        if new_who.strip() and new_text.strip():
            st.session_state["comments"].append((new_who.strip(), new_text.strip()))
            st.experimental_rerun()
        else:
            st.info("이름과 의견을 모두 입력해 주세요.")

with tab_sim:
    st.markdown("#### 🔍 조건 시뮬레이션")
    st.write("보증금·월세를 바꿔 보면서, 위험도 점수가 어떻게 달라지는지 가볍게 살펴볼 수 있는 영역입니다.")
    sim_col1, sim_col2 = st.columns(2)

    with sim_col1:
        sim_deposit = st.slider("가상의 보증금 (만원)", min_value=500, max_value=10000, step=500, value=default_sample["deposit"])
        sim_rent = st.slider("가상의 월세 (만원)", min_value=0, max_value=100, step=5, value=default_sample["rent"])
        sim_type = st.selectbox("가상의 계약 형태", ["전세", "반전세", "월세"], index=1)

    with sim_col2:
        sim_score = compute_risk_score(sim_deposit, sim_rent, sim_type)
        sim_level, sim_color, sim_caption, sim_pos = risk_color_and_label(sim_score)

        st.markdown(f"**시뮬레이션 점수: {sim_score}점 · {sim_level}**")
        st.progress(sim_score / 100.0)
        st.markdown(
            f"> 보증금을 `{sim_deposit}만 원`, 월세를 `{sim_rent}만 원`, "
            f"계약 형태를 `{sim_type}`으로 가정했을 때의 위험도입니다."
        )
        st.caption(sim_caption)

st.write("")
st.caption("© 2025 보증가드(가상 서비스) · 전세사기 예방 교육용 프로토타입")
