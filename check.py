import streamlit as st
import pandas as pd
import urllib.parse
import streamlit.components.v1 as components

# ----------------------------------------
# Functions
# ----------------------------------------
def compute_risk_score(deposit, rent, contract_type, memo=""):
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
    # 월세 거의 없으면 (전세에 가까우면) 조금 더 위험
    if rent <= 5:
        score += 5
    # 메모 키워드
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
    if score < 45:
        level = "안전"
        msg = "😊 이 집은 비교적 안전해 보여요. 그래도 체크리스트는 꼭 한 번 확인해요!"
    elif score < 70:
        level = "보통 (주의)"
        msg = "😐 조건이 살짝 애매해요. 다른 집과 비교하면서 한 번 더 고민해 보세요."
    else:
        level = "경고 (고위험)"
        msg = "🚨 헉, 다른 집들도 같이 알아보는 게 좋아요. 전문가 상담 없이 계약하면 위험해요!"
    return level, msg


def get_transit_summary_text(address: str) -> str:
    addr = (address or "").strip()
    if not addr:
        return ""
    lines = []
    if "은평" in addr:
        lines.append("**예시) 서울 은평구 기준 주변 교통**")
        lines.append("- 지하철: 3호선 구파발역이 비교적 가까운 편입니다.")
        lines.append("- 버스: 통일로 주변으로 다양한 버스 노선이 있습니다.")
        lines.append("- 도로: 내부순환로·통일로 진입이 비교적 쉬운 편입니다.")
    elif ("강남" in addr) or ("서초" in addr):
        lines.append("**예시) 강남권 기준 주변 교통**")
        lines.append("- 지하철: 2호선/신분당선 환승역이 인근에 있을 가능성이 높습니다.")
        lines.append("- 버스: 간선·광역·심야버스가 많이 지나는 지역일 수 있어요.")
        lines.append("- 도로: 경부고속도로, 올림픽대로 등 주요 도로와의 접근성이 좋은 편일 수 있습니다.")
    else:
        lines.append("**입력한 주소 기준 주변 교통 안내 (개략)**")
        lines.append("- 실제 서비스에서는 지도 API로 가장 가까운 지하철역·버스정류장·고속도로 IC를 계산합니다.")
        lines.append("- 역까지 도보 시간, 버스 정류장까지 거리, 주요 도로 접근성 등을 숫자로 보여주는 것을 목표로 합니다.")
    return "\n".join(lines)


def get_lifestyle_comment(address: str, noise_sensitive: bool, hate_walking: bool, night_active: bool) -> str:
    addr = (address or "").strip()
    if not addr:
        return ""
    lines = []
    if noise_sensitive:
        if ("강남" in addr) or ("서초" in addr):
            lines.append("- 소음에 예민하다면, 강남권은 차량·버스·유동 인구가 많아서 밤에도 시끄러울 수 있어요.")
        elif "은평" in addr:
            lines.append("- 소음에 예민하다면, 통일로·내부순환로 차량 소음이 신경 쓰일 수 있어요.")
        else:
            lines.append("- 소음에 예민하다면, 큰 도로·역 바로 앞 매물은 한 번 더 야간 방문해보는 게 좋아요.")
    if hate_walking:
        if "은평" in addr:
            lines.append("- 걷는 걸 싫어한다면, 구파발역 도보 7분 정도도 조금 멀게 느껴질 수 있어요.")
        elif ("강남" in addr) or ("서초" in addr):
            lines.append("- 걷는 걸 싫어한다면, 환승통로가 긴 대형역 근처는 동선이 길게 느껴질 수 있어요.")
        else:
            lines.append("- 걷는 걸 싫어한다면, 지도에서 역·버스 정류장까지 도보 시간을 꼭 확인해 보세요.")
    if night_active:
        if ("강남" in addr) or ("서초" in addr):
            lines.append("- 야행성이라면, 강남권은 늦은 시간까지 편의시설은 많지만 그만큼 소음도 강할 수 있어요.")
        else:
            lines.append("- 야행성이라면, 늦게까지 여는 편의점·버스 노선 유무도 함께 확인해 보세요.")
    if not lines:
        return ""
    lines.insert(0, "**생활 패턴 기준 코멘트 (예시)**")
    return "\n".join(lines)


