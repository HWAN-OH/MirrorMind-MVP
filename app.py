import streamlit as st
from openai import OpenAI
import json
import random

# --- Page Configuration / 페이지 설정 ---
# Set the page title and layout. / 페이지 제목과 레이아웃을 설정합니다.
st.set_page_config(page_title="MirrorMind MVP 0.2", layout="wide")

# --- OpenAI Client Initialization / OpenAI 클라이언트 초기화 ---
# Initialize the OpenAI client with the API key from Streamlit secrets.
# Streamlit 시크릿에서 API 키를 가져와 OpenAI 클라이언트를 초기화합니다.
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- Initial Persona Profiles / 초기 페르소나 프로필 ---
# Default personas available at the start of the app.
# 앱 시작 시 기본으로 제공되는 페르소나입니다.
initial_profiles = {
    "재규 (Jaegyu)": {"emotion": 2.0, "reasoning": 4.0, "expression": 3.5, "values": 3.0, "bias": 2.5},
    "유민 (Yoomin)": {"emotion": 1.5, "reasoning": 4.5, "expression": 2.0, "values": 3.5, "bias": 1.5},
    "현지 (Hyunji)": {"emotion": 4.5, "reasoning": 3.0, "expression": 4.5, "values": 4.0, "bias": 3.0},
}

# --- Session State Management / 세션 상태 관리 ---
# Initialize session state for personas if it doesn't exist.
# 'personas' 세션 상태가 없으면 초기화합니다.
if "personas" not in st.session_state:
    st.session_state.personas = dict(initial_profiles)

# Flag to manage default selection in the multiselect widget after adding a new persona.
# 새 페르소나 추가 후 멀티셀렉트 위젯의 기본 선택을 관리하기 위한 플래그입니다.
if "new_persona_flag" not in st.session_state:
    st.session_state.new_persona_flag = False

# --- Sidebar UI / 사이드바 UI ---
with st.sidebar:
    st.header("🧬 인격 생성 / Persona Creator")
    
    # --- Persona Creation Form / 페르소나 생성 폼 ---
    with st.form("persona_form"):
        name = st.text_input("이름 / Name")
        emotion = st.slider("감정 (감정적 반응의 민감도) / Emotion", 0.0, 5.0, 2.5)
        reasoning = st.slider("사고 (논리적 사고의 강도) / Reasoning", 0.0, 5.0, 2.5)
        expression = st.slider("표현 (표현의 직설성) / Expression", 0.0, 5.0, 2.5)
        values = st.slider("가치 (가치 중심의 판단력) / Values", 0.0, 5.0, 2.5)
        submitted = st.form_submit_button("추가하기 / Add")

        if submitted and name.strip():
            # Assign a random bias value for custom personas.
            # 커스텀 페르소나에 무작위 편향 값을 할당합니다.
            bias = round(random.uniform(1.0, 5.0), 2)
            label = f"{name.strip()} (Custom)"
            
            # Add the new persona to the session state.
            # 새 페르소나를 세션 상태에 추가합니다.
            st.session_state.personas[label] = {
                "emotion": emotion,
                "reasoning": reasoning,
                "expression": expression,
                "values": values,
                "bias": bias,
            }
            st.session_state.new_persona_flag = True
            st.success(f"'{label}' 인격이 추가되었습니다. (편향 계수는 자동 부여됨: {bias}) / Persona '{label}' has been added. (Bias coefficient assigned automatically: {bias})")

    st.markdown("---")
    
    # --- Informational Note / 안내 노트 ---
    st.markdown("""
    ℹ️ **Note / 참고:**
    - 생성된 인격 추출 기능은 다음 버전에 적용될 예정입니다.  
      (Exporting custom personas will be implemented in a future version.)
    - 사용자 생성 인격은 향후 LLM에 적용되어 동일 인격을 유지하며 사용할 수 있도록 확장됩니다.  
      (User-created personas will be integrated with LLMs for consistent long-term use.)
    """)

