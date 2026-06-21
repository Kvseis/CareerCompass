import discord
from config import COLOR_PRIMARY, COLOR_INFO, COLOR_WARNING

# ──────────────────────────────────────────────
#  TEST QUESTIONS DEFINITION
# ──────────────────────────────────────────────

QUESTIONS = [
    {
        "id": "interests",
        "text": "🌟 **Sual 1/5 — Maraq sahələri**\n\nHansı sahələr səni daha çox maraqlandırır?",
        "type": "select",
        "options": [
            ("💻 Texnologiya & Proqramlaşdırma", "tech"),
            ("🎨 Dizayn & Yaradıcılıq", "design"),
            ("🏥 Sağlamlıq & Tibb", "health"),
            ("💼 Biznes & Maliyyə", "business"),
            ("📱 Media & Kommunikasiya", "media"),
            ("🧠 Psixologiya & İnsanlarla İş", "psychology"),
            ("🔬 Elm & Tədqiqat", "science"),
            ("🌿 Ətraf Mühit & Təbiət", "environment"),
        ]
    },
    {
        "id": "work_style",
        "text": "👥 **Sual 2/5 — İş üslubu**\n\nNecə işləməyi sevirsən?",
        "type": "buttons",
        "options": [
            ("🧍 Tək işləmək", "solo", discord.ButtonStyle.primary),
            ("👥 Komanda ilə", "team", discord.ButtonStyle.secondary),
            ("🔀 Hər ikisi", "both", discord.ButtonStyle.success),
        ]
    },
    {
        "id": "priority",
        "text": "💎 **Sual 3/5 — Prioritet**\n\nSənin üçün karyerada nə daha önəmlidir?",
        "type": "select",
        "options": [
            ("💰 Yüksək maaş və maddi rifah", "money"),
            ("🎨 Yaradıcı iş, özünü ifadə", "creative"),
            ("🤝 İnsanlara kömək etmək", "helping"),
            ("🏠 Stabil, təhlükəsiz iş", "stable"),
            ("🚀 Böyümə və inkişaf imkanları", "growth"),
            ("🌍 Cəmiyyətə töhfə vermək", "impact"),
        ]
    },
    {
        "id": "skills",
        "text": "💪 **Sual 4/5 — Bacarıqlar**\n\nHansı bacarıqların daha güclüdür?",
        "type": "select",
        "options": [
            ("🧩 Analitik düşüncə, problem həlli", "analytical"),
            ("✍️ Yazma, ünsiyyət, danışma", "communication"),
            ("🎨 Yaradıcılıq, bədii zövq", "creative"),
            ("📊 Riyaziyyat, məlumat analizi", "mathematical"),
            ("🤝 İnsanlarla iş, empatiya", "interpersonal"),
            ("🔧 Texniki bacarıqlar, əl işi", "technical"),
            ("📋 Təşkilat, planlaşdırma", "organizational"),
        ]
    },
    {
        "id": "experience",
        "text": "🎓 **Sual 5/5 — Səviyyə**\n\nHazırda haradasın?",
        "type": "buttons",
        "options": [
            ("🌱 Tam başlanğıc", "beginner", discord.ButtonStyle.secondary),
            ("📚 Öyrənirəm", "learning", discord.ButtonStyle.primary),
            ("🔨 Bir az təcrübəm var", "some_exp", discord.ButtonStyle.success),
            ("💼 Karyera dəyişdirirəm", "career_change", discord.ButtonStyle.danger),
        ]
    },
]


def build_question_embed(q_index: int, username: str) -> discord.Embed:
    q = QUESTIONS[q_index]
    progress = "▓" * (q_index + 1) + "░" * (len(QUESTIONS) - q_index - 1)

    embed = discord.Embed(
        title=f"🧪 Karyera Testi  [{q_index + 1}/{len(QUESTIONS)}]",
        description=f"{q['text']}\n\n`{progress}` {q_index + 1}/{len(QUESTIONS)}",
        color=COLOR_INFO
    )
    embed.set_footer(text=f"CareerCompass • {username} üçün fərdi test")
    return embed


# ──────────────────────────────────────────────
#  SELECT MENU for questions with "select" type
# ──────────────────────────────────────────────

class QuestionSelect(discord.ui.Select):
    def __init__(self, q_index: int, answers: dict):
        q = QUESTIONS[q_index]
        options = [
            discord.SelectOption(label=label, value=value)
            for label, value in q["options"]
        ]
        super().__init__(
            placeholder="Seçimini et...",
            min_values=1,
            max_values=1,
            options=options,
            custom_id=f"test_select_{q_index}"
        )
        self.q_index = q_index
        self.answers = answers

    async def callback(self, interaction: discord.Interaction):
        q = QUESTIONS[self.q_index]
        self.answers[q["id"]] = self.values[0]
        await advance_test(interaction, self.q_index + 1, self.answers)


# ──────────────────────────────────────────────
#  BUTTON-BASED question view
# ──────────────────────────────────────────────

class QuestionButtonView(discord.ui.View):
    def __init__(self, q_index: int, answers: dict):
        super().__init__(timeout=300)
        q = QUESTIONS[q_index]
        for label, value, style in q["options"]:
            btn = AnswerButton(label=label, value=value, style=style,
                               q_index=q_index, answers=answers)
            self.add_item(btn)
        # Back button
        self.add_item(BackToMenuButton())


