# streamlit_app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. 예측 결과 불러오기
df = pd.read_csv("predicted_4weeks.csv")
df2 = pd.read_csv("last4_weeks.csv")  # 포함: week, item_id, store_id, sales, y_pred, gap, forecast_flag

df['week'] = df['week'].astype(int)

st.title("📦 다음 4주 수요 예측 대시보드")

# 탭으로 기능 분리
tab1, tab2, tab3 = st.tabs(["상품별 예측", "지점별 다운로드", "과거 판매량 분석"])

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

# 📦 Tab 3: 지난 4주간 예측 vs 실제 판매량 비교
with tab3:
    # ✅ 변수명 구분 (store → store_tab3 등)
    store_tab3 = st.selectbox("지점 선택", sorted(df2['store_id'].unique()), key="store_tab3")
    week_tab3 = st.selectbox("주차 선택", sorted(df2['week'].unique(), reverse=True), key="week_tab3")

    # ✅ 필터링된 데이터프레임 (지난 4주 중 선택된 지점 + 주차)
    filtered_tab3 = df2[(df2['store_id'] == store_tab3) & (df2['week'] == week_tab3)]

    # ✅ 예측 상태별 분포 시각화
    st.subheader(f"📊 {store_tab3} 지점 - {week_tab3}주차 예측 분류 현황")
    st.bar_chart(filtered_tab3['forecast_flag'].value_counts())

    # ✅ 과잉재고/부족위험 품목 목록
    st.subheader("🚨 과잉 또는 부족 품목 리스트")
    danger_df = filtered_tab3[filtered_tab3['forecast_flag'] != '✅ 정상범위']
    st.dataframe(danger_df[['item_id', 'sales', 'y_pred', 'gap', 'forecast_flag']])

    # ✅ CSV 다운로드 버튼
    st.download_button(
        label="📥 이 주차 예측 비교 결과 다운로드",
        data=filtered_tab3.to_csv(index=False).encode('utf-8-sig'),
        file_name=f"{store_tab3}_{week_tab3}_예측비교.csv",
        mime='text/csv'
    )

    # ✅ 품목 선택 → 예측 vs 실제 비교 시계열 시각화
    if not filtered_tab3.empty:
        selected_item_tab3 = st.selectbox(
            "📈 품목 예측 추이 보기", 
            filtered_tab3['item_id'].unique(), 
            key="selected_item_tab3"
        )

        item_history_df = df2[
            (df2['store_id'] == store_tab3) & 
            (df2['item_id'] == selected_item_tab3)
        ].sort_values(by="week")

        st.subheader(f"📉 {selected_item_tab3} - 예측 vs 실제 판매량 추이")

        fig, ax = plt.subplots()
        ax.plot(item_history_df['week'], item_history_df['sales'], label='실제 판매량', marker='o')
        ax.plot(item_history_df['week'], item_history_df['y_pred'], label='예측 판매량', marker='x')
        ax.set_title(f"{selected_item_tab3} - 판매량 비교")
        ax.set_xlabel("주차")
        ax.set_ylabel("판매량")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