def get_poi_summary_text(address: str) -> str:
    """주소를 기반으로 주변 지하철/편의점/공원/큰 도로 정보를 요약(예시)"""
    addr = (address or "").strip()
    if not addr:
        return ""
    lines = []
    # 서울 마곡/서울식물원 근처 느낌
    if ("마곡" in addr) or ("서울식물원" in addr) or ("강서구" in addr):
        lines.append("**주변 편의·교통·공원 정보 (예시)**")
        lines.append("- 지하철: 마곡나루역·마곡역·양천향교역 중 한 곳이 도보/버스로 접근 가능한 생활권일 수 있어요.")
        lines.append("- 편의점: 마곡지구 내 GS25·CU·이마트24 등 편의점이 도보 3~5분 거리에 여러 곳 있을 가능성이 높아요.")
        lines.append("- 공원·녹지: 서울식물원, 한강 방화대교 주변 수변공원 등이 가깝다는 장점이 있어요.")
        lines.append("- 큰 도로·고속도로: 올림픽대로, 방화대교·가양대교 진입이 가까워 차량 이동은 편하지만, 교통량에 따른 소음은 체크가 필요해요.")
    # 은평/구파발/연신내 근처 느낌
    elif ("은평" in addr) or ("구파발" in addr) or ("연신내" in addr):
        lines.append("**주변 편의·교통·공원 정보 (예시)**")
        lines.append("- 지하철: 3호선 구파발역·연신내역 등으로 출퇴근하는 생활권일 가능성이 높아요.")
        lines.append("- 편의점: 역세권과 주거지 사이에 편의점·카페·프랜차이즈 음식점이 밀집된 구간이 많아요.")
        lines.append("- 공원·녹지: 북한산, 불광천 산책로 등 자연 접근성이 좋지만 산·하천 인접 여부에 따라 벌레·습도도 체크해야 해요.")
        lines.append("- 큰 도로·고속도로: 통일로, 내부순환로 진입이 가까워 차량 소음과 매연도 함께 확인해보는 게 좋아요.")
    # 강남/서초 근처 느낌
    elif ("강남" in addr) or ("서초" in addr):
        lines.append("**주변 편의·교통·공원 정보 (예시)**")
        lines.append("- 지하철: 2호선·3호선·9호선·신분당선 등 여러 노선을 환승할 수 있는 역세권일 가능성이 높아요.")
        lines.append("- 편의점: 블록마다 편의점·카페·프랜차이즈 음식점이 있을 정도로 생활 편의시설이 매우 풍부해요.")
        lines.append("- 공원·녹지: 양재천, 탄천, 역삼·서초 일대 소규모 공원 등 산책 코스를 찾기 괜찮은 편이에요.")
        lines.append("- 큰 도로·고속도로: 경부고속도로, 테헤란로, 남부순환로 등 대형 도로와 가깝다면 소음·매연이 강할 수 있어요.")
    # 그 외는 개략 예시
    else:
        lines.append("**주변 편의·교통·공원 정보 (개략 예시)**")
        lines.append("- 지하철/전철: 입력한 주소 주변의 가장 가까운 역까지 도보 시간·거리 정보를 지도 API로 계산해 보여줄 수 있어요.")
        lines.append("- 편의점: GS25·CU·세븐일레븐·이마트24 등까지 도보 2~5분 거리인지 확인해, 생활 편의성을 점수화할 수 있어요.")
        lines.append("- 공원·녹지: 동네 근린공원·하천 산책로·대형 공원(예: 서울숲, 서울식물원 등) 접근성을 함께 볼 수 있어요.")
        lines.append("- 큰 도로·고속도로: 왕복 4차로 이상 도로·고속도로 IC까지 거리를 기준으로, 소음·매연 리스크를 평가할 수 있어요.")
    lines.append("")
    lines.append("※ 실제 서비스에서는 지도·장소 API를 활용해 역/편의점/공원/고속도로까지의 실제 거리를 계산해 줄 수 있습니다.")
    return "\n".join(lines)