class AnswerButton(discord.ui.Button):
    def __init__(self, label: str, value: str, style: discord.ButtonStyle,
                 q_index: int, answers: dict):
        super().__init__(label=label, style=style)
        self.value = value
        self.q_index = q_index
        self.answers = answers

    async def callback(self, interaction: discord.Interaction):
        q = QUESTIONS[self.q_index]
        self.answers[q["id"]] = self.value
        await advance_test(interaction, self.q_index + 1, self.answers)


# ──────────────────────────────────────────────
#  SELECT VIEW
# ──────────────────────────────────────────────

class QuestionSelectView(discord.ui.View):
    def __init__(self, q_index: int, answers: dict):
        super().__init__(timeout=300)
        self.add_item(QuestionSelect(q_index, answers))
        self.add_item(BackToMenuButton())


# ──────────────────────────────────────────────
#  MAIN TEST VIEW — routes to correct type
# ──────────────────────────────────────────────

class TestView(discord.ui.View):
    """Starts the test from question 0 with empty answers."""
    def __init__(self):
        # We don't add items here — just redirect immediately
        super().__init__(timeout=1)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return True


async def advance_test(interaction: discord.Interaction, next_q: int, answers: dict):
    """Move to the next question, or show results if done."""
    if next_q >= len(QUESTIONS):
        # All questions answered → generate recommendations
        await show_loading(interaction, answers)
        return

    q = QUESTIONS[next_q]
    embed = build_question_embed(next_q, interaction.user.display_name)

    if q["type"] == "select":
        view = QuestionSelectView(next_q, answers)
    else:
        view = QuestionButtonView(next_q, answers)

    await interaction.response.edit_message(embed=embed, view=view)


async def show_loading(interaction: discord.Interaction, answers: dict):
    """Show loading state while Gemini generates recommendations."""
    loading_embed = discord.Embed(
        title="⏳ Nəticələr hazırlanır...",
        description=(
            "🤖 Gemini AI cavablarını analiz edir...\n\n"
            "Bu bir neçə saniyə çəkə bilər. Zəhmət olmasa gözlə! ⌛"
        ),
        color=COLOR_WARNING
    )
    await interaction.response.edit_message(embed=loading_embed, view=discord.ui.View())

    # Generate recommendations
    from gemini_client import get_career_recommendations
    from database import upsert_user, save_test_result
    from views.result_views import ResultView, build_result_embed

    try:
        recommendations_text = await get_career_recommendations(answers)

        # Save to DB
        upsert_user(str(interaction.user.id), interaction.user.display_name)
        save_test_result(str(interaction.user.id), answers, [recommendations_text])

        embed = build_result_embed(recommendations_text, interaction.user.display_name)
        view = ResultView(answers=answers)
        await interaction.edit_original_response(embed=embed, view=view)

    except Exception as e:
        print(f"[FALLBACK] Recommendation API error: {e}")
        try:
            import json
            import os
            data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "career_data.json")
            with open(data_path, "r", encoding="utf-8") as f:
                career_data = json.load(f)

            interest = answers.get("interests", "tech")
            careers = career_data.get(interest, [])
            if not careers:
                careers = career_data.get("tech", [])

            recommendations_text = "🤖 **Yerli Məlumat Bazası (Lokal Analiz):**\n\n"
            recommendations_text += "Cavablarınız əsasında sizə tövsiyə olunan karyera istiqamətləri:\n\n"
            for c in careers[:3]:
                recommendations_text += f"🎯 **{c['name']}**\n"
                recommendations_text += f"📌 **Təsvir:** {c['description']}\n"
                recommendations_text += f"🛠️ **Əsas bacarıqlar:** {', '.join(c['skills'])}\n"
                recommendations_text += f"🚀 **İlk addım:** {c['roadmap'][0]}\n\n"
            recommendations_text += "---\n\nUğurlar! Addım-addım hədəflərinizə doğru irəliləyin."

            # Save to DB
            upsert_user(str(interaction.user.id), interaction.user.display_name)
            save_test_result(str(interaction.user.id), answers, [recommendations_text])

            embed = build_result_embed(recommendations_text, interaction.user.display_name)
            embed.set_footer(text=f"CareerCompass 🧭 • Yerli bazadan (Lokal) • {interaction.user.display_name} üçün fərdi test")
            view = ResultView(answers=answers)
            await interaction.edit_original_response(embed=embed, view=view)

        except Exception as fallback_err:
            print(f"[CRITICAL] Recommendation Fallback error: {fallback_err}")
            error_embed = discord.Embed(
                title="❌ Xəta baş verdi",
                description=f"Gemini API ilə əlaqə qurarkən xəta: `{str(e)[:200]}`\n\nZəhmət olmasa yenidən cəhd et.",
                color=0xE74C3C
            )
            view = discord.ui.View()
            retry_btn = discord.ui.Button(label="🔄 Yenidən Cəhd Et", style=discord.ButtonStyle.danger)

            async def retry_callback(i: discord.Interaction):
                await show_loading(i, answers)

            retry_btn.callback = retry_callback
            view.add_item(retry_btn)
            await interaction.edit_original_response(embed=error_embed, view=view)


# ──────────────────────────────────────────────
#  SHARED BACK BUTTON
# ──────────────────────────────────────────────

class BackToMenuButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="← Ana Menyu", emoji="🏠", style=discord.ButtonStyle.secondary, row=4)

    async def callback(self, interaction: discord.Interaction):
        from views.main_menu import MainMenuView, build_greeting_embed
        embed = build_greeting_embed(interaction.user.display_name)
        view = MainMenuView()
        await interaction.response.edit_message(embed=embed, view=view)
