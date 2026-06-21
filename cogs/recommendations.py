import discord
from discord.ext import commands
from discord import app_commands
from database import upsert_user, get_favorites, remove_favorite
from gemini_client import get_ai_recommendation_from_text, chat_with_bot
from config import COLOR_PRIMARY, COLOR_SUCCESS, COLOR_WARNING


class Recommendations(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # Track users waiting to send a text description
        self._waiting_for_text: set = set()

    # ── /recommend ─────────────────────────────────────────────────────────
    @app_commands.command(
        name="recommend",
        description="Özün haqqında yaz, AI sənə karyera tövsiyə etsin 📊"
    )
    @app_commands.describe(description="Özün haqqında bir neçə cümlə yaz (maraqlar, bacarıqlar, hədəflər)")
    async def recommend(self, interaction: discord.Interaction, description: str):
        upsert_user(str(interaction.user.id), interaction.user.display_name)

        loading_embed = discord.Embed(
            title="⏳ AI analiz edir...",
            description=(
                f"🤖 Gemini AI sənin təsvirinə əsasən karyera tövsiyəsi hazırlayır...\n\n"
                f"**Sən yazdın:** *\"{description[:150]}...\"*"
            ),
            color=COLOR_WARNING
        )
        await interaction.response.send_message(embed=loading_embed)

        try:
            result = await get_ai_recommendation_from_text(description)
            embed = discord.Embed(
                title=f"🎯 {interaction.user.display_name} üçün AI Tövsiyələri",
                description=result[:4096],
                color=COLOR_SUCCESS
            )
            embed.set_footer(text="CareerCompass 🧭 • Gemini AI tərəfindən hazırlanmışdır")

            view = PostRecommendView()
            await interaction.edit_original_response(embed=embed, view=view)

        except Exception as e:
            err_embed = discord.Embed(
                title="❌ Xəta",
                description=f"Bir xəta baş verdi: `{str(e)[:200]}`",
                color=0xE74C3C
            )
            await interaction.edit_original_response(embed=err_embed)

    # ── /favorites ──────────────────────────────────────────────────────────
    @app_commands.command(name="favorites", description="Saxladığın karyeraları gör ⭐")
    async def favorites(self, interaction: discord.Interaction):
        upsert_user(str(interaction.user.id), interaction.user.display_name)
        favs = get_favorites(str(interaction.user.id))

        if not favs:
            embed = discord.Embed(
                title="⭐ Favoritlər",
                description=(
                    "Hələ heç bir karyera əlavə etməmisən.\n\n"
                    "Karyeraları kəşf etmək üçün `/explore` yaz və bəyəndiklərini ⭐ et!"
                ),
                color=COLOR_PRIMARY
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        embed = discord.Embed(
            title=f"⭐ Sənin Favoritlərin — {len(favs)} karyera",
            color=COLOR_SUCCESS
        )
        for fav in favs:
            cd = fav['career_data']
            embed.add_field(
                name=f"{cd.get('emoji', '📌')} {fav['career_name']}",
                value=(
                    f"💰 {cd.get('salary_range', 'N/A')}\n"
                    f"📈 {cd.get('demand', 'N/A')}\n"
                    f"🗓️ Əlavə: {fav['added_at'][:10]}"
                ),
                inline=True
            )
        embed.set_footer(text="CareerCompass 🧭 • /explore ilə daha çox karyera kəşf et")
        view = FavoritesView(favs)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    # ── /chat ────────────────────────────────────────────────────────────────
    @app_commands.command(
        name="chat",
        description="CareerCompass AI ilə söhbət et 💬"
    )
    @app_commands.describe(message="Karyera haqqında sualını yaz")
    async def chat(self, interaction: discord.Interaction, message: str):
        upsert_user(str(interaction.user.id), interaction.user.display_name)

        loading_embed = discord.Embed(
            title="💬 Cavab hazırlanır...",
            description=f"🤖 AI sualını analiz edir...\n\n**Sual:** *\"{message[:100]}\"*",
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
            embed.set_footer(text="CareerCompass 🧭 • /chat ilə daha çox sual ver")
            await interaction.edit_original_response(embed=embed)
        except Exception as e:
            await interaction.edit_original_response(
                embed=discord.Embed(title="❌ Xəta", description=str(e)[:200], color=0xE74C3C)
            )

    # ── on_message — AI tövsiyə üçün mətn gözləmə ───────────────────────────
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Handle free-text AI recommendation when user is prompted."""
        if message.author.bot:
            return
        if str(message.author.id) not in self._waiting_for_text:
            return

        self._waiting_for_text.discard(str(message.author.id))
        loading = await message.channel.send("⏳ AI analiz edir...")

        try:
            result = await get_ai_recommendation_from_text(message.content)
            embed = discord.Embed(
                title=f"🎯 {message.author.display_name} üçün AI Tövsiyələri",
                description=result[:4096],
                color=COLOR_SUCCESS
            )
            embed.set_footer(text="CareerCompass 🧭 • Gemini AI tərəfindən hazırlanmışdır")
            await loading.delete()
            await message.channel.send(embed=embed, view=PostRecommendView())
        except Exception as e:
            await loading.edit(content=f"❌ Xəta: {str(e)[:200]}")


# ──────────────────────────────────────────────
#  POST-RECOMMEND VIEW
# ──────────────────────────────────────────────

class PostRecommendView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)

    @discord.ui.button(label="🔎 Karyeraları Kəşf Et", style=discord.ButtonStyle.primary)
    async def explore_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        from views.explore_views import ExploreView, build_explore_embed
        embed = build_explore_embed()
        view = ExploreView()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @discord.ui.button(label="🎯 Testi Et", style=discord.ButtonStyle.secondary)
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

    @discord.ui.button(label="🔎 Daha Çox Kəşf Et", style=discord.ButtonStyle.primary)
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
                description="Favoritlərdən çıxar"
            )
            for fav in favs[:25]
        ]
        super().__init__(
            placeholder="Silmək istədiyini seç...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        career_id = self.values[0]
        removed = remove_favorite(str(interaction.user.id), career_id)
        if removed:
            await interaction.response.send_message(
                f"🗑️ Karyera favoritlərdən silindi.", ephemeral=True
            )
        else:
            await interaction.response.send_message("ℹ️ Karyera tapılmadı.", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Recommendations(bot))
