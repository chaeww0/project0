
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Art Materials",
    page_icon="🎨",
    layout="centered"
)

# 디자인
st.markdown("""
<style>
.stApp {
    background-color: #FAF8F5;
}
h1, h2, h3 {
    color: #51463E;
}
div.stButton > button {
    background-color: #8C7563;
    color: white;
    border-radius: 10px;
    border: none;
    height: 45px;
}
div.stButton > button:hover {
    background-color: #6D5747;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# 기록 저장 공간
if "records" not in st.session_state:
    st.session_state.records = []

st.title("🎨 Art Materials")
st.caption("미술 재료 구매 관리")

st.divider()

st.subheader("재료 정보 입력")

with st.form("material_form"):
    material = st.text_input(
        "재료 이름",
        placeholder="예: 캔버스, 유화 물감, 붓"
    )

    quantity = st.number_input(
        "현재 보유 수량",
        min_value=0,
        step=1,
        value=0
    )

    need = st.number_input(
        "작업에 필요한 수량",
        min_value=0,
        step=1,
        value=1
    )

    submitted = st.form_submit_button(
        "구매 수량 확인",
        use_container_width=True
    )

if submitted:
    if not material.strip():
        st.warning("재료 이름을 입력해주세요.")
    else:
        purchase = max(need - quantity, 0)

        record = {
            "재료 이름": material,
            "현재 보유 수량": quantity,
            "필요 수량": need,
            "구매 수량": purchase
        }

        st.session_state.records.append(record)

        if purchase > 0:
            st.warning(f"{material} 재료가 부족합니다.")
            st.metric("추가 구매 수량", f"{purchase}개")
        else:
            st.success(f"{material} 재료는 충분합니다!")
            st.metric("추가 구매 수량", "0개")

st.divider()

st.subheader("📋 구매 기록")

if st.session_state.records:
    df = pd.DataFrame(st.session_state.records)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    csv_data = df.to_csv(
        index=False,
        encoding="utf-8-sig"
    )

    st.download_button(
        label="구매 기록 다운로드",
        data=csv_data,
        file_name="art_materials.csv",
        mime="text/csv",
        use_container_width=True
    )

    if st.button("기록 초기화"):
        st.session_state.records = []
        st.rerun()

else:
    st.info("아직 저장된 구매 기록이 없습니다.")
