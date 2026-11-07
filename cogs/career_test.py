import discord
from discord.ext import commands
from discord import app_commands
from views.test_views import QuestionSelectView, QuestionButtonView, build_question_embed, QUESTIONS
from database import upsert_user


class CareerTest(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="test", description="Karyera testinə başla 🎯")
    async def test(self, interaction: discord.Interaction):
        upsert_user(str(interaction.user.id), interaction.user.display_name)
        embed = build_question_embed(0, interaction.user.display_name)
        q = QUESTIONS[0]
        if q["type"] == "select":
            view = QuestionSelectView(0, {})
        else:
            view = QuestionButtonView(0, {})
        await interaction.response.send_message(embed=embed, view=view)


async def setup(bot: commands.Bot):
    await bot.add_cog(CareerTest(bot))
