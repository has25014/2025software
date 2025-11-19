import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="베스킨라빈스 키오스크",
    page_icon="🍨",
)

st.title("🍨 베스킨라빈스 키오스크")
st.caption("천천히 골라도 괜찮아요! 제가 끝까지 도와드릴게요 😊")

st.markdown("---")

# 1. 매장에서 / 포장 선택
eat_where = st.radio(
    "1️⃣ 어디서 드실 건가요?",
    ("매장에서 먹고 갈게요 🪑", "포장해서 가져갈게요 🛍️")
)

st.markdown("---")

# 2. 용기 사이즈 선택
st.subheader("2️⃣ 용기 사이즈를 선택해 주세요 📦")

size_info = {
    "싱글컵 (1스쿱)": {"price": 3500, "scoops": 1},
    "더블컵 (2스쿱)": {"price": 6500, "scoops": 2},
    "파인트 (3스쿱)": {"price": 8200, "scoops": 3},
    "쿼터 (4스쿱)": {"price": 15500, "scoops": 4},
}

size_name = st.selectbox(
    "용기 사이즈를 골라 주세요:",
    list(size_info.keys())
)

selected_size = size_info[size_name]
num_scoops = selected_size["scoops"]
base_price = selected_size["price"]

st.info(f"➡️ 이 사이즈는 **{num_scoops}가지 맛**을 담을 수 있어요! 🍨")

st.markdown("---")

# 3. 맛 선택 (스쿱 수에 맞게)
st.subheader("3️⃣ 아이스크림 맛을 골라 주세요 😋")

flavors = [
    "아몬드 봉봉",
    "베리베리 스트로베리",
    "슈팅스타",
    "초콜릿 무스",
    "민트 초콜릿 칩",
    "뉴욕 치즈케이크",
    "바람과 함께 사라지다",
    "피스타치오 아몬드",
    "엄마는 외계인",
    "체리쥬빌레",
]

selected_flavors = []

for i in range(num_scoops):
    flavor = st.selectbox(
        f"{i + 1}번째 맛을 골라 주세요:",
        flavors,
        key=f"flavor_{i}"
    )
    selected_flavors.append(flavor)

st.markdown("---")

# 4. 결제 수단 & 최종 확인
st.subheader("4️⃣ 결제 수단을 선택해 주세요 💳")

payment_method = st.radio(
    "어떤 방법으로 결제하시겠어요?",
    ("현금 결제 🧾", "카드 결제 💳")
)

# 필요하다면 포장 추가금 같은 것도 여기서 더할 수 있음
total_price = base_price  # 지금은 사이즈 가격만 사용

st.markdown("### 💰 최종 결제 금액")
st.metric(label="총 금액", value=f"{total_price:,} 원")

st.markdown("---")

if st.button("✅ 주문 완료하기"):
    # 텍스트 정리
    where_text = "매장에서 드시고 가는 것" if "매장에서" in eat_where else "포장해서 가져가시는 것"
    flavor_text = " / ".join(selected_flavors)

    st.success("주문이 정상적으로 접수되었습니다! 🎉")
    st.write(f"👉 드시는 방식: **{where_text}**")
    st.write(f"👉 선택하신 사이즈: **{size_name}**")
    st.write(f"👉 선택하신 맛: **{flavor_text}**")
    st.write(f"👉 결제 수단: **{payment_method}**")
    st.write(f"👉 결제하실 금액은 **{total_price:,}원** 입니다. 감사합니다! 🥰")
    st.balloons()
