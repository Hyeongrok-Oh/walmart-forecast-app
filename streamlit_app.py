# streamlit_app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. 예측 결과 불러오기
df = pd.read_csv("predicted_4weeks.csv")

st.title("📦 다음 4주 수요 예측 대시보드")

df['week'] = (df['week']).astype(int)

# 2. 카테고리 필터 UI
store = st.selectbox("지점 선택", df['store_id'].unique())
cat = st.selectbox("카테고리 선택", df[df['store_id'] == store]['cat_id'].unique())
dept = st.selectbox("부서 선택", df[df['cat_id'] == cat]['dept_id'].unique())
item = st.selectbox("상품 선택", df[(df['dept_id'] == dept) & (df['store_id'] == store)]['item_id'].unique())

# 3. 선택된 조건에 해당하는 데이터 필터링
filtered = df[(df['cat_id'] == cat) &
              (df['dept_id'] == dept) &
              (df['store_id'] == store) &
              (df['item_id'] == item)]

# 4. 예측 시계열 그래프
fig, ax = plt.subplots()
ax.plot(["1","2","3","4"], filtered['predicted_sales'], marker='o', color='seagreen')
ax.set_title(f"{item} expected sales")
ax.set_xlabel("Weeks After This Week")
ax.set_ylabel("Sales")
ax.grid(True)
st.pyplot(fig)

# 2. 지점 선택 (store_id 기준)
store = st.selectbox("지점을 선택하세요", df['store_id'].unique())

# 3. 해당 지점 데이터 필터링
store_df = df[df['store_id'] == store]

# 4. 지점 전체 데이터 다운로드 버튼
st.download_button(
    label=f"📥 {store} 지점 전체 예측 결과 다운로드",
    data=store_df.to_csv(index=False).encode('utf-8-sig'),
    file_name=f"{store}_predicted_4weeks.csv",
    mime='text/csv'
)

# 5. (옵션) 요약 그래프 예시 – 가장 많이 팔릴 상품 1개
top_item = store_df.groupby('item_id')['predicted_sales'].sum().idxmax()
item_df = store_df[store_df['item_id'] == top_item]

st.subheader(f"🔥 {store} - {top_item}의 예측 추이")

fig, ax = plt.subplots()
ax.plot(item_df['week'], item_df['predicted_sales'], marker='o', color='darkgreen')
ax.set_title(f"{top_item} 예측 수요량 (주별)")
ax.set_xlabel("주차")
ax.set_ylabel("예측 수요량")
ax.grid(True)
st.pyplot(fig)
