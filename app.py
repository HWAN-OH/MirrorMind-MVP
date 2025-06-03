import streamlit as st
from openai import OpenAI
import json
import random

st.set_page_config(page_title="MirrorMind MVP 0.2", layout="wide")
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 초기 인격 정보
initial_profiles = {
    "재규 (Jaegyu)": {"emotion": 2.0, "reasoning": 4.0, "expression": 3.5, "values": 3.0, "bias": 2.5},
    "유민 (Yoomin)": {"emotion": 1.5, "reasoning": 4.5, "expression": 2.0, "values": 3.5, "bias": 1.5},
    "현지 (Hyunji)": {"emotion": 4.5, "reasoning": 3.0, "expression": 4.5, "values": 4.0, "bias": 3.0},
}

if "personas" not in st.session_state:
    st.session_state.personas = dict(initial_profiles)
if "new_persona_flag" not in st.session_state:
    st.session_state.new_persona_flag = False

# 인격 생성 폼
with st.sidebar:
    st.header("🧬 인격 생성 / Persona Creator")
    with st.form("persona_form"):
        name = st.text_input("이름 / Name")
        emotion = st.slider("감정 (감정적 반응의 민감도) / Emotion", 0.0, 5.0, 2.5)
        reasoning = st.slider("사고 (논리적 사고의 강도) / Reasoning", 0.0, 5.0, 2.5)
        expression = st.slider("표현 (표현의 직설성) / Expression", 0.0, 5.0, 2.5)
        values = st.slider("가치 (가치 중심의 판단력) / Values", 0.0, 5.0, 2.5)
        submitted = st.form_submit_button("추가하기 / Add")
        if submitted and name.strip():
            bias = round(random.uniform(1.0, 5.0), 2)
            label = f"{name.strip()} (Custom)"
            st.session_state.personas[label] = {
                "emotion": emotion,
                "reasoning": reasoning,
                "expression": expression,
                "values": values,
                "bias": bias,
            }
            st.session_state.new_persona_flag = True
            st.success(f"'{label}' 인격이 추가되었습니다. (편향 계수는 자동 부여됨: {bias})")
    st.markdown("""
---

ℹ️ **Note:**  
생성된 인격 추출은 다음 버전에서 적용될 예정입니다.  
사용자 생성 인격은 향후 LLM에 적용되어 동일 인격을 유지하며 사용할 수 있도록 확장됩니다.
""")

# 본문 UI
st.title("🪞 MirrorMind - 인격 반응 테스트")
situation = st.text_area("상황을 입력하세요 / Describe a situation", height=100)
response_length = st.radio("응답 길이 / Response length", ["보통 / Medium", "길게 / Long"])

if st.session_state.new_persona_flag:
    default_selection = list(initial_profiles.keys()) + [k for k in st.session_state.personas if k not in initial_profiles]
    st.session_state.new_persona_flag = False
else:
    default_selection = list(initial_profiles.keys())


valid_personas = list(st.session_state.personas.keys())
selected_personas = st.multiselect(
    "인격 선택 / Choose personas",
    valid_personas,
    default=[p for p in default_selection if p in valid_personas]
)

st.caption("""※ 재규: 논리적 사고가 강하고 감정 표현은 절제된 스타일입니다.
※ 유민: 분석적이고 내성적인 성향을 가지며, 가치 기반 판단을 중요시합니다.
※ 현지: 감성적이고 표현력이 뛰어나며 따뜻한 시각으로 접근합니다.""")

length_map = {
    "보통 / Medium": 400,
    "길게 / Long": 800
}

def generate_response(profile, text):
    prompt = f"""
You are an AI persona with the following traits:
Emotion: {profile['emotion']}, Reasoning: {profile['reasoning']}, Expression: {profile['expression']}, Values: {profile['values']}, Bias: {profile['bias']}.
Respond to the user's situation in Korean, matching the emotional and expressive style. Be consistent with the described identity.
Situation: {text}
"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": text}
        ],
        max_tokens=length_map[response_length],
        temperature=1.0
    )
    return response.choices[0].message.content.strip()  # v1 compatible

if st.button("답변 생성 / Generate Responses") and situation:
    for name in selected_personas:
        if name not in st.session_state.personas:
            st.warning(f"{name} 인격 정보가 누락되어 답변을 생성할 수 없습니다.")
            continue
        profile = st.session_state.personas[name]
        with st.expander(f"💬 {name}의 반응 / Response from {name}"):
            response = generate_response(profile, situation)
            st.write(response)