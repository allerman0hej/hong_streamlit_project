from shared_filter import load_filtered_data
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.warning("🔒 로그인 후에 접근할 수 있습니다.")
    st.stop()

st.set_page_config(page_title="SKU별 추이", layout="wide")
st.subheader("📈 SKU별 일자별 판매/매출 추이")
st.write("⏱️ 데이터 크기에 따라 로딩이 길어질 수 있습니다(1~5분 소요)")

# 데이터 불러오기
filtered_df, start_date, end_date = load_filtered_data()

# 데이터 없을 경우
if filtered_df.empty:
    st.warning("❗선택된 조건에 해당하는 데이터가 없습니다.")
    st.stop()

# 선택된 품목이 1개인지 확인
item_codes = filtered_df['품목번호'].unique()
if len(item_codes) != 1:
    st.info("👆 위쪽 필터에서 **품목번호를 1개만 선택**하면 그래프가 나타납니다.")
    st.stop()

# SKU별 그룹핑
sku_grouped = filtered_df.groupby(['SKU_ID', '품목번호', '품목명', '색상', '사이즈'])

for (sku_id, item_code, item_name, item_color, item_size), sku_data in sku_grouped:
    unique_dates = sku_data['주문/물류일자'].sort_values().unique()
    if len(unique_dates) < 2:
        st.info(f"⏸️ {item_code} / {item_name} / {item_color} / {item_size} 는 일자별 데이터가 부족하여 그래프를 생략합니다.")
        continue

    st.markdown(f"### 🔹 {item_code} / {item_name} / {item_color} / {item_size}")

    # 일자별 집계 및 보정
    daily_grouped = sku_data.groupby('주문/물류일자')[['판매량', '매출']].sum().asfreq('D').fillna(0).reset_index()
    daily_grouped['매출'] = (daily_grouped['매출'] / 1000).round(1)

    # 그래프 생성
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=daily_grouped['주문/물류일자'], y=daily_grouped['판매량'],
        name='판매량', yaxis='y1', mode='lines+markers', line=dict(color='royalblue')
    ))

    fig.add_trace(go.Scatter(
        x=daily_grouped['주문/물류일자'], y=daily_grouped['매출'],
        name='매출', yaxis='y2', mode='lines+markers', line=dict(color='orangered', dash='dash')
    ))

    fig.update_layout(
        title='판매량 / 매출 추이',
        xaxis=dict(
            title='날짜',
            rangeslider=dict(visible=True),
            type='date',
            tickformat='%y-%m-%d'
        ),
        yaxis=dict(title='판매량 (건수)', titlefont=dict(color='black'), tickfont=dict(color='black')),
        yaxis2=dict(
            title='매출 (천원)', titlefont=dict(color='black'), tickfont=dict(color='black'),
            overlaying='y', side='right'
        ),
        legend=dict(x=0, y=1.1, orientation='h'),
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)
