# streamlit_app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. 예측 결과 불러오기
df = pd.read_csv("predicted_4weeks.csv")

st.title("📦 다음 4주 수요 예측 대시보드")

# 2. 카테고리 필터 UI
cat = st.selectbox("카테고리 선택", df['cat_id'].unique())
dept = st.selectbox("부서 선택", df[df['cat_id'] == cat]['dept_id'].unique())
store = st.selectbox("지점 선택", df[df['dept_id'] == dept]['store_id'].unique())
item = st.selectbox("상품 선택", df[(df['dept_id'] == dept) & (df['store_id'] == store)]['item_id'].unique())

# 3. 선택된 조건에 해당하는 데이터 필터링
filtered = df[(df['cat_id'] == cat) &
              (df['dept_id'] == dept) &
              (df['store_id'] == store) &
              (df['item_id'] == item)]

# 4. 예측 시계열 그래프
fig, ax = plt.subplots()
ax.plot(filtered['week'], filtered['predicted_sales'], marker='o', color='seagreen')
ax.set_title(f"{item} - 4주 예측")
ax.set_xlabel("주차")
ax.set_ylabel("예측 수요량")
ax.grid(True)
st.pyplot(fig)
