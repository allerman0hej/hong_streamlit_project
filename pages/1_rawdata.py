# 1_rawdata.py

import streamlit as st
from shared_filter import load_filtered_data

if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.warning("🔒 로그인 후에 접근할 수 있습니다.")
    st.stop()

st.set_page_config(page_title="Rawdata", layout="wide")

st.subheader("📋 Rawdata")
st.write("⏱️ 데이터 크기에 따라 로딩이 길어질 수 있습니다(1~5분 소요)")

filtered_df, start_date, end_date = load_filtered_data()

if filtered_df.empty:
    st.warning("❗선택된 조건에 해당하는 데이터가 없습니다.")
else:
    st.dataframe(filtered_df)

    csv = filtered_df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        "📥 선택된 기간 데이터 다운로드 (CSV)",
        csv,
        file_name=f"sales_data_{start_date}_{end_date}.csv",
        mime="text/csv"
    )
