import streamlit as st

def main():
    st.set_page_config(page_title="단백질 정량 계산기", page_icon="🧪")

    st.title("🧪 단백질 정량 계산기")
    st.markdown("---")

    # ---------------------------------------------------------
    # 1. 기본 데이터 입력 (공통)
    # ---------------------------------------------------------
    st.header("1. 기본 데이터 입력")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 단백질 정량 농도: 소수점 둘째자리까지
        measured_conc = st.number_input(
            "측정된 단백질 농도 (µg/ml)", 
            min_value=0.0, 
            format="%.2f", 
            step=0.01,
            value=3.16,
            help="분광광도계 등을 통해 측정된 희석된 시료의 농도입니다."
        )

    with col2:
        # 희석 배수: 정수 입력
        dilution_factor = st.number_input(
            "희석 배수 (D)", 
            min_value=1, 
            step=1, 
            format="%d",
            value=100,
            help="예: 100D인 경우 100을 입력하세요."
        )

    # 실제 원액 농도 계산
    actual_conc = measured_conc * dilution_factor
    st.info(f"💡 희석 배수를 고려한 **실제 시료 농도**: **{actual_conc:,.2f} µg/ml**")

    st.markdown("---")

    # ---------------------------------------------------------
    # 2. 목표 단백질 함량을 위한 시료 부피 계산
    # ---------------------------------------------------------
    st.header("2. 필요 시료 부피 계산")
    st.caption("실험에 사용할 단백질 함량을 입력하면, 취해야 할 시료의 부피를 알려줍니다.")

    # 취하고자 하는 protein 함량: 정수 입력
    target_mass = st.number_input(
        "취하고자 하는 Protein 함량 (µg)", 
        min_value=0.0, 
        step=1.0, 
        format="%.0f",
        value=20.0
    )

    if st.button("필요 부피 계산하기"):
        if actual_conc > 0:
            # 계산 로직: 부피(ml) = 질량(µg) / 농도(µg/ml)
            volume_ml = target_mass / actual_conc
            volume_ul = volume_ml * 1000

            # 출력 단위 조절 (소수점 아래로 너무 내려가지 않도록)
            if volume_ml < 1.0:
                # 1ml 미만이면 µl 단위로 표시 (소수점 첫째자리 반올림)
                result_str = f"{volume_ul:.1f} µl"
            else:
                # 1ml 이상이면 ml 단위로 표시 (소수점 첫째자리 반올림)
                result_str = f"{volume_ml:.1f} ml"

            st.success(f"🧪 취해야 하는 시료 부피: **{result_str}**")
        else:
            st.error("농도가 0입니다. 입력값을 확인해주세요.")

    st.markdown("---")

    # ---------------------------------------------------------
    # 3. 총 단백질 함량 계산 (추가 기능)
    # ---------------------------------------------------------
    st.header("3. 시료 내 총 단백질 함량 확인")
    st.caption("시료의 부피를 입력하면, 시료 안에 들어있는 총 단백질 양을 계산합니다.")

    c1, c2 = st.columns([2, 1])
    
    with c1:
        sample_volume = st.number_input(
            "시료 부피 입력", 
            min_value=0.0, 
            format="%.1f",
            step=0.1
        )
    
    with c2:
        vol_unit = st.radio(
            "단위 선택", 
            ("µl", "ml"),
            horizontal=True
        )

    if st.button("총 함량 계산하기"):
        if actual_conc > 0:
            # 부피를 ml로 통일하여 계산
            input_vol_ml = sample_volume if vol_unit == "ml" else sample_volume / 1000.0
            
            # 총 함량(µg) = 농도(µg/ml) * 부피(ml)
            total_mass_ug = actual_conc * input_vol_ml
            
            # 단위 변환 (1000µg 이상이면 mg으로 표기)
            if total_mass_ug >= 1000:
                total_mass_mg = total_mass_ug / 1000.0
                st.success(f"📊 시료 내 총 단백질 함량: **{total_mass_mg:,.2f} mg**")
            else:
                st.success(f"📊 시료 내 총 단백질 함량: **{total_mass_ug:,.1f} µg**")
        else:
            st.warning("먼저 위에서 농도와 희석배수를 입력해주세요.")

if __name__ == "__main__":
    main()