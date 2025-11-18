import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    df = pd.read_csv("product_1.csv")
    return df

df = load_data()

st.title("상품 검색 / 정렬 데모")

st.write("CSV에 저장된 상품 데이터를 검색하고, 이름·가격 기준으로 정렬하는 예시입니다.")

# ---- 검색어 입력 ----
query = st.text_input("상품명을 입력하세요 (예: 라면, 김밥, 샌드위치)")

# ---- 정렬 기준 선택 ----
sort_option = st.radio(
    "정렬 기준을 선택하세요",
    ("기본순", "이름 오름차순", "이름 내림차순", "가격 낮은순", "가격 높은순")
)

st.subheader("검색 결과")

# 🔹 검색어가 있을 때만 결과를 보여줌
if query:
    # 부분 일치 검색
    filtered = df[df["상품명"].astype(str).str.contains(query, case=False, na=False)]

    # 정렬 처리
    if sort_option == "이름 오름차순":
        filtered = filtered.sort_values(by="상품명", ascending=True)
    elif sort_option == "이름 내림차순":
        filtered = filtered.sort_values(by="상품명", ascending=False)
    elif sort_option == "가격 낮은순":
        filtered = filtered.sort_values(by="가격", ascending=True)
    elif sort_option == "가격 높은순":
        filtered = filtered.sort_values(by="가격", ascending=False)
    # "기본순"은 정렬 안 함

    if filtered.empty:
        st.info("조건에 맞는 상품이 없습니다.")
    else:
        st.dataframe(
            filtered[["상품ID", "상품명", "카테고리", "가격"]],
            use_container_width=True,
        )
else:
    # 아직 검색어가 없으면 안내만 보여주고 리스트는 숨김
    st.info("검색창에 상품명을 입력한 뒤 Enter를 누르면 결과가 표시됩니다.")
