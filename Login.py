import streamlit as st


# ✅ 세션 상태 체크
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    user_id = st.text_input("📌 배정받은 번호를 입력하세요 (예: a17)").lower()
    password = st.text_input("🔒 비밀번호를 입력하세요", type="password")

    def extract_number(uid):
        if uid.startswith("a") and uid[1:].isdigit():
            return int(uid[1:])
        return None

    user_num = extract_number(user_id)

    if not user_id:
        st.warning("배정번호를 입력하세요")
        st.stop()
    elif user_num is None or not (1 <= user_num <= 100):
        st.error("잘못된 배정번호입니다 (a1~a100)")
        st.stop()

    if not password:
        st.warning("비밀번호를 입력하세요")
        st.stop()

    if 1 <= user_num <= 20:
        correct_password = "rlghlrtlf"
    elif 21 <= user_num <= 50:
        correct_password = "duddjqqn"
    elif 51 <= user_num <= 70:
        correct_password = "todtksqn"
    else:
        correct_password = "allerman"

    if password != correct_password:
        st.error("비밀번호가 틀렸습니다.")
        st.stop()

    st.session_state.authenticated = True
    st.rerun()

# ✅ 로그인 성공 후 안내
st.success("✅ 인증 성공! 왼쪽에서 원하는 페이지를 선택하세요.")

st.markdown("""
---
### 사용 가능한 페이지
- 📋 **Rawdata**: 전체 데이터 확인 및 다운로드
- 📊 **Summary**: 월별 판매량 / 매출 요약
- 📈 **SKU Trend**: SKU별 일자별 판매/매출 추이 시각화

> 왼쪽 사이드바에서 페이지를 선택해 이동하세요.

---

### ℹ️ 데이터 안내
- 해당 데이터는 유통별 수집 방식에 따라 전처리된 데이터입니다.
- 판매수량, 매출, 사전원가 등은 모두 **반품이 반영**된 수치이며, **VAT 제외**입니다.
- 파르페 24년 매출 비중은 반영되지 않았습니다.
- 다운로드된 CSV 파일은 Excel에서 열 수 있으며, 추가 편집이 필요할 경우 Excel로 저장 후 사용해주세요.

---

### ❓ 문의
-  개발 및 데이터 설계 : 기획실 홍은정 대리
""")
