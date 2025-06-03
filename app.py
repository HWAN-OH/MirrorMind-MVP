import streamlit as st
from response_engine import generate_response

# 초기 인격 정의
initial_profiles = {
    "재규 (Jaegyu)": {"감정": 2, "사고": 5, "표현": 3, "가치": 4, "편향": "중립"},
    "유민 (Yoomin)": {"감정": 3, "사고": 4, "표현": 2, "가치": 5, "편향": "보수적"},
    "현지 (Hyunji)": {"감정": 5, "사고": 3, "표현": 4, "가치": 3, "편향": "진보적"},
}

# 세션 초기화
if "personas" not in st.session_state:
    st.session_state.personas = initial_profiles.copy()
if "default_selection" not in st.session_state:
    st.session_state.default_selection = list(initial_profiles.keys())

st.title("🧠 MirrorMind: AI 인격 시뮬레이션")

# 인격 선택
valid_personas = list(st.session_state.personas.keys())
default_selection_filtered = [p for p in st.session_state.default_selection if p in valid_personas]
selected_personas = st.multiselect(
    "인격 선택 / Choose personas",
    options=valid_personas,
    default=default_selection_filtered
)

st.caption("""
※ 재규: 논리적 사고가 강하고 감정 표현은 절제된 스타일입니다.  
※ 유민: 분석적이고 내성적인 성향을 가지며, 가치 기반 판단을 중요시합니다.  
※ 현지: 감성적이고 표현력이 뛰어나며 따뜻한 시각으로 접근합니다.
""")

# 상황 입력
situation = st.text_area("상황 설명 / Situation", placeholder="예: 회의에서 의견 충돌이 있었던 상황")

# 답변 생성
if st.button("답변 생성 / Generate Responses") and situation:
    for name in selected_personas:
        if name in st.session_state.personas:
            profile = st.session_state.personas[name]
            with st.expander(f"💬 {name}의 반응 / Response from {name}"):
                response = generate_response(profile, situation)
                st.write(response)
        else:
            st.warning(f"{name} 인격 정보가 누락되어 답변을 생성할 수 없습니다.")

st.divider()

# 새 인격 생성
with st.sidebar:
    st.header("➕ 새로운 인격 생성")
    label = st.text_input("이름 / Name")
    col1, col2 = st.columns(2)
    with col1:
        emotion = st.slider("감정 / Emotion", 1, 5, 3)
        logic = st.slider("사고 / Logic", 1, 5, 3)
    with col2:
        expression = st.slider("표현 / Expression", 1, 5, 3)
        value = st.slider("가치 / Values", 1, 5, 3)
    if st.button("인격 추가"):
        if label:
            bias = "랜덤"  # 추후 자동 바이어스 설정 가능
            st.session_state.personas[label] = {
                "감정": emotion, "사고": logic, "표현": expression, "가치": value, "편향": bias
            }
            st.session_state.default_selection.append(label)
            st.success(f"'{label}' 인격이 추가되었습니다.")
        else:
            st.error("이름을 입력해주세요.")

    st.markdown("""
---
### © 2025 SungHwan Oh. All rights reserved.  
본 앱 및 생성된 인격 구조, 인터페이스, 설계 철학은 모두 **오승환**에게 저작권이 있습니다.  
문의: [hawn21@gmail.com](mailto:hawn21@gmail.com)
""")