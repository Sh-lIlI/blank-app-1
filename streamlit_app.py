import streamlit as st
import pandas as pd

# ---- 데이터 불러오기 ----
@st.cache_data
def load_data():
    df = pd.read_csv("product_1.csv")
    return df

df = load_data()

st.title("상품 검색")

# ---- 검색어 입력 ----
query = st.text_input("상품명을 입력하세요 (예: 라면, 김밥, 샌드위치, 과자)")

# ---- 세션 상태 초기화 ----
if "sort_col" not in st.session_state:
    st.session_state["sort_col"] = None  # "상품명" 또는 "가격"
if "name_asc" not in st.session_state:
    st.session_state["name_asc"] = True  # True=오름차순, False=내림차순
if "price_asc" not in st.session_state:
    st.session_state["price_asc"] = True

# ---- 정렬 버튼 ----
col1, col2 = st.columns(2)

with col1:
    if st.button("이름 정렬"):
        # 지금 값 토글 → 클릭할 때마다 오름/내림 변경
        st.session_state["name_asc"] = not st.session_state["name_asc"]
        st.session_state["sort_col"] = "상품명"

with col2:
    if st.button("가격 정렬"):
        st.session_state["price_asc"] = not st.session_state["price_asc"]
        st.session_state["sort_col"] = "가격"

st.subheader("검색 결과")

# ---- 검색어가 있을 때만 결과 표시 ----
if query:
    # 부분 일치 검색
    filtered = df[df["상품명"].astype(str).str.contains(query, case=False, na=False)]

    # ---- 정렬 적용 ----
    sort_col = st.session_state["sort_col"]

    if sort_col == "상품명":
        filtered = filtered.sort_values(
            by="상품명",
            ascending=st.session_state["name_asc"]
        )
    elif sort_col == "가격":
        filtered = filtered.sort_values(
            by="가격",
            ascending=st.session_state["price_asc"]
        )
    # sort_col 이 None이면 정렬 안 함 (default)

    if filtered.empty:
        st.info("조건에 맞는 상품이 없습니다.")
    else:
        st.dataframe(
            filtered[["상품명", "가격"]],
            use_container_width=True,
        )
else:
    st.info("검색창에 상품명을 입력한 뒤 Enter를 누르면 결과가 표시됩니다.")