# ----------------------------------------
# Page config & title
# ----------------------------------------
st.set_page_config(
    page_title="깡통체크 | 전·월세 보증금 위험도 스캔",
    page_icon="🏠",
    layout="wide",
)

st.title("🛡️ 깡통체크")
st.caption("전·월세 보증금 위험도 스캔 & 초보 세입자 가이드 (교육용 데모)")
st.write("")

# ----------------------------------------
# 상단: 입력 + 결과
# ----------------------------------------
left_col, right_col = st.columns([1.1, 1])

with left_col:
    st.header("1. 기본 정보 입력")

    address = st.text_input("집 주소", placeholder="예) 서울시 ○○구 ○○로 123, 302호")

    c1, c2 = st.columns(2)
    with c1:
        deposit = st.number_input("보증금 (만원)", min_value=0, step=100)
    with c2:
        rent = st.number_input("월세 (만원)", min_value=0, step=5)

    c3, c4 = st.columns(2)
    with c3:
        contract_type = st.selectbox("계약 형태", ["전세", "반전세", "월세"])
    with c4:
        tenant_type = st.selectbox("세입자 유형", ["학생·청년", "1인 가구", "가족 세대", "외국인 세입자"])

    st.markdown("**생활 패턴 체크 (선택)**")
    noise_sensitive = st.checkbox("소음에 예민한 편이에요", value=False)
    hate_walking = st.checkbox("걷는 걸 별로 좋아하지 않아요 (역·버스는 최대한 가까웠으면 좋겠어요)", value=False)
    night_active = st.checkbox("야행성/늦게까지 깨어 있는 편이에요", value=False)

    memo = st.text_area(
        "집 상태 메모 (선택)",
        placeholder="예) 벽 곰팡이 조금, 천장 누수 자국, 옆집 소음 심함, 귀신 소문 있음 등",
        height=80,
    )

    st.caption("※ 메모에 적은 곰팡이·누수·소음·악취·벌레·귀신 소문 등도 위험도 계산에 반영됩니다.")

    reg_file = st.file_uploader(
        "등기부등본 이미지 또는 PDF (선택)",
        type=["png", "jpg", "jpeg", "pdf"],
        help="실제 서비스라면 등기부를 자동 인식해 소유자·근저당·가압류 등을 분석합니다.",
    )

    scan_clicked = st.button("위험도 스캔하기")

