import google.generativeai as genai
import asyncio
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

# Use gemini-2.5-flash with thinking disabled for fast, direct answers and token efficiency
generation_config = {
    "temperature": 0.7,
}
model = genai.GenerativeModel(
    "gemini-2.5-flash",
    generation_config=generation_config,
)

SYSTEM_CONTEXT = """You are the AI counselor inside the CareerCompass Discord bot.
You help students and career changers explore realistic career directions.
Write in clear, supportive English and avoid unexplained jargon.
Give practical, specific guidance without presenting the result as a guarantee or a professional assessment.
Recommend no more than three career paths.
"""


async def get_career_recommendations(answers: dict) -> str:
    """
    Generate personalized career recommendations based on test answers.
    answers: dict with keys: interests, work_style, priority, skills, experience
    """
    prompt = f"""{SYSTEM_CONTEXT}

The user submitted these assessment answers:
- Interest area: {answers.get('interests', 'unknown')}
- Preferred work style: {answers.get('work_style', 'unknown')}
- Career priority: {answers.get('priority', 'unknown')}
- Strongest skills: {answers.get('skills', 'unknown')}
- Experience level: {answers.get('experience', 'unknown')}

Recommend **exactly three career paths** that fit this profile.

Use this format for each path:

🎯 **[Career Name]**
📌 **Why it fits:** [1-2 sentences tied to the user's answers]
🛠️ **Core skills:** [4-5 comma-separated skills]
🚀 **First steps:** [2-3 concrete actions]
⏱️ **Preparation time:** [a realistic range]
💡 **Useful insight:** [one relevant fact]

---

Finish with a short, grounded encouragement message of two or three sentences.
"""
    response = await asyncio.to_thread(model.generate_content, prompt)
    return response.text


async def get_ai_recommendation_from_text(user_text: str) -> str:
    """
    Generate career recommendation based on free-text user description.
    """
    prompt = f"""{SYSTEM_CONTEXT}

The user described themselves as follows:
"{user_text}"

Recommend the three most suitable career directions based on this description.

Use this format for each path:
🎯 **[Career Name]**
📌 **Why it fits:** [connect the explanation to details in the description]
🛠️ **Core skills:** [4-5 skills]
🚀 **First steps:** [2-3 concrete actions]
⏱️ **Preparation:** [a realistic range]

---

Finish with two encouraging but realistic sentences.
"""
    response = await asyncio.to_thread(model.generate_content, prompt)
    return response.text


async def get_career_detail(career_name: str, career_data: dict) -> str:
    """
    Generate detailed information about a specific career.
    """
    prompt = f"""{SYSTEM_CONTEXT}

The user wants a deeper explanation of a career in **{career_name}**.

Available catalog data:
- Description: {career_data.get('description', '')}
- Skills: {', '.join(career_data.get('skills', []))}
- Salary range: {career_data.get('salary_range', '')}
- Work style: {career_data.get('work_style', '')}

Explain these topics in clear, student-friendly English:

1. 🌍 **What does a typical day look like?** (2-3 sentences)
2. 💰 **Earning potential** (entry → mid-level → senior; note that location matters)
3. 🔮 **Future outlook** (including the effect of AI)
4. 😊 **Most rewarding aspects**
5. 😓 **Common challenges** (be candid)
6. 🌐 **International and local opportunities**
7. 🎓 **Free learning resources** (name 3-5 concrete resources without inventing links)
"""
    response = await asyncio.to_thread(model.generate_content, prompt)
    return response.text


async def get_roadmap(career_name: str, experience_level: str = "beginner") -> str:
    """
    Generate a detailed learning roadmap for a career.
    """
    prompt = f"""{SYSTEM_CONTEXT}

The user wants a learning roadmap for **{career_name}**, starting at the **{experience_level}** level.

Create a clear, step-by-step roadmap:

📍 **Months 0-3 (Foundations):**
- [concrete tasks]

📍 **Months 3-6 (Core skills):**
- [tasks]

📍 **Months 6-12 (Practice):**
- [tasks]

📍 **Years 1-2 (Professional growth):**
- [tasks]

📍 **Year 2+ (Specialization):**
- [long-term goals]

💼 **How to find a first opportunity:**
[3-4 concrete suggestions]

📚 **Free resources:**
[five concrete platform or course names]

Use supportive, practical English and avoid promising a guaranteed outcome.
"""
    response = await asyncio.to_thread(model.generate_content, prompt)
    return response.text


async def chat_with_bot(message: str, history: list = None) -> str:
    """
    Free-form chat with the career counselor bot.
    """
    prompt = f"""{SYSTEM_CONTEXT}

The user asks: "{message}"

Respond as a career exploration assistant.
- If the question is unrelated to careers or education, politely redirect it.
- Keep the answer clear and under 300 words.
- Use Discord-compatible Markdown such as **bold** and *italics*.
"""
    response = await asyncio.to_thread(model.generate_content, prompt)
    return response.text

