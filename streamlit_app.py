# streamlit_app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. 예측 결과 불러오기
df = pd.read_csv("predicted_4weeks.csv")
df['week'] = df['week'].astype(int)

st.title("📦 다음 4주 수요 예측 대시보드")

# 탭으로 기능 분리
tab1, tab2 = st.tabs(["📊 상품별 예측", "📥 지점별 다운로드"])

# 📊 상품별 예측 탭
with tab1:
    store = st.selectbox("지점 선택", df['store_id'].unique())
    cat = st.selectbox("카테고리 선택", df[df['store_id'] == store]['cat_id'].unique())
    dept = st.selectbox("부서 선택", df[df['cat_id'] == cat]['dept_id'].unique())
    item = st.selectbox("상품 선택", df[(df['dept_id'] == dept) & (df['store_id'] == store)]['item_id'].unique())

    filtered = df[(df['cat_id'] == cat) &
                  (df['dept_id'] == dept) &
                  (df['store_id'] == store) &
                  (df['item_id'] == item)]

    fig, ax = plt.subplots()
    ax.plot(["1", "2", "3", "4"], filtered['predicted_sales'], marker='o', color='seagreen')
    ax.set_title(f"{item} expected sales")
    ax.set_xlabel("Weeks After This Week")
    ax.set_ylabel("Sales")
    ax.grid(True)
    st.pyplot(fig)

# 📥 지점별 다운로드 탭
with tab2:
    store = st.selectbox("지점을 선택하세요", df['store_id'].unique(), key="download_store")
    store_df = df[df['store_id'] == store]

    st.download_button(
        label=f"📥 {store} 지점 전체 예측 결과 다운로드",
        data=store_df.to_csv(index=False).encode('utf-8-sig'),
        file_name=f"{store}_predicted_4weeks.csv",
        mime='text/csv'
    )

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
