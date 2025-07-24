import streamlit as st
from openai import OpenAI
import json
import random

# --- Page Configuration / 페이지 설정 ---
# Set the page title and layout. / 페이지 제목과 레이아웃을 설정합니다.
st.set_page_config(page_title="MirrorMind MVP 0.3", layout="wide")

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
            bias = round(random.uniform(1.0, 5.0), 2)
            label = f"{name.strip()} (Custom)"
            st.session_state.personas[label] = {
                "emotion": emotion, "reasoning": reasoning, "expression": expression,
                "values": values, "bias": bias
            }
            st.session_state.new_persona_flag = True
            st.success(f"'{label}' 인격이 추가되었습니다. (편향 계수 자동 부여됨: {bias}) / Persona '{label}' has been added.")

    st.markdown("---")

    # --- Persona Import/Export Section / 인격 관리 섹션 ---
    st.header("📂 인격 관리 / Manage Personas")

    # --- Persona Importer / 인격 가져오기 ---
    st.subheader("인격 가져오기 / Import Personas")
    uploaded_file = st.file_uploader(
        "저장된 인격(.json) 파일을 업로드하세요 / Upload a persona (.json) file",
        type="json"
    )
    if uploaded_file is not None:
        try:
            imported_data = json.load(uploaded_file)
            if isinstance(imported_data, dict):
                count = 0
                for name, profile in imported_data.items():
                    if all(key in profile for key in ["emotion", "reasoning", "expression", "values", "bias"]):
                        st.session_state.personas[name] = profile
                        count += 1
                    else:
                        st.warning(f"'{name}' 데이터 형식이 올바르지 않아 건너뜁니다. / Skipping '{name}' due to incorrect data format.")
                if count > 0:
                    st.success(f"{count}개의 인격을 성공적으로 가져왔습니다! / Successfully imported {count} personas!")
                    st.session_state.new_persona_flag = True
            else:
                st.error("업로드된 파일이 올바른 인격 데이터 형식이 아닙니다. / The uploaded file is not in the correct format.")
        except Exception as e:
            st.error(f"파일 처리 중 오류가 발생했습니다: {e} / An error occurred while processing the file: {e}")

    # --- Persona Exporter / 인격 내보내기 ---
    st.subheader("인격 내보내기 / Export Personas")
    custom_personas = {name: profile for name, profile in st.session_state.personas.items() if "(Custom)" in name}

    if not custom_personas:
        st.info("내보낼 커스텀 인격이 없습니다. / No custom personas to export.")
    else:
        personas_to_export = st.multiselect(
            "내보낼 커스텀 인격 선택 / Select custom personas to export",
            options=list(custom_personas.keys()),
            default=list(custom_personas.keys())
        )
        if personas_to_export:
            export_data = {name: st.session_state.personas[name] for name in personas_to_export}
            json_string = json.dumps(export_data, indent=4, ensure_ascii=False)
            st.download_button(
                label="선택한 인격 다운로드 (.json) / Download Selected (.json)",
                data=json_string,
                file_name="mirrormind_personas.json",
                mime="application/json",
            )

# --- Main Body UI / 본문 UI ---
st.title("🪞 MirrorMind - 인격 반응 테스트 / Persona Response Test")
situation = st.text_area("상황을 입력하세요 / Describe a situation", height=100)
response_length = st.radio(
    "응답 길이 / Response length",
    ["보통 / Medium", "길게 / Long"]
)

if st.session_state.new_persona_flag:
    default_selection = list(st.session_state.personas.keys())
    st.session_state.new_persona_flag = False
else:
    default_selection = list(initial_profiles.keys())

valid_personas = list(st.session_state.personas.keys())
selected_personas = st.multiselect(
    "인격 선택 / Choose personas",
    options=valid_personas,
    default=[p for p in default_selection if p in valid_personas]
)

st.caption("""
※ **재규 (Jaegyu)**: 논리적 사고가 강하고 감정 표현은 절제된 스타일입니다. / Strong logical reasoning with restrained emotional expression.
※ **유민 (Yoomin)**: 분석적이고 내성적인 성향을 가지며, 가치 기반 판단을 중요시합니다. / Analytical and introspective, prioritizes value-based judgments.
※ **현지 (Hyunji)**: 감성적이고 표현력이 뛰어나며 따뜻한 시각으로 접근합니다. / Emotional and expressive, approaches situations with a warm perspective.
""")

length_map = {"보통 / Medium": 400, "길게 / Long": 800}

def generate_response(profile, text):
    prompt = f"""
You are an AI persona with the following traits:
Emotion: {profile['emotion']}, Reasoning: {profile['reasoning']}, Expression: {profile['expression']}, Values: {profile['values']}, Bias: {profile['bias']}.
Based on these traits, respond to the user's situation in Korean. Your response should reflect your unique personality, matching the specified emotional and expressive style. Be consistent with your defined identity.
Situation: {text}
"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}, {"role": "user", "content": text}],
        max_tokens=length_map[response_length],
        temperature=1.0
    )
    return response.choices[0].message.content.strip()

if st.button("답변 생성 / Generate Responses") and situation:
    if not selected_personas:
        st.warning("분석할 인격을 하나 이상 선택해주세요. / Please select at least one persona to analyze.")
    else:
        for name in selected_personas:
            if name not in st.session_state.personas:
                st.warning(f"'{name}' 인격 정보가 누락되어 답변을 생성할 수 없습니다. / Persona data for '{name}' is missing.")
                continue
            profile = st.session_state.personas[name]
            with st.expander(f"💬 {name}의 반응 / Response from {name}"):
                with st.spinner(f"'{name}'이(가) 생각 중... / '{name}' is thinking..."):
                    response = generate_response(profile, situation)
                    st.write(response)
