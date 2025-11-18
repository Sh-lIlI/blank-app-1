import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    df = pd.read_csv("product_1.csv")
    return df

df = load_data()

st.title("상품 검색")

# --- 검색어 입력 ---
query = st.text_input("상품명을 입력하세요 (예: 라면, 김밥, 샌드위치)")

# 검색어 없으면 결과/버튼 둘 다 안 보이게
if not query:
    st.info("검색어를 입력하면 결과가 표시됩니다.")
    st.stop()

# --- 세션 상태 초기화 (가격 정렬만) ---
if "price_order" not in st.session_state:
    st.session_state["price_order"] = None

st.subheader("검색 결과")

# --- 정렬 버튼을 오른쪽으로 몰기 ---
# 앞 컬럼은 여백용, 뒤 두 개에 버튼
spacer, col_low, col_high = st.columns([6, 1, 1])

with col_low:
    if st.button("가격 낮은 순"):
        st.session_state["price_order"] = "asc"

with col_high:
    if st.button("가격 높은 순"):
        st.session_state["price_order"] = "desc"



# --- 검색 필터 ---
result = df[df["상품명"].str.contains(query)]

# --- 가격 정렬 적용 ---
if st.session_state["price_order"] == "asc":
    result = result.sort_values("가격", ascending=True)
elif st.session_state["price_order"] == "desc":
    result = result.sort_values("가격", ascending=False)

st.dataframe(result, use_container_width=True)
