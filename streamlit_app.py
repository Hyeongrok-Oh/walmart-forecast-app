# streamlit_app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📦 다음 4주 상품별 수요 예측")

# 1. 예측 결과 불러오기
forecast_df = pd.read_csv("predicted_4weeks.csv")

# 2. 상품 선택
item_list = forecast_df['item_id'].unique()
selected_item = st.selectbox("상품을 선택하세요", item_list)

# 3. 선택된 상품만 필터링
item_df = forecast_df[forecast_df['item_id'] == selected_item]

# 4. 시각화
fig, ax = plt.subplots()
ax.plot(item_df['week'], item_df['predicted_sales'], marker='o', color='seagreen')
ax.set_title(f"{selected_item} - 4주 예측")
ax.set_xlabel("주차")
ax.set_ylabel("예측 수요량")
ax.grid(True)
st.pyplot(fig)