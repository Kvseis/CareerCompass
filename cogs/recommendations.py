import discord
from discord.ext import commands
from discord import app_commands
from database import upsert_user, get_favorites, remove_favorite
from gemini_client import get_ai_recommendation_from_text, chat_with_bot
from config import COLOR_PRIMARY, COLOR_SUCCESS, COLOR_WARNING


class Recommendations(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ── /recommend ─────────────────────────────────────────────────────────
    @app_commands.command(
        name="recommend",
        description="Özünü təsvir et və AI karyera tövsiyələri al 📊"
    )
    @app_commands.describe(description="Maraqlarını, güclü tərəflərini və hədəflərini yaz")
    async def recommend(self, interaction: discord.Interaction, description: str):
        upsert_user(str(interaction.user.id), interaction.user.display_name)

        loading_embed = discord.Embed(
            title="⏳ Məlumatların təhlil olunur...",
            description=(
                "🤖 Gemini təsvirinə əsasən karyera tövsiyələri hazırlayır.\n\n"
                f"**Sən yazdın:** *\"{description[:150]}...\"*"
            ),
            color=COLOR_WARNING
        )
        await interaction.response.send_message(embed=loading_embed)

        try:
            result = await get_ai_recommendation_from_text(description)
            embed = discord.Embed(
                title=f"🎯 {interaction.user.display_name} üçün Karyera Tövsiyələri",
                description=result[:4096],
                color=COLOR_SUCCESS
            )
            embed.set_footer(text="CareerCompass 🧭 • Gemini AI ilə hazırlanıb")

            view = PostRecommendView()
            await interaction.edit_original_response(embed=embed, view=view)

        except Exception as e:
            err_embed = discord.Embed(
                title="❌ Tövsiyə hazırlanmadı",
                description="AI xidməti sorğunu tamamlaya bilmədi. Zəhmət olmasa bir qədər sonra yenidən cəhd et.",
                color=0xE74C3C
            )
            await interaction.edit_original_response(embed=err_embed)

    # ── /favorites ──────────────────────────────────────────────────────────
    @app_commands.command(name="favorites", description="Saxladığın karyeralara bax ⭐")
    async def favorites(self, interaction: discord.Interaction):
        upsert_user(str(interaction.user.id), interaction.user.display_name)
        favs = get_favorites(str(interaction.user.id))

        if not favs:
            embed = discord.Embed(
                title="⭐ Saxlanılmış Karyeralar",
                description=(
                    "Hələ heç bir karyera saxlamamısan.\n\n"
                    "Maraqlı istiqamət tapdıqda `/explore` bölməsində ⭐ seç."
                ),
                color=COLOR_PRIMARY
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        embed = discord.Embed(
            title=f"⭐ Saxladığın Karyeralar — cəmi {len(favs)}",
            color=COLOR_SUCCESS
        )
        for fav in favs:
            cd = fav['career_data']
            embed.add_field(
                name=f"{cd.get('emoji', '📌')} {fav['career_name']}",
                value=(
                    f"💰 {cd.get('salary_range', 'N/A')}\n"
                    f"📈 {cd.get('demand', 'N/A')}\n"
                    f"🗓️ Saxlanılıb: {fav['added_at'][:10]}"
                ),
                inline=True
            )
        embed.set_footer(text="CareerCompass 🧭 • Yeni istiqamətlər üçün /explore istifadə et")
        view = FavoritesView(favs)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    # ── /chat ────────────────────────────────────────────────────────────────
    @app_commands.command(
        name="chat",
        description="CareerCompass AI məsləhətçisinə sual ver 💬"
    )
    @app_commands.describe(message="Karyera ilə bağlı sualını yaz")
    async def chat(self, interaction: discord.Interaction, message: str):
        upsert_user(str(interaction.user.id), interaction.user.display_name)

        loading_embed = discord.Embed(
            title="💬 Cavab hazırlanır...",
            description=f"🤖 AI sualını təhlil edir.\n\n**Sual:** *\"{message[:100]}\"*",
            color=COLOR_WARNING
        )
        await interaction.response.send_message(embed=loading_embed)

        try:
            response = await chat_with_bot(message)
            embed = discord.Embed(
                title="🤖 CareerCompass AI Cavabı",
                description=response[:4096],
                color=COLOR_PRIMARY
            )
            embed.add_field(name="❓ Sualın", value=f"*{message[:200]}*", inline=False)
            embed.set_footer(text="CareerCompass 🧭 • Yeni sual üçün /chat istifadə et")
            await interaction.edit_original_response(embed=embed)
        except Exception as e:
            await interaction.edit_original_response(
                embed=discord.Embed(
                    title="❌ Cavab hazırlanmadı",
                    description="AI xidməti sorğunu tamamlaya bilmədi. Zəhmət olmasa bir qədər sonra yenidən cəhd et.",
                    color=0xE74C3C,
                )
            )


# ──────────────────────────────────────────────
#  POST-RECOMMEND VIEW
# ──────────────────────────────────────────────

class PostRecommendView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)

    @discord.ui.button(label="🔎 Karyeraları Araşdır", style=discord.ButtonStyle.primary)
    async def explore_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        from views.explore_views import ExploreView, build_explore_embed
        embed = build_explore_embed()
        view = ExploreView()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @discord.ui.button(label="🎯 Testi Tamamla", style=discord.ButtonStyle.secondary)
    async def test_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        from views.test_views import QuestionSelectView, build_question_embed, QUESTIONS
        embed = build_question_embed(0, interaction.user.display_name)
        view = QuestionSelectView(0, {})
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


# ──────────────────────────────────────────────
#  FAVORITES MANAGEMENT VIEW
# ──────────────────────────────────────────────

class FavoritesView(discord.ui.View):
    def __init__(self, favs: list):
        super().__init__(timeout=300)
        if favs:
            self.add_item(RemoveFavoriteSelect(favs))

    @discord.ui.button(label="🔎 Daha Çox Araşdır", style=discord.ButtonStyle.primary)
    async def explore_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        from views.explore_views import ExploreView, build_explore_embed
        embed = build_explore_embed()
        view = ExploreView()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


class RemoveFavoriteSelect(discord.ui.Select):
    def __init__(self, favs: list):
        options = [
            discord.SelectOption(
                label=f"❌ {fav['career_name']}",
                value=fav['career_id'],
                description="Saxlanılmışlardan sil"
            )
            for fav in favs[:25]
        ]
        super().__init__(
            placeholder="Silmək istədiyin karyeranı seç...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        career_id = self.values[0]
        removed = remove_favorite(str(interaction.user.id), career_id)
        if removed:
            await interaction.response.send_message(
                "🗑️ Karyera saxlanılmış siyahıdan silindi.", ephemeral=True
            )
        else:
            await interaction.response.send_message("ℹ️ Karyera tapılmadı.", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Recommendations(bot))