# --- Main Body UI / 본문 UI ---
st.title("🪞 MirrorMind - 인격 반응 테스트 / Persona Response Test")
situation = st.text_area("상황을 입력하세요 / Describe a situation", height=100)
response_length = st.radio(
    "응답 길이 / Response length",
    ["보통 / Medium", "길게 / Long"]
)

# --- Persona Selection Logic / 페르소나 선택 로직 ---
# If a new persona was just added, update the default selection to include it.
# 새 페르소나가 방금 추가되었다면, 기본 선택 목록에 이를 포함하도록 업데이트합니다.
if st.session_state.new_persona_flag:
    default_selection = list(initial_profiles.keys()) + [k for k in st.session_state.personas if k not in initial_profiles]
    st.session_state.new_persona_flag = False
else:
    default_selection = list(initial_profiles.keys())

# Get a list of all available personas for the multiselect widget.
# 멀티셀렉트 위젯에 사용할 수 있는 모든 페르소나 목록을 가져옵니다.
valid_personas = list(st.session_state.personas.keys())
selected_personas = st.multiselect(
    "인격 선택 / Choose personas",
    options=valid_personas,
    default=[p for p in default_selection if p in valid_personas]
)

# --- Persona Descriptions / 페르소나 설명 ---
st.caption("""
※ **재규 (Jaegyu)**: 논리적 사고가 강하고 감정 표현은 절제된 스타일입니다. / Strong logical reasoning with restrained emotional expression.
※ **유민 (Yoomin)**: 분석적이고 내성적인 성향을 가지며, 가치 기반 판단을 중요시합니다. / Analytical and introspective, prioritizes value-based judgments.
※ **현지 (Hyunji)**: 감성적이고 표현력이 뛰어나며 따뜻한 시각으로 접근합니다. / Emotional and expressive, approaches situations with a warm perspective.
""")

# --- Response Length Mapping / 응답 길이 매핑 ---
length_map = {
    "보통 / Medium": 400,
    "길게 / Long": 800
}

# --- Response Generation Function / 응답 생성 함수 ---
def generate_response(profile, text):
    """
    Generates a response from the OpenAI API based on the persona's profile.
    페르소나의 프로필을 기반으로 OpenAI API에서 응답을 생성합니다.
    """
    prompt = f"""
You are an AI persona with the following traits:
Emotion: {profile['emotion']}, Reasoning: {profile['reasoning']}, Expression: {profile['expression']}, Values: {profile['values']}, Bias: {profile['bias']}.

Based on these traits, respond to the user's situation in Korean. Your response should reflect your unique personality, matching the specified emotional and expressive style. Be consistent with your defined identity.
Situation: {text}
"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": text}
        ],
        max_tokens=length_map[response_length],
        temperature=1.0  # Higher temperature for more creative/diverse responses
    )
    return response.choices[0].message.content.strip()

# --- Generate Button and Response Display / 생성 버튼 및 응답 표시 ---
if st.button("답변 생성 / Generate Responses") and situation:
    # Check if any personas are selected.
    # 선택된 페르소나가 있는지 확인합니다.
    if not selected_personas:
        st.warning("분석할 인격을 하나 이상 선택해주세요. / Please select at least one persona to analyze.")
    else:
        # Loop through each selected persona and generate a response.
        # 선택된 각 페르소나를 순회하며 응답을 생성합니다.
        for name in selected_personas:
            if name not in st.session_state.personas:
                st.warning(f"'{name}' 인격 정보가 누락되어 답변을 생성할 수 없습니다. / Persona data for '{name}' is missing, cannot generate response.")
                continue
            
            profile = st.session_state.personas[name]
            
            # Use an expander to neatly display each response.
            # expander를 사용하여 각 응답을 깔끔하게 표시합니다.
            with st.expander(f"💬 {name}의 반응 / Response from {name}"):
                with st.spinner(f"'{name}'이(가) 생각 중... / '{name}' is thinking..."):
                    response = generate_response(profile, situation)
                    st.write(response)