with right_col:
    st.header("2. 현재 조건 기준 위험도 요약")

    if scan_clicked and deposit > 0:
        score, memo_issues = compute_risk_score(deposit, rent, contract_type, memo)
    elif deposit > 0:
        score, memo_issues = compute_risk_score(deposit, rent, contract_type, memo)
    else:
        score, memo_issues = None, []

    if score is None:
        st.write("아직 스캔 전입니다. 왼쪽 정보를 입력하고 **'위험도 스캔하기'** 버튼을 눌러 주세요.")
        st.write("· 위험도 점수: -- / 100점")
        st.write("· 전·월세 위험 수준: -")
    else:
        level, msg = risk_label(score)
        st.markdown(f"**위험도 점수: {score} / 100점**")
        st.markdown(f"**전·월세 위험 수준: {level}**")
        st.write(msg)
        st.progress(score / 100.0)

        if memo_issues:
            st.write("메모에서 감지된 내부 위험 요소:", ", ".join(memo_issues))
        else:
            st.write("메모에서 특별한 위험 키워드는 감지되지 않았어요.")

    # --------- 주변 교통 + 실제 지도 + POI 요약 ---------
    st.subheader("주변 교통·지도·편의시설")

    if address:
        # 간단 교통 요약
        st.markdown(get_transit_summary_text(address))

        # 실제 지도 임베드 (Google Maps)
        encoded_addr = urllib.parse.quote(address)
        map_url = f"https://www.google.com/maps?q={encoded_addr}&output=embed"

        st.markdown("**아래 지도는 입력한 주소를 기준으로 한 실제 지도 화면입니다.**")
        components.iframe(map_url, height=400)

        # 생활 패턴 코멘트
        lifestyle_comment = get_lifestyle_comment(address, noise_sensitive, hate_walking, night_active)
        if lifestyle_comment:
            st.markdown(lifestyle_comment)

        # 주변 지하철/편의점/공원/큰 도로 요약
        poi_summary = get_poi_summary_text(address)
        if poi_summary:
            st.markdown(poi_summary)
    else:
        st.caption("주소를 입력하면, 해당 주소 기준 실제 지도와 주변 지하철·편의점·공원·큰 도로 정보를 요약해서 보여줍니다.")

    # --------- 등기부 해석 ---------
    st.subheader("등기부등본 자동 해석 (예시)")
    if reg_file is not None:
        if getattr(reg_file, "type", "").startswith("image/"):
            st.image(reg_file, caption="업로드한 등기부등본 (예시)", use_column_width=True)
        else:
            st.caption("PDF 형식 등기부가 업로드되었습니다. (데모 버전이라 실제 내용은 분석하지 않습니다.)")

        explain = (
            "- 현재 버전은 데모라 등기부 내용을 실제로 읽지는 않습니다.\n"
            "- 실제 서비스라면 다음 정보를 자동으로 뽑아서 보여줍니다:\n"
            "  - 소유자 이름, 공유 지분 여부\n"
            "  - 근저당권(은행명, 채권최고액, 설정일, 순위)\n"
            "  - 가압류·가처분 등 권리관계\n"
            "  - 세입자 입장에서 위험한 조합(선순위 근저당 과도, 다수의 가압류 등)"
        )
        st.markdown(explain)
    else:
        st.caption("등기부등본을 올리면 여기에서 권리관계 요약(예시)을 보여주는 화면입니다.")

    st.caption(
        "※ 깡통체크는 교육용 도구이며, 실제 법률 자문·신고는 "
        "한국법률구조공단·HUG·지자체 주거 상담 창구 등과 꼭 상의해야 합니다."
    )

# ----------------------------------------
# 하단 탭들
# ----------------------------------------
tab_check, tab_review, tab_after, tab_share, tab_sim = st.tabs(
    ["계약 전 체크리스트", "집 후기", "분쟁 발생 시 대응", "부모님과 결과 공유", "조건 시뮬레이션"]
)

