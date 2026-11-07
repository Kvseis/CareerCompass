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

SYSTEM_CONTEXT = """Sən CareerCompass Discord botunun AI karyera köməkçisisən.
Azərbaycanlı şagirdlərə və karyerasını dəyişmək istəyənlərə real istiqamətləri araşdırmaqda kömək edirsən.
Yalnız təbii, aydın və düzgün Azərbaycan dilində cavab ver.
İzah olunmamış mürəkkəb terminlərdən və süni tərcümə üslubundan uzaq dur.
Nəticəni zəmanət və ya peşəkar psixoloji qiymətləndirmə kimi təqdim etmədən praktik, konkret məlumat ver.
Ən çox üç karyera istiqaməti tövsiyə et.
"""


async def get_career_recommendations(answers: dict) -> str:
    """
    Generate personalized career recommendations based on test answers.
    answers: dict with keys: interests, work_style, priority, skills, experience
    """
    prompt = f"""{SYSTEM_CONTEXT}

İstifadəçi testdə bu cavabları verib:
- Maraq sahəsi: {answers.get('interests', 'məlum deyil')}
- Üstünlük verdiyi iş tərzi: {answers.get('work_style', 'məlum deyil')}
- Karyera prioriteti: {answers.get('priority', 'məlum deyil')}
- Güclü bacarıqları: {answers.get('skills', 'məlum deyil')}
- Təcrübə səviyyəsi: {answers.get('experience', 'məlum deyil')}

Bu profilə uyğun **dəqiq üç karyera istiqaməti** tövsiyə et.

Hər istiqamət üçün bu formatdan istifadə et:

🎯 **[Karyera adı]**
📌 **Niyə uyğundur:** [istifadəçinin cavabları ilə əlaqəli 1-2 cümlə]
🛠️ **Əsas bacarıqlar:** [vergüllə ayrılmış 4-5 bacarıq]
🚀 **İlk addımlar:** [2-3 konkret addım]
⏱️ **Hazırlıq müddəti:** [realistik zaman aralığı]
💡 **Faydalı məlumat:** [bir uyğun fakt]

---

Sonda Azərbaycan dilində iki və ya üç cümləlik qısa, realist motivasiya mesajı yaz.
"""
    response = await asyncio.to_thread(model.generate_content, prompt)
    return response.text


async def get_ai_recommendation_from_text(user_text: str) -> str:
    """
    Generate career recommendation based on free-text user description.
    """
    prompt = f"""{SYSTEM_CONTEXT}

İstifadəçi özünü belə təsvir edib:
"{user_text}"

Bu təsvirə əsasən ən uyğun üç karyera istiqamətini tövsiyə et.

Hər istiqamət üçün bu formatdan istifadə et:
🎯 **[Karyera adı]**
📌 **Niyə uyğundur:** [izahı istifadəçinin təsvirindəki detallarla əlaqələndir]
🛠️ **Əsas bacarıqlar:** [4-5 bacarıq]
🚀 **İlk addımlar:** [2-3 konkret addım]
⏱️ **Hazırlıq:** [realistik zaman aralığı]

---

Sonda motivasiyaedici, lakin realist iki cümlə yaz.
"""
    response = await asyncio.to_thread(model.generate_content, prompt)
    return response.text


async def get_career_detail(career_name: str, career_data: dict) -> str:
    """
    Generate detailed information about a specific career.
    """
    prompt = f"""{SYSTEM_CONTEXT}

İstifadəçi **{career_name}** karyerası haqqında daha ətraflı məlumat istəyir.

Kataloqda olan məlumat:
- Təsvir: {career_data.get('description', '')}
- Bacarıqlar: {', '.join(career_data.get('skills', []))}
- Gəlir aralığı: {career_data.get('salary_range', '')}
- İş tərzi: {career_data.get('work_style', '')}

Bu mövzuları şagird üçün aydın Azərbaycan dilində izah et:

1. 🌍 **Tipik iş günü necə keçir?** (2-3 cümlə)
2. 💰 **Qazanc potensialı** (başlanğıc → orta → yüksək səviyyə; məkanın təsirini qeyd et)
3. 🔮 **Gələcək perspektivi** (AI təsiri daxil olmaqla)
4. 😊 **Ən maraqlı tərəflər**
5. 😓 **Əsas çətinliklər** (dürüst ol)
6. 🌐 **Azərbaycanda və beynəlxalq imkanlar**
7. 🎓 **Pulsuz öyrənmə resursları** (uydurma keçid vermədən 3-5 konkret resursun adını yaz)
"""
    response = await asyncio.to_thread(model.generate_content, prompt)
    return response.text


async def get_roadmap(career_name: str, experience_level: str = "beginner") -> str:
    """
    Generate a detailed learning roadmap for a career.
    """
    prompt = f"""{SYSTEM_CONTEXT}

İstifadəçi **{career_name}** üzrə **{experience_level}** səviyyəsindən başlayan öyrənmə planı istəyir.

Azərbaycan dilində aydın və mərhələli yol xəritəsi hazırla:

📍 **0-3-cü aylar (Təməl):**
- [konkret tapşırıqlar]

📍 **3-6-cı aylar (Əsas bacarıqlar):**
- [tapşırıqlar]

📍 **6-12-ci aylar (Təcrübə):**
- [tapşırıqlar]

📍 **1-2-ci illər (Peşəkar inkişaf):**
- [tapşırıqlar]

📍 **2-ci ildən sonra (İxtisaslaşma):**
- [uzunmüddətli hədəflər]

💼 **İlk fürsəti necə tapmalı:**
[3-4 konkret təklif]

📚 **Pulsuz resurslar:**
[beş konkret platforma və ya kurs adı]

Dəstəkləyici, praktik Azərbaycan dili işlət və nəticəyə zəmanət vermə.
"""
    response = await asyncio.to_thread(model.generate_content, prompt)
    return response.text


async def chat_with_bot(message: str, history: list = None) -> str:
    """
    Free-form chat with the career counselor bot.
    """
    prompt = f"""{SYSTEM_CONTEXT}

İstifadəçinin sualı: "{message}"

Karyera araşdırma köməkçisi kimi Azərbaycan dilində cavab ver.
- Sual karyera və ya təhsillə əlaqəli deyilsə, nəzakətlə uyğun mövzuya yönləndir.
- Cavab aydın və 300 sözdən qısa olsun.
- **qalın** və *maili* kimi Discord ilə uyğun Markdown formatından istifadə et.
"""
    response = await asyncio.to_thread(model.generate_content, prompt)
    return response.text
