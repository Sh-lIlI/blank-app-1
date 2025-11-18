import streamlit as st
import pandas as pd

# ---- 데이터 불러오기 ----
@st.cache_data
def load_data():
    df = pd.read_csv("product_1.csv")
    return df

df = load_data()

st.title("상품 검색 / 정렬 데모")

st.write("CSV에 저장된 상품 데이터를 검색하고, 이름·가격 기준으로 정렬하는 예시입니다.")

# ---- 검색어 입력(플로우차트의 '상품명을 입력하시오(A)') ----
query = st.text_input("상품명을 입력하세요 (예: 라면, 김밥, 샌드위치)")

# ---- 정렬 기준 선택 ----
sort_option = st.radio(
    "정렬 기준을 선택하세요",
    ("기본순", "이름 오름차순", "이름 내림차순", "가격 낮은순", "가격 높은순")
)

# ---- 검색(순차 탐색 느낌으로 필터링) ----
if query:
    # 부분 일치 검색 (해당 단어가 들어간 상품명 모두)
    filtered = df[df["상품명"].astype(str).str.contains(query, case=False, na=False)]
else:
    filtered = df.copy()

# ---- 정렬 처리 ----
if sort_option == "이름 오름차순":
    filtered = filtered.sort_values(by="상품명", ascending=True)
elif sort_option == "이름 내림차순":
    filtered = filtered.sort_values(by="상품명", ascending=False)
elif sort_option == "가격 낮은순":
    filtered = filtered.sort_values(by="가격", ascending=True)
elif sort_option == "가격 높은순":
    filtered = filtered.sort_values(by="가격", ascending=False)
# "기본순"은 정렬 X

# ---- 결과 출력(플로우차트의 *@라면 출력 / @김밥 출력... 부분) ----
st.subheader("검색 결과")

if filtered.empty:
    st.info("조건에 맞는 상품이 없습니다.")
else:
    # 보여줄 컬럼만 선택해서 출력
    st.dataframe(filtered[["상품ID", "상품명", "가격"]], use_container_width=True)
