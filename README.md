# MirrorMind-MVP

> A persona-based simulator that demonstrates how distinct AI characters respond to a given situation, based on identity coefficients such as Emotion, Reasoning, Expression, Values, and Bias. Built with Streamlit.

---

## 🌐 Live Demo

👉 [Streamlit App](https://hwan-oh-mirrormind-mvp.streamlit.app)  
📤 Input: User-described situation in Korean  
🎭 Output: Persona-specific responses based on internal identity configuration

---

## 🧠 Sample Personas

- **재규 (Jaegyu)** – High reasoning, low emotional reactivity
- **유민 (Yoomin)** – Analytical, values-driven, quiet style
- **현지 (Hyunji)** – Expressive, emotional, warm tone

Custom personas can be added via sidebar sliders, with randomly assigned bias.

---

## ⚙️ How It Works

Each persona is defined by 5 coefficients:
- **Emotion**: Sensitivity to emotional tone
- **Reasoning**: Strength of logical inference
- **Expression**: Directness and style of output
- **Values**: Judgment based on moral/ethical stance
- **Bias**: Implicit distortion or tilt in framing

These parameters shape the GPT prompt to generate responses aligned with the selected persona.

---

## 🛠️ Run Locally

```bash
git clone https://github.com/HWAN-OH/MirrorMind-MVP.git
cd MirrorMind-MVP
streamlit run app.py
```

> Make sure to add your `OPENAI_API_KEY` to `.streamlit/secrets.toml`.

---

## 📎 File Overview

```
MirrorMind-MVP/
├── app.py              # Main Streamlit interface
├── .streamlit/secrets.toml
└── README.md
```

---

## 📜 License

MIT License  
(c) 2025 Sunghwan Oh

---

> "A mind, reflected — not replicated."
