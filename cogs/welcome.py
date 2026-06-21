import discord
from discord.ext import commands
from discord import app_commands
from database import upsert_user
from views.main_menu import MainMenuView, build_greeting_embed


class Welcome(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ── Slash command: /start ──────────────────────────────────────────────
    @app_commands.command(name="start", description="CareerCompass botunu başlat 🧭")
    async def start(self, interaction: discord.Interaction):
        upsert_user(str(interaction.user.id), interaction.user.display_name)
        embed = build_greeting_embed(interaction.user.display_name)
        view = MainMenuView()
        await interaction.response.send_message(embed=embed, view=view)

    # ── Slash command: /about ─────────────────────────────────────────────
    @app_commands.command(name="about", description="CareerCompass haqqında məlumat 📖")
    async def about(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🧭 CareerCompass haqqında",
            description=(
                "**CareerCompass** gənclərin və karyerasını dəyişmək istəyənlərin "
                "özlərinə uyğun karyera yollarını tapmasına kömək edən AI Discord botudur.\n\n"
                "🤖 **AI Engine:** Google Gemini 2.0 Flash\n"
                "💾 **Baza:** SQLite\n"
                "🔧 **Framework:** discord.py v2\n"
                "📦 **Versiya:** 1.0.0\n\n"
                "**Əsas xüsusiyyətlər:**\n"
                "• 5 sualdan ibarət interaktiv karyera testi\n"
                "• 6 sahədə 18+ karyera kəşf sistemi\n"
                "• AI ilə fərdi tövsiyə sistemi\n"
                "• Favoritlər siyahısı\n"
                "• Ətraflı karyera məlumatları + yol xəritəsi\n\n"
                "**Komandalar:**\n"
                "`/start` — Ana menyu\n"
                "`/test` — Birbaşa testi başlat\n"
                "`/explore` — Karyera kəşf et\n"
                "`/recommend` — AI tövsiyəsi al\n"
                "`/favorites` — Favoritlərini gör\n"
                "`/about` — Bu mesaj"
            ),
            color=0x6C63FF
        )
        embed.set_footer(text="CareerCompass v1.0 🧭 • Sənin karyera yol xəritən")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    # ── on_member_join event ─────────────────────────────────────────────
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """Yeni üzv qoşulanda DM ilə qarşıla."""
        try:
            upsert_user(str(member.id), member.display_name)
            embed = discord.Embed(
                title=f"👋 Xoş gəldin, {member.display_name}!",
                description=(
                    f"**{member.guild.name}** serverinə xoş gəldin! 🎉\n\n"
                    "Mən **CareerCompass** — karyera yol xəritəsi botunun!\n\n"
                    "Sənə uyğun karyera tapmaq üçün `/start` yaz və işə başlayaq! 🚀"
                ),
                color=0x6C63FF
            )
            await member.send(embed=embed)
        except discord.Forbidden:
            pass  # DM-lər bağlı ola bilər


async def setup(bot: commands.Bot):
    await bot.add_cog(Welcome(bot))
