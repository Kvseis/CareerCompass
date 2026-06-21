import discord
from config import COLOR_SUCCESS, COLOR_PRIMARY


def build_result_embed(recommendations_text: str, username: str) -> discord.Embed:
    embed = discord.Embed(
        title=f"🎯 {username} üçün Karyera Tövsiyələri",
        description=recommendations_text[:4096],
        color=COLOR_SUCCESS
    )
    embed.set_footer(
        text="CareerCompass 🧭 • Gemini AI tərəfindən hazırlanmışdır • Yenidən test üçün /test"
    )
    return embed


class ResultView(discord.ui.View):
    def __init__(self, answers: dict = None):
        super().__init__(timeout=600)
        self.answers = answers or {}

    @discord.ui.button(label="🔄 Yenidən Test Et", style=discord.ButtonStyle.primary, row=0)
    async def retest_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        from views.test_views import QuestionSelectView, QuestionButtonView, build_question_embed, QUESTIONS
        embed = build_question_embed(0, interaction.user.display_name)
        q = QUESTIONS[0]
        if q["type"] == "select":
            view = QuestionSelectView(0, {})
        else:
            view = QuestionButtonView(0, {})
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="🔎 Karyera Kəşf Et", style=discord.ButtonStyle.secondary, row=0)
    async def explore_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        from views.explore_views import ExploreView, build_explore_embed
        embed = build_explore_embed()
        view = ExploreView()
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="🏠 Ana Menyu", style=discord.ButtonStyle.secondary, row=0)
    async def menu_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        from views.main_menu import MainMenuView, build_greeting_embed
        embed = build_greeting_embed(interaction.user.display_name)
        view = MainMenuView()
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="📋 Keçmiş Nəticələr", style=discord.ButtonStyle.success, row=1)
    async def history_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        from database import get_all_test_results
        results = get_all_test_results(str(interaction.user.id))
        if not results:
            await interaction.response.send_message(
                "📭 Hələ heç bir test nəticən yoxdur.", ephemeral=True
            )
            return

        embed = discord.Embed(
            title="📋 Test Tarixçən",
            description=f"Cəmi **{len(results)}** test etmisən.",
            color=COLOR_PRIMARY
        )
        for i, r in enumerate(results[:5], 1):
            embed.add_field(
                name=f"Test #{i} — {r['created_at'][:10]}",
                value=f"Maraqlar: `{r['answers'].get('interests', '?')}` | "
                      f"Prioritet: `{r['answers'].get('priority', '?')}`",
                inline=False
            )
        await interaction.response.send_message(embed=embed, ephemeral=True)
