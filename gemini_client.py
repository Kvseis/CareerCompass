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

SYSTEM_CONTEXT = """Sen CareerCompass Discord botunun AI komekcisisən.
Sən genclərin ve karyerasini deyişmek isteyen boyuklərin karyera yolu tapmasina kömek edirsən.
Cavablarini Azerbaycan turkcesindem verir, genc, dostcasina, motivasiyaverici uslubda danişirsan.
Murekkeb jarqon isletmirsən. Konkret, praktik, real melumat verirsən.
Maksimum 3 karyera tovsiye edirsən.
"""


async def get_career_recommendations(answers: dict) -> str:
    """
    Generate personalized career recommendations based on test answers.
    answers: dict with keys: interests, work_style, priority, skills, experience
    """
    prompt = f"""{SYSTEM_CONTEXT}

İstifadəçi aşağıdakı cavabları verdi:
- Maraq sahəsi: {answers.get('interests', 'bilinmir')}
- İş üslubu: {answers.get('work_style', 'bilinmir')}
- Prioritet: {answers.get('priority', 'bilinmir')}
- Güclü bacarıqlar: {answers.get('skills', 'bilinmir')}
- Təcrübə/səviyyə: {answers.get('experience', 'bilinmir')}

Bu istifadəçiyə uyğun **dəqiq 3 karyera** tövsiyə et.

Hər karyera üçün aşağıdakı formatda yaz (emoji işlət, Azərbaycan dilindən):

🎯 **[Karyera Adı]**
📌 **Niyə uyğundur:** [1-2 cümlə, bu insanın cavablarına uyğun izah]
🛠️ **Əsas bacarıqlar:** [vergüllə ayrılmış 4-5 bacarıq]
🚀 **Başlama yolu:** [2-3 konkret ilk addım]
⏱️ **Hazırlıq müddəti:** [realistik müddət]
💡 **Maraqlı fakt:** [bir maraqlı məlumat]

---

Cavabın sonunda qısa bir motivasiya mesajı yaz (2-3 cümlə).
"""
    response = await asyncio.to_thread(model.generate_content, prompt)
    return response.text


async def get_ai_recommendation_from_text(user_text: str) -> str:
    """
    Generate career recommendation based on free-text user description.
    """
    prompt = f"""{SYSTEM_CONTEXT}

İstifadəçi özünü belə təsvir etdi:
"{user_text}"

Bu mətnə əsasən onun üçün ən uyğun 3 karyera tövsiyə et.

Hər karyera üçün format:
🎯 **[Karyera Adı]**
📌 **Niyə uyğundur:** [izah - bu şəxsin sözlərindən nümunə gətir]
🛠️ **Əsas bacarıqlar:** [4-5 bacarıq]
🚀 **İlk addım:** [2-3 konkret addım]
⏱️ **Hazırlıq:** [müddət]

---

Sonda istifadəçini həvəsləndirən 2 cümlə yaz.
"""
    response = await asyncio.to_thread(model.generate_content, prompt)
    return response.text


async def get_career_detail(career_name: str, career_data: dict) -> str:
    """
    Generate detailed information about a specific career.
    """
    prompt = f"""{SYSTEM_CONTEXT}

İstifadəçi **{career_name}** karyerası haqqında daha ətraflı məlumat istəyir.

Mövcud məlumat:
- Sahə: {career_data.get('description', '')}
- Bacarıqlar: {', '.join(career_data.get('skills', []))}
- Maaş aralığı: {career_data.get('salary_range', '')}
- İş üslubu: {career_data.get('work_style', '')}

Aşağıdakı mövzularda ətraflı, gəncə uyğun dildə izah et:

1. 🌍 **Gündəlik iş həyatı necədir?** (2-3 cümlə)
2. 💰 **Pul qazanma potensialı** (başlanğıc → orta → senior)
3. 🔮 **Gələcəyi necədir?** (AI dövrü, trend)
4. 😊 **Bu karyeranın ən gözəl tərəfi nədir?**
5. 😓 **Çətin tərəfləri?** (dürüst ol)
6. 🌐 **Azərbaycanda bu sahənin vəziyyəti**
7. 🎓 **Pulsuz öyrənmə resursları** (3-5 konkret resurs, link olmadan ad yaz)
"""
    response = await asyncio.to_thread(model.generate_content, prompt)
    return response.text


async def get_roadmap(career_name: str, experience_level: str = "başlanğıc") -> str:
    """
    Generate a detailed learning roadmap for a career.
    """
    prompt = f"""{SYSTEM_CONTEXT}

İstifadəçi **{career_name}** sahəsində **{experience_level}** səviyyəsindən başlayaraq karyera yolu xəritəsi istəyir.

Aydın, addım-addım yol xəritəsi hazırla:

📍 **0-3 Ay (Başlanğıc):**
- [konkret tapşırıqlar]

📍 **3-6 Ay (Əsaslar):**
- [tapşırıqlar]

📍 **6-12 Ay (Praktika):**
- [tapşırıqlar]

📍 **1-2 İl (Peşəkar):**
- [tapşırıqlar]

📍 **2+ İl (Expert):**
- [uzunmüddətli hədəflər]

💼 **İlk işi necə tapmaq:**
[3-4 konkret tövsiyə]

📚 **Pulsuz resurslar:**
[5 konkret platforma/kurs adı]

Azərbaycan dilindən yaz, motivasiyaverici ton işlət.
"""
    response = await asyncio.to_thread(model.generate_content, prompt)
    return response.text


async def chat_with_bot(message: str, history: list = None) -> str:
    """
    Free-form chat with the career counselor bot.
    """
    prompt = f"""{SYSTEM_CONTEXT}

İstifadəçi sənə bu sualı verir: "{message}"

Karyera məsləhətçisi kimi cavab ver.
- Əgər karyera ilə əlaqəli sual deyilsə, mehriban şəkildə karyera mövzusuna yönləndir.
- Cavabın qısa, aydın olsun (max 300 söz).
- Discord formatına uyğun yazı işlət (**qalın**, *italic*).
"""
    response = await asyncio.to_thread(model.generate_content, prompt)
    return response.text