# ---------------- 체크리스트 탭 ----------------
with tab_check:
    st.subheader("계약 전 체크리스트")
    st.caption(
        "집 보러 갈 때 휴대폰으로 열어두고 항목을 하나씩 체크해 보세요. "
        "체크 상태는 이 브라우저에서 앱을 사용하는 동안 유지됩니다."
    )
    warning_text = (
        "🚫 **이런 집은 웬만하면 절대 계약하지 마세요!**\n"
        "\n"
        "- 등기부에 적힌 소유자와 계약하자는 사람이 다른 경우\n"
        "- 등기부에 근저당이 집값(추정 매매가)에 거의 가까울 정도로 많이 잡혀 있는 경우\n"
        "- 집을 실제로 보여주지 않거나, 매우 짧게만 보여주고 계약을 서두르는 경우\n"
        "- 전입신고·확정일자·보증보험 가입을 막으려 하거나 필요 없다고 계속 우기는 경우\n"
        "- 오늘 안에 계약해야 한다면서 계약서 내용을 충분히 설명해 주지 않고 서명을 급하게 요구하는 경우\n"
    )
    st.warning(warning_text)

    col1, col2 = st.columns(2)

    items_col1 = [
        ("chk_owner_match", "등기부등본으로 집주인 이름과 계약서 상 임대인이 같은 사람인지 확인하기"),
        ("chk_rights", "근저당·가압류·가처분이 과도하게 잡혀 있지 않은지 확인하기"),
        ("chk_agency", "중개업소가 정식 등록된 공인중개사무소인지(등록번호·자격증 비치) 확인하기"),
        ("chk_price", "주변 시세와 비교해 보증금·전세가율이 비정상적으로 높지 않은지 비교하기"),
        ("chk_maintenance", "관리비 항목(경비·청소·승강기·난방 등)과 평균 금액, 추가 비용 여부 확인하기"),
        ("chk_deposit_insurance", "전세보증보험 가입 가능 여부, 보험료 및 부담 주체(임대인 vs 임차인) 확인하기"),
        ("chk_contract_copy", "계약서 사본과 특약 사항을 사진 또는 스캔으로 따로 보관하기"),
        ("chk_id_match", "임대인(또는 대리인)의 신분증과 등기부 상 소유자 정보가 일치하는지 확인하기"),
    ]

    items_col2 = [
        ("chk_defects", "벽·천장·창틀 곰팡이, 누수 자국, 균열, 바닥 울렁거림 등 하자 여부 체크하기"),
        ("chk_sun_dir", "해가 들어오는 방향(남향·동향·서향)과 채광, 겨울철 결로 가능성 확인하기"),
        ("chk_noise", "밤 시간대에 다시 방문해 층간소음·술집·도로·공사장 소음 등 확인하기"),
        ("chk_smell", "화장실·배수구·복도 악취, 담배 냄새, 음식 냄새 등이 심하지 않은지 체크하기"),
        ("chk_infra", "편의점·마트·병원·학교·카페·지하철역 등 생활 인프라 거리 확인하기"),
        ("chk_register", "전입신고·확정일자 받는 날짜와 이사 날짜를 미리 계획하고 메모해 두기"),
        ("chk_safety", "공동현관 잠금장치, CCTV, 비상구, 소화기 등 기본 안전 설비 상태 확인하기"),
        ("chk_parking", "주차 공간이 필요한 경우, 실제로 주차 가능한지(세대 수 대비) 확인하기"),
    ]

    with col1:
        for key, label in items_col1:
            st.checkbox(label, key=key)
    with col2:
        for key, label in items_col2:
            st.checkbox(label, key=key)

    st.info(
        "💡 체크박스는 `key`를 기준으로 `st.session_state`에 저장돼서, "
        "앱을 새로 고쳐도 같은 브라우저 세션에서 다시 열면 상태가 유지돼요."
    )

# ---------------- 집 후기 탭 ----------------
with tab_review:
    st.subheader("집 후기 (세입자 경험 공유)")

    if "reviews" not in st.session_state:
        st.session_state["reviews"] = {}

    addr_key = (address or "").strip()

    if not addr_key:
        st.info("먼저 위에서 **주소를 입력**하면, 해당 주소 기준으로 후기를 남기고 볼 수 있어요.")
    else:
        reviews = st.session_state["reviews"].get(addr_key, [])
        st.markdown(f"**현재 이 주소에 등록된 후기: {len(reviews)}개**")

        if reviews:
            for i, r in enumerate(reviews):
                header = f"후기 #{i+1} · {r.get('nickname', '익명')} · 별점 {r.get('rating', 0)}/5"
                with st.expander(header):
                    st.write("· 거주 기간:", r.get("period", ""))
                    st.write("· 좋았던 점:", r.get("pros", ""))
                    st.write("· 아쉬웠던 점 / 주의할 점:", r.get("cons", ""))
                    flags = []
                    if r.get("noise_issue"):
                        flags.append("소음 심함")
                    if r.get("bug_issue"):
                        flags.append("벌레 자주 나옴")
                    if r.get("mold_issue"):
                        flags.append("곰팡이/누수 문제")
                    if r.get("landlord_good"):
                        flags.append("집주인 친절함")
                    if r.get("landlord_bad"):
                        flags.append("집주인/관리 응대 불친절")
                    if flags:
                        st.write("· 한 줄 요약 태그:", ", ".join(flags))
        else:
            st.write("아직 등록된 후기가 없습니다. 이 집에 살아본 적이 있다면 첫 후기를 남겨 주세요!")

        st.markdown("---")
        st.markdown("### 새 후기 남기기")

        with st.form("review_form"):
            nickname = st.text_input("닉네임 (선택)", placeholder="예) 전세살이 2년차")
            period = st.selectbox(
                "실제 거주 기간 (대략)",
                ["6개월 미만", "6개월~1년", "1~2년", "2년 이상"],
            )
            rating = st.slider("별점 (1~5)", min_value=1, max_value=5, value=4)
            pros = st.text_area("좋았던 점", height=80, placeholder="예) 역이 가깝고 채광이 좋아요.")
            cons = st.text_area("아쉬웠던 점 / 주의할 점", height=80, placeholder="예) 층간소음이 심해서 밤에 시끄러웠어요.")
            noise_issue = st.checkbox("소음이 신경 쓰였어요")
            bug_issue = st.checkbox("벌레가 자주 나왔어요")
            mold_issue = st.checkbox("곰팡이/누수 문제 있었어요")
            landlord_good = st.checkbox("집주인이 비교적 친절했어요")
            landlord_bad = st.checkbox("집주인/관리인 응대가 별로였어요")
            submitted = st.form_submit_button("후기 등록하기")

        if submitted:
            new_r = {
                "nickname": nickname or "익명",
                "period": period,
                "rating": rating,
                "pros": pros,
                "cons": cons,
                "noise_issue": noise_issue,
                "bug_issue": bug_issue,
                "mold_issue": mold_issue,
                "landlord_good": landlord_good,
                "landlord_bad": landlord_bad,
            }
            all_reviews = st.session_state["reviews"].get(addr_key, [])
            all_reviews.append(new_r)
            st.session_state["reviews"][addr_key] = all_reviews
            st.success("후기가 저장되었습니다. 위 목록에서 방금 남긴 후기를 확인할 수 있어요.")

