import openai
import os

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_response(profile, situation):
    content = f"""
당신은 다음과 같은 인격을 가진 존재입니다:
감정: {profile['감정']}
사고: {profile['사고']}
표현: {profile['표현']}
가치: {profile['가치']}
편향: {profile['편향']}

아래 상황에 대한 당신의 반응을 표현해주세요:
"""{situation}"""
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": content}],
        temperature=1.0,
        max_tokens=300
    )
    return response.choices[0].message.content.strip()