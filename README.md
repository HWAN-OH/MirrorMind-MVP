# MirrorMind-MVP

> A persona-based simulator that demonstrates how distinct AI characters respond to a given situation, based on identity coefficients such as Emotion, Reasoning, Expression, Values, and Bias. Built with Streamlit.
> 
> 주어진 상황에 대해 감정, 사고, 표현, 가치, 편향과 같은 정체성 계수를 기반으로 서로 다른 AI 페르소나가 어떻게 반응하는지 시뮬레이션하는 페르소나 기반 시뮬레이터입니다. Streamlit으로 제작되었습니다.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://hwan-oh-mirrormind-mvp.streamlit.app)

---

## 🌐 Live Demo / 라이브 데모

👉 [Streamlit App 바로가기](https://hwan-oh-mirrormind-mvp.streamlit.app)  
📤 **Input / 입력**: User-described situation in Korean / 사용자가 한국어로 상황을 입력  
🎭 **Output / 출력**: Persona-specific responses based on internal identity configuration / 내부 정체성 설정에 따른 페르소나별 응답

---

## ✨ Features / 주요 기능

* **Dynamic Persona Generation / 동적 페르소나 생성**: Create and customize your own AI personas by adjusting five core identity traits. / 5가지 핵심 정체성 특성을 조정하여 자신만의 AI 페르소나를 만들고 커스터마이징할 수 있습니다.
* **Real-time Response Simulation / 실시간 반응 시뮬레이션**: Instantly see how different personas would react to any given situation. / 주어진 상황에 대해 여러 페르소나가 어떻게 다르게 반응하는지 즉시 확인할 수 있습니다.
* **Pre-configured Sample Personas / 사전 설정된 샘플 페르소나**: Comes with three distinct, ready-to-use personas (Jaegyu, Yoomin, Hyunji). / 즉시 사용 가능한 개성 있는 3개의 페르소나(재규, 유민, 현지)가 기본으로 제공됩니다.
* **Customizable Response Length / 응답 길이 조절**: Choose between medium and long responses to fit your needs. / 필요에 따라 '보통' 또는 '길게' 두 가지 응답 길이 중 선택할 수 있습니다.

---

## 🧠 Sample Personas / 샘플 페르소나

- **재규 (Jaegyu)** – High reasoning, low emotional reactivity / 논리적 사고가 강하고 감정적 반응성이 낮음
- **유민 (Yoomin)** – Analytical, values-driven, quiet style / 분석적이고 가치 중심적이며 내향적인 스타일
- **현지 (Hyunji)** – Expressive, emotional, warm tone / 표현력이 풍부하고 감성적이며 따뜻한 톤

> Custom personas can be added via sidebar sliders, with a randomly assigned bias coefficient. / 사이드바의 슬라이더를 통해 커스텀 페르소나를 추가할 수 있으며, 편향 계수는 무작위로 할당됩니다.

---

## ⚙️ How It Works / 작동 방식

Each persona is defined by 5 coefficients that shape its identity. / 각 페르소나는 정체성을 형성하는 5가지 계수로 정의됩니다.

- **Emotion / 감정**: Sensitivity to emotional tone and context. / 감정적인 톤과 맥락에 대한 민감도.
- **Reasoning / 사고**: Strength of logical inference and analytical thinking. / 논리적 추론 및 분석적 사고의 강도.
- **Expression / 표현**: Directness and style of the generated output. / 생성되는 결과물의 직설성과 스타일.
- **Values / 가치**: Judgment based on a moral or ethical stance. / 도덕적 또는 윤리적 입장에 기반한 판단.
- **Bias / 편향**: Implicit distortion or tilt in framing and perspective. / 프레이밍과 관점에서의 내재된 왜곡 또는 경향성.

These parameters are inserted into a system prompt for a GPT model, which then generates a response aligned with the selected persona's unique characteristics. / 이 파라미터들은 GPT 모델의 시스템 프롬프트에 삽입되어, 선택된 페르소나의 고유한 특성에 맞는 응답을 생성하도록 유도합니다.

---

## 🚀 Future Plans / 향후 계획

- **Persona Export/Import / 페르소나 내보내기/가져오기**: Allow users to save their custom personas and load them in future sessions. / 사용자가 생성한 페르소나를 저장하고 나중에 다시 불러올 수 있는 기능을 추가할 예정입니다.
- **Long-term Memory / 장기 기억**: Enable personas to remember past interactions for consistent and evolving conversations. / 페르소나가 과거의 상호작용을 기억하여 일관성 있고 발전적인 대화를 나눌 수 있도록 기능을 확장할 계획입니다.
- **Advanced Model Integration / 고급 모델 통합**: Integrate more sophisticated language models to enhance response quality and persona depth. / 더 정교한 언어 모델을 통합하여 응답의 품질과 페르소나의 깊이를 향상시킬 것입니다.

---

## 🛠️ Run Locally / 로컬에서 실행하기

```bash
# 1. Clone the repository / 리포지토리 복제
git clone [https://github.com/HWAN-OH/MirrorMind-MVP.git](https://github.com/HWAN-OH/MirrorMind-MVP.git)

# 2. Navigate to the project directory / 프로젝트 디렉토리로 이동
cd MirrorMind-MVP

# 3. Install dependencies / 의존성 설치
pip install -r requirements.txt

# 4. Run the Streamlit app / Streamlit 앱 실행
streamlit run app.py
