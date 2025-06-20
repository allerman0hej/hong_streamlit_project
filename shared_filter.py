import streamlit as st
import pandas as pd
import datetime
from data_preprocessing import load_data, get_unique_sorted  # ✅ 변경된 파일명 반영

def load_filtered_data():
    if "df_raw" not in st.session_state:
        st.session_state.df_raw = load_data()
    df = st.session_state.df_raw

    # 날짜 필터
    min_date = datetime.date(2022, 1, 1)
    max_date = df['주문/물류일자'].max().date()
    default_start = datetime.date(2025, 5, 1)
    default_end = max_date

    selected_range = st.date_input(
        "📅 기간 선택 (주문/물류일자 기준)",
        (default_start, default_end),
        min_value=min_date,
        max_value=max_date
    )

    # 기본 필터
    with st.expander("🔍 기본 필터", expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            selected_items = st.multiselect("품목번호", get_unique_sorted(df['품목번호']))
        with col2:
            selected_names = st.multiselect("품목명", get_unique_sorted(df['품목명']))
        with col3:
            selected_colors = st.multiselect("색상", get_unique_sorted(df['색상']))
        with col4:
            selected_sizes = st.multiselect("사이즈", get_unique_sorted(df['사이즈']))

    # 상세 필터
    with st.expander("⚙️ 상세 필터", expanded=False):
        col5, col6, col7, col8 = st.columns(4)
        with col5:
            selected_groups = st.multiselect("고객그룹", get_unique_sorted(df['고객그룹']))
        with col6:
            selected_subgroups = st.multiselect("고객소그룹", get_unique_sorted(df['고객소그룹']))
        with col7:
            selected_types = st.multiselect("판매유형", get_unique_sorted(df['판매유형']))
        with col8:
            selected_channels = st.multiselect("주문유형", get_unique_sorted(df['주문유형'])) if '주문유형' in df.columns else []

    # 필터 적용
    start_date, end_date = selected_range
    filtered_df = df[
        (df['주문/물류일자'] >= pd.to_datetime(start_date)) &
        (df['주문/물류일자'] <= pd.to_datetime(end_date))
    ]

    if selected_items:
        filtered_df = filtered_df[filtered_df['품목번호'].isin(selected_items)]
    if selected_names:
        filtered_df = filtered_df[filtered_df['품목명'].isin(selected_names)]
    if selected_colors:
        filtered_df = filtered_df[filtered_df['색상'].isin(selected_colors)]
    if selected_sizes:
        filtered_df = filtered_df[filtered_df['사이즈'].isin(selected_sizes)]
    if selected_groups:
        filtered_df = filtered_df[filtered_df['고객그룹'].isin(selected_groups)]
    if selected_subgroups:
        filtered_df = filtered_df[filtered_df['고객소그룹'].isin(selected_subgroups)]
    if selected_types:
        filtered_df = filtered_df[filtered_df['판매유형'].isin(selected_types)]
    if '주문유형' in df.columns and selected_channels:
        filtered_df = filtered_df[filtered_df['주문유형'].isin(selected_channels)]

    return filtered_df, start_date, end_date
