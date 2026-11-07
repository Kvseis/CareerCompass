import discord
from config import COLOR_PRIMARY


class MainMenuView(discord.ui.View):
    """Main navigation with the three primary user journeys."""

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
        label="Karyeraları Araşdır",
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
        label="Tövsiyə Al",
        emoji="📊",
        style=discord.ButtonStyle.success,
        custom_id="main_recommend"
    )
    async def recommend_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="📊 AI Tövsiyəsi",
            description=(
                "`/recommend` komandasından istifadə et və maraqlarını, güclü "
                "tərəflərini, hədəflərini bir neçə cümlə ilə təsvir et.\n\n"
                "**Nümunə:** *Yaradıcı işləri və insanlarla əməkdaşlığı sevirəm. "
                "Texnologiya ilə maraqlanıram, amma proqramlaşdırmanı yeni öyrənirəm.*\n\n"
                "CareerCompass təsvirinə əsasən üç praktik istiqamət təqdim edəcək."
            ),
            color=COLOR_PRIMARY
        )
        embed.set_footer(text="CareerCompass AI 🤖 • Gemini 2.5 Flash ilə işləyir")
        view = WaitingForTextView()
        await interaction.response.edit_message(embed=embed, view=view)


class WaitingForTextView(discord.ui.View):
    """Return navigation for the recommendation instructions."""
    def __init__(self):
        super().__init__(timeout=300)

    @discord.ui.button(label="← Geri", emoji="↩️", style=discord.ButtonStyle.secondary)
    async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = build_greeting_embed(interaction.user.display_name)
        view = MainMenuView()
        await interaction.response.edit_message(embed=embed, view=view)


def build_greeting_embed(username: str) -> discord.Embed:
    embed = discord.Embed(
        title="👋 Salam! Mən CareerCompass-am.",
        description=(
            f"**Xoş gəldin, {username}!** 🎉\n\n"
            "Maraqlarına və hədəflərinə uyğun **karyera istiqamətlərini araşdırmağa** "
            "kömək edən AI köməkçiyəm.\n\n"
            "Qısa testi tamamla, sahələri araşdır və ya fərdi tövsiyə üçün özünü təsvir et.\n\n"
            "⬇️ **Başlamaq üçün seçim et:**"
        ),
        color=COLOR_PRIMARY
    )
    embed.add_field(
        name="🎯 Testə Başla",
        value="5 sual, təxminən 2 dəqiqə → fərdi istiqamətlər",
        inline=True
    )
    embed.add_field(
        name="🔎 Karyeraları Araşdır",
        value="Altı sahəyə bax və mümkün istiqamətləri müqayisə et",
        inline=True
    )
    embed.add_field(
        name="📊 Tövsiyə Al",
        value="Özünü təsvir et → AI üç istiqamət təklif etsin",
        inline=True
    )
    embed.set_footer(text="CareerCompass v1.1 🧭 • Gemini 2.5 Flash ilə işləyir")
    return embed
