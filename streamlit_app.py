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

# 검색어 없으면 결과 표시 안 함
if not query:
    st.info("검색어를 입력하면 결과가 표시됩니다.")
    st.stop()

# --- 세션 상태 초기화 (가격 정렬만) ---
# price_order: None / "asc" / "desc"
if "price_order" not in st.session_state:
    st.session_state["price_order"] = None

# --- 정렬 버튼 (가격 낮은 순 / 높은 순) ---
col1, col2 = st.columns(2)

with col1:
    if st.button("가격 낮은 순"):
        st.session_state["price_order"] = "asc"

with col2:
    if st.button("가격 높은 순"):
        st.session_state["price_order"] = "desc"

st.subheader("검색 결과")

# --- 검색 필터 ---
result = df[df["상품명"].str.contains(query)]

# --- 가격 정렬 적용 ---
if st.session_state["price_order"] == "asc":
    result = result.sort_values("가격", ascending=True)
elif st.session_state["price_order"] == "desc":
    result = result.sort_values("가격", ascending=False)

st.dataframe(result, use_container_width=True)
