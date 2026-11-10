import discord
from config import COLOR_PRIMARY, COLOR_INFO, COLOR_WARNING

# ──────────────────────────────────────────────
#  TEST QUESTIONS DEFINITION
# ──────────────────────────────────────────────

QUESTIONS = [
    {
        "id": "interests",
        "text": "🌟 **Question 1/5 — Interests**\n\nWhich areas interest you most?",
        "type": "select",
        "options": [
            ("💻 Technology & Programming", "tech"),
            ("🎨 Design & Creativity", "design"),
            ("🏥 Health & Medicine", "health"),
            ("💼 Business & Finance", "business"),
            ("📱 Media & Communication", "media"),
            ("🧠 Psychology & People", "psychology"),
            ("🔬 Science & Research", "science"),
            ("🌿 Environment & Nature", "environment"),
        ]
    },
    {
        "id": "work_style",
        "text": "👥 **Question 2/5 — Work style**\n\nHow do you prefer to work?",
        "type": "buttons",
        "options": [
            ("🧍 Independently", "solo", discord.ButtonStyle.primary),
            ("👥 With a team", "team", discord.ButtonStyle.secondary),
            ("🔀 A mix of both", "both", discord.ButtonStyle.success),
        ]
    },
    {
        "id": "priority",
        "text": "💎 **Question 3/5 — Priority**\n\nWhat matters most to you in a career?",
        "type": "select",
        "options": [
            ("💰 Strong earning potential", "money"),
            ("🎨 Creativity and expression", "creative"),
            ("🤝 Helping people", "helping"),
            ("🏠 Stability and security", "stable"),
            ("🚀 Growth and learning", "growth"),
            ("🌍 Positive social impact", "impact"),
        ]
    },
    {
        "id": "skills",
        "text": "💪 **Question 4/5 — Strengths**\n\nWhich skills feel strongest to you?",
        "type": "select",
        "options": [
            ("🧩 Analytical thinking & problem-solving", "analytical"),
            ("✍️ Writing & communication", "communication"),
            ("🎨 Creativity & visual thinking", "creative"),
            ("📊 Mathematics & data analysis", "mathematical"),
            ("🤝 Empathy & working with people", "interpersonal"),
            ("🔧 Technical & hands-on skills", "technical"),
            ("📋 Organization & planning", "organizational"),
        ]
    },
    {
        "id": "experience",
        "text": "🎓 **Question 5/5 — Experience**\n\nWhere are you in your journey?",
        "type": "buttons",
        "options": [
            ("🌱 Complete beginner", "beginner", discord.ButtonStyle.secondary),
            ("📚 Currently learning", "learning", discord.ButtonStyle.primary),
            ("🔨 Some practical experience", "some_exp", discord.ButtonStyle.success),
            ("💼 Changing careers", "career_change", discord.ButtonStyle.danger),
        ]
    },
]


def build_question_embed(q_index: int, username: str) -> discord.Embed:
    q = QUESTIONS[q_index]
    progress = "▓" * (q_index + 1) + "░" * (len(QUESTIONS) - q_index - 1)

    embed = discord.Embed(
        title=f"🧪 Career Assessment  [{q_index + 1}/{len(QUESTIONS)}]",
        description=f"{q['text']}\n\n`{progress}` {q_index + 1}/{len(QUESTIONS)}",
        color=COLOR_INFO
    )
    embed.set_footer(text=f"CareerCompass • Personalized assessment for {username}")
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
            placeholder="Choose an answer...",
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
        title="⏳ Preparing your results...",
        description=(
            "🤖 Gemini is analyzing your answers.\n\n"
            "This may take a few seconds. Thanks for your patience. ⌛"
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
            from services.career_catalog import recommend_from_answers
            careers = recommend_from_answers(answers, limit=3)

            recommendations_text = "🤖 **Local catalog recommendation:**\n\n"
            recommendations_text += "Based on your answers, consider these career directions:\n\n"
            for c in careers[:3]:
                recommendations_text += f"🎯 **{c['name']}**\n"
                recommendations_text += f"📌 **Overview:** {c['description']}\n"
                recommendations_text += f"🛠️ **Core skills:** {', '.join(c['skills'])}\n"
                recommendations_text += f"🚀 **First step:** {c['roadmap'][0]}\n\n"
            recommendations_text += "---\n\nUse these suggestions as a starting point, then research and test each path through small projects."

            # Save to DB
            upsert_user(str(interaction.user.id), interaction.user.display_name)
            save_test_result(str(interaction.user.id), answers, [recommendations_text])

            embed = build_result_embed(recommendations_text, interaction.user.display_name)
            embed.set_footer(text=f"CareerCompass 🧭 • Local catalog • Personalized for {interaction.user.display_name}")
            view = ResultView(answers=answers)
            await interaction.edit_original_response(embed=embed, view=view)

        except Exception as fallback_err:
            print(f"[CRITICAL] Recommendation Fallback error: {fallback_err}")
            error_embed = discord.Embed(
                title="❌ Results unavailable",
                description="Neither the AI service nor the local catalog could complete this request. Please try again.",
                color=0xE74C3C
            )
            view = discord.ui.View()
            retry_btn = discord.ui.Button(label="🔄 Try Again", style=discord.ButtonStyle.danger)

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
        super().__init__(label="← Main Menu", emoji="🏠", style=discord.ButtonStyle.secondary, row=4)

    async def callback(self, interaction: discord.Interaction):
        from views.main_menu import MainMenuView, build_greeting_embed
        embed = build_greeting_embed(interaction.user.display_name)
        view = MainMenuView()
        await interaction.response.edit_message(embed=embed, view=view)

