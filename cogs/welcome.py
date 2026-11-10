import discord
from discord.ext import commands
from discord import app_commands
from database import upsert_user
from views.main_menu import MainMenuView, build_greeting_embed


class Welcome(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ── Slash command: /start ──────────────────────────────────────────────
    @app_commands.command(name="start", description="CareerCompass-ı aç 🧭")
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
                "**CareerCompass** azərbaycanlı şagirdlərə və karyerasını dəyişmək "
                "istəyənlərə maraqlarına uyğun istiqamətləri araşdırmağa kömək edən "
                "AI əsaslı Discord botudur.\n\n"
                "🤖 **AI mühərriki:** Google Gemini 2.5 Flash\n"
                "💾 **Məlumat bazası:** SQLite\n"
                "🔧 **Framework:** discord.py v2\n"
                "📦 **Versiya:** 1.1.0\n\n"
                "**Əsas funksiyalar:**\n"
                "• Beş suallıq interaktiv karyera testi\n"
                "• Altı sahə üzrə karyera araşdırması\n"
                "• Fərdiləşdirilmiş AI tövsiyələri\n"
                "• Seçilmiş karyeraların saxlanılması\n"
                "• Ətraflı məlumat və inkişaf yol xəritələri\n\n"
                "**Komandalar:**\n"
                "`/start` — Əsas menyunu aç\n"
                "`/test` — Testə başla\n"
                "`/explore` — Karyeraları araşdır\n"
                "`/recommend` — AI tövsiyəsi al\n"
                "`/favorites` — Saxlanılmış karyeraları göstər\n"
                "`/about` — Bu məlumatı göstər"
            ),
            color=0x22C55E
        )
        embed.set_footer(text="CareerCompass v1.1 🧭 • Növbəti addımını müəyyən et")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    # ── on_member_join event ─────────────────────────────────────────────
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """Welcome a new server member with a direct message."""
        try:
            upsert_user(str(member.id), member.display_name)
            embed = discord.Embed(
                title=f"👋 Xoş gəldin, {member.display_name}!",
                description=(
                    f"**{member.guild.name}** serverinə xoş gəldin! 🎉\n\n"
                    "Mən **CareerCompass**, sənin AI karyera araşdırma köməkçinəm.\n\n"
                    "`/start` yaz və sənə uyğun istiqamətləri birlikdə araşdıraq. 🚀"
                ),
                color=0x22C55E
            )
            await member.send(embed=embed)
        except discord.Forbidden:
            pass  # İstifadəçi şəxsi mesajları bağlamış ola bilər.


async def setup(bot: commands.Bot):
    await bot.add_cog(Welcome(bot))
