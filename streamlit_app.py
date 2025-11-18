import streamlit as st
import pandas as pd

# 🔹 버튼 간격 줄이기용 CSS
st.markdown("""
    <style>
    /* 모든 st.button 간 가로 간격을 조금만 주기 */
    div.stButton > button {
        margin-right: 4px;
        margin-left: 4px;
        padding: 0.3rem 0.8rem;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("product_1.csv")
    return df

df = load_data()

st.title("상품 검색")

# --- 검색어 입력 ---
query = st.text_input("상품명을 입력하세요 (예: 라면, 김밥, 샌드위치, 과자)")

# 검색어 없으면 결과/버튼 둘 다 안 보이게
if not query:
    st.info("검색어를 입력하면 결과가 표시됩니다.")
    st.stop()

# --- 세션 상태 초기화 (가격 정렬만) ---
if "price_order" not in st.session_state:
    st.session_state["price_order"] = None

st.subheader("검색 결과")

# --- 정렬 버튼: 오른쪽에, 한 줄로 배치 ---
left_space, right_buttons = st.columns([6, 4])

with right_buttons:
    col_high, col_low = st.columns(2)
    with col_high:
        if st.button("가격 높은 순"):
            st.session_state["price_order"] = "desc"
    with col_low:
        if st.button("가격 낮은 순"):
            st.session_state["price_order"] = "asc"


# --- 검색 필터 ---
result = df[df["상품명"].str.contains(query)]

# --- 가격 정렬 적용 ---
if st.session_state["price_order"] == "asc":
    result = result.sort_values("가격", ascending=True)
elif st.session_state["price_order"] == "desc":
    result = result.sort_values("가격", ascending=False)

# --- 상품명, 가격만 출력 ---
result = result[["상품명", "가격"]]

# --- 상품명, 가격만 출력 ---
result = result[["상품명", "가격"]]


# 인덱스 숨기고 정적인 표로 출력
st.table(result.style.hide(axis="index"))

