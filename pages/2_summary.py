from shared_filter import load_filtered_data
import streamlit as st


if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.warning("🔒 로그인 후에 접근할 수 있습니다.")
    st.stop()

st.set_page_config(page_title="요약 데이터", layout="wide")

st.subheader("📊 월별 판매량 요약 데이터")
st.write("⏱️ 데이터 크기에 따라 로딩이 길어질 수 있습니다(1~5분 소요)")

# 필터링된 데이터 가져오기
filtered_df, start_date, end_date = load_filtered_data()

# ✅ 데이터 없을 경우 처리
if filtered_df.empty:
    st.warning("❗선택된 조건에 해당하는 데이터가 없습니다.")
    st.stop()

# ✅ 월별 판매량 요약 테이블
sales_pivot = (
    filtered_df.groupby(['품목번호', '품목명', '사이즈', '색상', '주문월'])
    .agg(판매량=('판매량', 'sum'))
    .reset_index()
    .pivot_table(
        index=['품목번호', '품목명', '사이즈', '색상'],
        columns='주문월',
        values='판매량',
        fill_value=0
    )
    .reset_index()
)

st.dataframe(sales_pivot)
st.download_button(
    "📥 판매량 다운로드",
    sales_pivot.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig'),
    file_name=f"sales_volume_summary_{start_date}_{end_date}.csv",
    mime="text/csv"
)

# ✅ 월별 매출 요약 테이블 (원 단위)
st.subheader("📊 월별 매출 요약 데이터")
st.write("⏱️ 데이터 크기에 따라 로딩이 길어질 수 있습니다(1~5분 소요)")

revenue_pivot = (
    filtered_df.groupby(['품목번호', '품목명', '사이즈', '색상', '주문월'])
    .agg(매출=('매출', 'sum'))  # 원 단위 그대로 사용
    .reset_index()
    .pivot_table(
        index=['품목번호', '품목명', '사이즈', '색상'],
        columns='주문월',
        values='매출',
        fill_value=0
    )
    .reset_index()
)

st.dataframe(revenue_pivot)
st.download_button(
    "📥 매출 다운로드 (단위: 원)",
    revenue_pivot.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig'),
    file_name=f"sales_revenue_summary_{start_date}_{end_date}.csv",
    mime="text/csv"
)
st.caption("※ 매출 데이터는 원 단위로 제공됩니다.")