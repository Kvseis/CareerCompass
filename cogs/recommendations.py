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
        description="Describe yourself and receive AI career suggestions 📊"
    )
    @app_commands.describe(description="Share your interests, strengths, and goals")
    async def recommend(self, interaction: discord.Interaction, description: str):
        upsert_user(str(interaction.user.id), interaction.user.display_name)

        loading_embed = discord.Embed(
            title="⏳ Analyzing your profile...",
            description=(
                "🤖 Gemini is preparing career suggestions from your description.\n\n"
                f"**You wrote:** *\"{description[:150]}...\"*"
            ),
            color=COLOR_WARNING
        )
        await interaction.response.send_message(embed=loading_embed)

        try:
            result = await get_ai_recommendation_from_text(description)
            embed = discord.Embed(
                title=f"🎯 Career Suggestions for {interaction.user.display_name}",
                description=result[:4096],
                color=COLOR_SUCCESS
            )
            embed.set_footer(text="CareerCompass 🧭 • Generated with Gemini AI")

            view = PostRecommendView()
            await interaction.edit_original_response(embed=embed, view=view)

        except Exception as e:
            err_embed = discord.Embed(
                title="❌ Recommendation unavailable",
                description="The AI service could not complete this request. Please try again shortly.",
                color=0xE74C3C
            )
            await interaction.edit_original_response(embed=err_embed)

    # ── /favorites ──────────────────────────────────────────────────────────
    @app_commands.command(name="favorites", description="View your saved careers ⭐")
    async def favorites(self, interaction: discord.Interaction):
        upsert_user(str(interaction.user.id), interaction.user.display_name)
        favs = get_favorites(str(interaction.user.id))

        if not favs:
            embed = discord.Embed(
                title="⭐ Saved Careers",
                description=(
                    "You have not saved a career yet.\n\n"
                    "Use `/explore` and select ⭐ when you find an interesting path."
                ),
                color=COLOR_PRIMARY
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        embed = discord.Embed(
            title=f"⭐ Your Saved Careers — {len(favs)} total",
            color=COLOR_SUCCESS
        )
        for fav in favs:
            cd = fav['career_data']
            embed.add_field(
                name=f"{cd.get('emoji', '📌')} {fav['career_name']}",
                value=(
                    f"💰 {cd.get('salary_range', 'N/A')}\n"
                    f"📈 {cd.get('demand', 'N/A')}\n"
                    f"🗓️ Saved: {fav['added_at'][:10]}"
                ),
                inline=True
            )
        embed.set_footer(text="CareerCompass 🧭 • Use /explore to discover more paths")
        view = FavoritesView(favs)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    # ── /chat ────────────────────────────────────────────────────────────────
    @app_commands.command(
        name="chat",
        description="Ask the CareerCompass AI counselor a question 💬"
    )
    @app_commands.describe(message="Ask a career-related question")
    async def chat(self, interaction: discord.Interaction, message: str):
        upsert_user(str(interaction.user.id), interaction.user.display_name)

        loading_embed = discord.Embed(
            title="💬 Preparing an answer...",
            description=f"🤖 The AI is reviewing your question.\n\n**Question:** *\"{message[:100]}\"*",
            color=COLOR_WARNING
        )
        await interaction.response.send_message(embed=loading_embed)

        try:
            response = await chat_with_bot(message)
            embed = discord.Embed(
                title="🤖 CareerCompass AI Response",
                description=response[:4096],
                color=COLOR_PRIMARY
            )
            embed.add_field(name="❓ Your question", value=f"*{message[:200]}*", inline=False)
            embed.set_footer(text="CareerCompass 🧭 • Use /chat to ask another question")
            await interaction.edit_original_response(embed=embed)
        except Exception as e:
            await interaction.edit_original_response(
                embed=discord.Embed(
                    title="❌ Response unavailable",
                    description="The AI service could not complete this request. Please try again shortly.",
                    color=0xE74C3C,
                )
            )


# ──────────────────────────────────────────────
#  POST-RECOMMEND VIEW
# ──────────────────────────────────────────────

class PostRecommendView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)

    @discord.ui.button(label="🔎 Explore Careers", style=discord.ButtonStyle.primary)
    async def explore_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        from views.explore_views import ExploreView, build_explore_embed
        embed = build_explore_embed()
        view = ExploreView()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @discord.ui.button(label="🎯 Take the Assessment", style=discord.ButtonStyle.secondary)
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

    @discord.ui.button(label="🔎 Explore More", style=discord.ButtonStyle.primary)
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
                description="Remove from saved careers"
            )
            for fav in favs[:25]
        ]
        super().__init__(
            placeholder="Choose a career to remove...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        career_id = self.values[0]
        removed = remove_favorite(str(interaction.user.id), career_id)
        if removed:
            await interaction.response.send_message(
                "🗑️ Career removed from your saved list.", ephemeral=True
            )
        else:
            await interaction.response.send_message("ℹ️ Career not found.", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Recommendations(bot))