# ---------------- 사후 대응 탭 ----------------
with tab_after:
    st.subheader("분쟁(보증금 미반환·전세사기 의심) 발생 시 대응 플로우")

    after_text = (
        "1️⃣ 증거 싹 모으기\n"
        "- 임대인과 주고받은 문자·카톡·메일, 통화 녹취, 계좌이체 내역, 계약서 원본 모두 보관하기\n"
        "- 집 상태 사진·영상(하자, 곰팡이, 누수 등)도 시간 보이게 촬영해서 클라우드에 백업하기\n"
        "- 중개업소 상호·주소·전화번호, 공인중개사 이름과 등록번호도 함께 기록해 두기\n\n"
        "2️⃣ 내용증명 보내기\n"
        "- 언제까지 어떤 금액을 지급하라는지, 계약 내용을 정리해 내용증명 우편 발송하기\n"
        "- 이 단계에서 한국법률구조공단이나 변호사 상담을 먼저 받아 두면 이후 절차 설계에 도움이 됨\n\n"
        "3️⃣ 공식 상담 기관 활용하기\n"
        "- 한국법률구조공단: 무료 또는 저렴한 비용으로 법률 상담, 소송 지원 가능 여부 문의\n"
        "- 주택도시보증공사(HUG): 전세보증보험 가입 여부, 보증금 반환 보증 청구 가능성 확인\n"
        "- 지자체 주거복지센터·전월세 지원센터: 지역별 전세피해 상담 창구, 긴급 지원 제도 문의\n\n"
        "4️⃣ 전세사기 의심 시 신고·고소 검토\n"
        "- 집주인이 애초에 돌려줄 의사가 없어 보이거나, 여러 집을 동시에 깡통전세로 운영한 정황이 있으면\n"
        "  → 관할 경찰서 민원실에 사기 혐의로 신고·고소 상담하기\n"
        "- 불법 중개(허위 매물, 중개사 미등록 등) 의심 시\n"
        "  → 관할 시·군·구청 부동산 담당 부서, 국토부 전세사기·불법중개 신고센터 활용하기\n\n"
        "5️⃣ 법적 절차 진행 (전문가와 함께)\n"
        "- 임차권 등기명령 신청: 집을 이미 비웠거나 비워야 할 때, 대항력·우선변제권을 유지하기 위한 절차\n"
        "- 보증금 반환 청구 소송 제기: 판결 후에도 안 주면 강제집행(부동산 경매 등) 절차로 이어질 수 있음\n"
        "- 이 단계는 반드시 한국법률구조공단, 변호사 등과 상의한 뒤 진행하는 것이 안전함\n\n"
        "※ 깡통체크는 \"어떤 순서로 움직이면 좋을지\" 방향을 잡아주는 교육용 도구이고,\n"
        "   실제 법률 자문·소송 대리는 전문 기관과 함께 해야 합니다."
    )
    st.markdown(after_text)

