import streamlit as st
from response_engine import generate_response
import openai
import os

st.set_page_config(page_title="MirrorMind MVP", layout="wide")

st.title("🧠 MirrorMind: Persona-based Reasoning Simulator")

st.markdown("### 상황 설명 / Situation Description")
situation = st.text_area("예: '상사가 갑자기 회의를 소집했다' / e.g., 'The boss suddenly called a meeting.'", height=100)

st.markdown("### 인격 선택 / Choose personas")
selected_profiles = st.multiselect("아래 인격 중 선택 / Select from below", ["현지 (Hyunji)", "유민 (Yumin)", "재규 (Jaegyu)"])

st.markdown("### 답변 길이 / Response length")
length_option = st.selectbox("응답 길이 선택 / Choose response length", ["보통 / Normal", "길게 / Long"])
max_tokens = 500 if "길게" in length_option else 250

if st.button("🗣️ 답변 생성 / Generate Response"):
    if not situation or not selected_profiles:
        st.warning("상황과 인격을 모두 입력해주세요 / Please enter both situation and personas.")
    else:
        for profile in selected_profiles:
            with st.spinner(f"{profile}의 생각 생성 중..."):
                response = generate_response(profile, situation, max_tokens)
                st.markdown(f"**{profile}** 💬")
                st.write(response)
                st.divider()

st.caption("ⓒ 2025. 승환 오. 모든 권리 보유. / All rights reserved. Contact: hawn21@gmail.com")