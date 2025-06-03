import openai
import os

def generate_response(profile, situation, max_tokens=300):
    system_msg = {
        "현지 (Hyunji)": "이 인격은 부드럽고 섬세한 시각을 가졌으며, 공감능력이 뛰어납니다.",
        "유민 (Yumin)": "이 인격은 냉철하고 분석적이며, 리더십과 추진력이 강합니다.",
        "재규 (Jaegyu)": "이 인격은 유머 감각이 뛰어나고, 다소 가볍지만 솔직한 관점을 가졌습니다."
    }

    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_msg.get(profile, "")},
            {"role": "user", "content": f"상황: {situation}\n이 인격의 시각에서 생각과 반응을 알려줘."}
        ],
        temperature=1.0,
        max_tokens=max_tokens
    )

    return response.choices[0].message.content