import discord
from config import COLOR_PRIMARY


class MainMenuView(discord.ui.View):
    """Main navigation with the three primary user journeys."""

    def __init__(self):
        super().__init__(timeout=300)

    @discord.ui.button(
        label="Start Assessment",
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
        label="Explore Careers",
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
        label="Ask for a Recommendation",
        emoji="📊",
        style=discord.ButtonStyle.success,
        custom_id="main_recommend"
    )
    async def recommend_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="📊 AI Recommendation",
            description=(
                "Use the `/recommend` command and describe your interests, strengths, "
                "and goals in a few sentences.\n\n"
                "**Example:** *I enjoy creative work and collaborating with people. "
                "I am curious about technology but I am still learning to code.*\n\n"
                "CareerCompass will turn your description into three practical paths."
            ),
            color=COLOR_PRIMARY
        )
        embed.set_footer(text="CareerCompass AI 🤖 • Powered by Gemini 2.5 Flash")
        view = WaitingForTextView()
        await interaction.response.edit_message(embed=embed, view=view)


class WaitingForTextView(discord.ui.View):
    """Return navigation for the recommendation instructions."""
    def __init__(self):
        super().__init__(timeout=300)

    @discord.ui.button(label="← Back", emoji="↩️", style=discord.ButtonStyle.secondary)
    async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        from cogs.welcome import build_greeting_embed
        embed = build_greeting_embed(interaction.user.display_name)
        view = MainMenuView()
        await interaction.response.edit_message(embed=embed, view=view)


def build_greeting_embed(username: str) -> discord.Embed:
    embed = discord.Embed(
        title="👋 Hello! I am CareerCompass.",
        description=(
            f"**Welcome, {username}!** 🎉\n\n"
            "I am an AI assistant that helps you explore **career paths that fit your "
            "interests and goals**.\n\n"
            "Take a short assessment, browse sectors, or describe yourself for a "
            "personalized recommendation.\n\n"
            "⬇️ **Choose where to begin:**"
        ),
        color=COLOR_PRIMARY
    )
    embed.add_field(
        name="🎯 Start Assessment",
        value="5 questions, about 2 minutes → personalized directions",
        inline=True
    )
    embed.add_field(
        name="🔎 Explore Careers",
        value="Browse six sectors and compare possible paths",
        inline=True
    )
    embed.add_field(
        name="📊 Get a Recommendation",
        value="Describe yourself → AI suggests three paths",
        inline=True
    )
    embed.set_footer(text="CareerCompass v1.1 🧭 • Powered by Gemini 2.5 Flash")
    return embed

