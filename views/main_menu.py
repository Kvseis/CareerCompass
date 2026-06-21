import discord
from config import COLOR_PRIMARY


class MainMenuView(discord.ui.View):
    """Ana menyu — 3 əsas düymə."""

    def __init__(self):
        super().__init__(timeout=300)

    @discord.ui.button(
        label="Testə Başla",
        emoji="🎯",
        style=discord.ButtonStyle.primary,
        custom_id="main_test"
    )
    async def test_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        from views.test_views import QuestionSelectView, QuestionButtonView, build_question_embed, QUESTIONS
        q = QUESTIONS[0]
        if q["type"] == "select":
            view = QuestionSelectView(0, {})
        else:
            view = QuestionButtonView(0, {})
        embed = build_question_embed(0, interaction.user.display_name)
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(
        label="Karyera Kəşf Et",
        emoji="🔎",
        style=discord.ButtonStyle.secondary,
        custom_id="main_explore"
    )
    async def explore_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        from views.explore_views import ExploreView, build_explore_embed
        embed = build_explore_embed()
        view = ExploreView()
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(
        label="Mənə Tövsiyə Ver",
        emoji="📊",
        style=discord.ButtonStyle.success,
        custom_id="main_recommend"
    )
    async def recommend_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="📊 AI Tövsiyə Sistemi",
            description=(
                "Özün haqqında bir neçə cümlə yaz — maraqların, bacarıqların, "
                "nə istədiyin.\n\n"
                "**Məsələn:** *'Mən yaradıcı işlər sevirəm, insanlarla ünsiyyət "
                "qurmağı sevirəm, texnologiyaya marağım var amma kod yazmağı bilmirəm...'*\n\n"
                "💬 Cavabı bu kanalda **mətn mesajı** olaraq göndər!"
            ),
            color=COLOR_PRIMARY
        )
        embed.set_footer(text="CareerCompass AI 🤖 • Gemini 2.0 ilə işləyir")
        view = WaitingForTextView()
        await interaction.response.edit_message(embed=embed, view=view)


class WaitingForTextView(discord.ui.View):
    """Geri dön düyməsi."""
    def __init__(self):
        super().__init__(timeout=300)

    @discord.ui.button(label="← Geri", emoji="↩️", style=discord.ButtonStyle.secondary)
    async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        from cogs.welcome import build_greeting_embed
        embed = build_greeting_embed(interaction.user.display_name)
        view = MainMenuView()
        await interaction.response.edit_message(embed=embed, view=view)


def build_greeting_embed(username: str) -> discord.Embed:
    embed = discord.Embed(
        title="👋 Salam! Mən CareerCompass-ım!",
        description=(
            f"**Xoş gəldin, {username}!** 🎉\n\n"
            "Mən sənin gələcəyin üçün **doğru karyera yolunu** tapmağa kömək edən "
            "AI köməkçiyəm.\n\n"
            "Sənə uyğun karyera yollarını tapmaq üçün qısa bir test edək, "
            "yoxsa birbaşa sahələri kəşf etmək istəyirsən?\n\n"
            "⬇️ **Aşağıdan seçimini et:**"
        ),
        color=COLOR_PRIMARY
    )
    embed.add_field(
        name="🎯 Testə Başla",
        value="5 sual, 2 dəqiqə → fərdi tövsiyə",
        inline=True
    )
    embed.add_field(
        name="🔎 Karyera Kəşf Et",
        value="6 sahə → yüzlərlə karyera",
        inline=True
    )
    embed.add_field(
        name="📊 Mənə Tövsiyə Ver",
        value="Özün haqqında yaz → AI analiz edir",
        inline=True
    )
    embed.set_footer(text="CareerCompass v1.0 🧭 • Gemini 2.0 ilə işləyir")
    embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/🧭")
    return embed
