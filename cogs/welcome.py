import discord
from discord.ext import commands
from discord import app_commands
from database import upsert_user
from views.main_menu import MainMenuView, build_greeting_embed


class Welcome(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ── Slash command: /start ──────────────────────────────────────────────
    @app_commands.command(name="start", description="Open CareerCompass 🧭")
    async def start(self, interaction: discord.Interaction):
        upsert_user(str(interaction.user.id), interaction.user.display_name)
        embed = build_greeting_embed(interaction.user.display_name)
        view = MainMenuView()
        await interaction.response.send_message(embed=embed, view=view)

    # ── Slash command: /about ─────────────────────────────────────────────
    @app_commands.command(name="about", description="Learn about CareerCompass 📖")
    async def about(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🧭 About CareerCompass",
            description=(
                "**CareerCompass** is an AI-powered Discord bot that helps students "
                "and career changers explore paths that fit their interests and goals.\n\n"
                "🤖 **AI engine:** Google Gemini 2.5 Flash\n"
                "💾 **Database:** SQLite\n"
                "🔧 **Framework:** discord.py v2\n"
                "📦 **Version:** 1.1.0\n\n"
                "**Core features:**\n"
                "• Five-question interactive career assessment\n"
                "• Career discovery across six sectors\n"
                "• Personalized AI recommendations\n"
                "• Saved favorites\n"
                "• Detailed career information and roadmaps\n\n"
                "**Commands:**\n"
                "`/start` — Open the main menu\n"
                "`/test` — Start the assessment\n"
                "`/explore` — Explore careers\n"
                "`/recommend` — Get an AI recommendation\n"
                "`/favorites` — View saved careers\n"
                "`/about` — Show this message"
            ),
            color=0x22C55E
        )
        embed.set_footer(text="CareerCompass v1.1 🧭 • Navigate your next step")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    # ── on_member_join event ─────────────────────────────────────────────
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """Welcome a new server member with a direct message."""
        try:
            upsert_user(str(member.id), member.display_name)
            embed = discord.Embed(
                title=f"👋 Welcome, {member.display_name}!",
                description=(
                    f"Welcome to **{member.guild.name}**! 🎉\n\n"
                    "I am **CareerCompass**, your AI career exploration assistant.\n\n"
                    "Use `/start` and let us find a direction that fits you. 🚀"
                ),
                color=0x22C55E
            )
            await member.send(embed=embed)
        except discord.Forbidden:
            pass  # The member may have direct messages disabled.


async def setup(bot: commands.Bot):
    await bot.add_cog(Welcome(bot))