# ---------------- 부모님과 공유 탭 ----------------
with tab_share:
    st.subheader("부모님과 결과 공유")

    if "score" not in locals() or score is None or deposit <= 0:
        st.write("먼저 위쪽에서 주소·보증금 등을 입력하고 **'위험도 스캔하기'** 버튼을 눌러 주세요.")
    else:
        level, msg = risk_label(score)
        issues_text = ", ".join(memo_issues) if memo_issues else "특이사항 없음"

        lifestyle_bits = []
        if noise_sensitive:
            lifestyle_bits.append("소음에 예민함")
        if hate_walking:
            lifestyle_bits.append("걷는 것 비선호")
        if night_active:
            lifestyle_bits.append("야행성")
        lifestyle_text = ", ".join(lifestyle_bits) if lifestyle_bits else "별도 기입 없음"

        lines = []
        lines.append("[깡통체크 전·월세 위험도 결과 공유]")
        lines.append("")
        if address:
            lines.append("• 주소: " + address)
        else:
            lines.append("• 주소: (입력 안 함)")
        lines.append("• 계약 형태: " + contract_type)
        lines.append("• 세입자 유형: " + tenant_type)
        lines.append("• 보증금: " + str(deposit) + "만 원")
        lines.append("• 월세: " + str(rent) + "만 원")
        lines.append("• 생활 패턴: " + lifestyle_text)
        lines.append("")
        lines.append("• 위험도 점수: " + str(score) + " / 100점 (" + level + ")")
        lines.append("• 내부 하자·위험 요소(메모 기준): " + issues_text)
        lines.append("")
        lines.append("• 요약 코멘트: " + msg)
        lines.append("")
        lines.append("※ 이 결과는 실제 법률·부동산 자문이 아닌, 전세사기를 의식하게 도와주는 교육용 참고 자료입니다.")

        share_text = "\n".join(lines)

        st.caption("아래 내용을 복사해서 카톡/문자/메일 등으로 부모님께 보내면 좋아요.")
        st.text_area("부모님께 보내기용 요약", value=share_text, height=260)

        st.markdown(
            "- 부모님과 같이 볼 때 이런 점을 함께 이야기해 보세요.\n"
            "  - 이 보증금·월세 수준이 우리 집 형편에 맞는지\n"
            "  - 전세보증보험을 꼭 드는 게 좋을지\n"
            "  - 혹시 더 안전한 매물이 있는지, 중개사에게 무엇을 더 물어봐야 할지"
        )

# ---------------- 시뮬레이션 탭 ----------------
with tab_sim:
    st.subheader("조건 시뮬레이션")

    s_deposit = st.slider("보증금 (만원)", min_value=500, max_value=10000, value=5000, step=500)
    s_rent = st.slider("월세 (만원)", min_value=0, max_value=100, value=40, step=5)
    s_type = st.selectbox("계약 형태(가정)", ["전세", "반전세", "월세"])

    sim_score, _ = compute_risk_score(s_deposit, s_rent, s_type, "")
    level, msg = risk_label(sim_score)

    st.markdown(f"**시뮬레이션 점수: {sim_score} / 100점 · {level}**")
    st.progress(sim_score / 100.0)
    st.caption("보증금·월세·계약 형태에 따라 위험도가 어떻게 바뀌는지 감각을 익히기 위한 기능입니다.")

st.caption("© 2025 깡통체크(가상 서비스) · 전세사기 예방 교육용 프로토타입")
