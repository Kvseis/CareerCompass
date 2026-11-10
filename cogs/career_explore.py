import discord
from discord.ext import commands
from discord import app_commands
from views.explore_views import ExploreView, build_explore_embed, SECTORS, build_sector_embed, SectorView
from database import upsert_user


class CareerExplore(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="explore", description="Karyera sahələrini araşdır 🔎")
    @app_commands.describe(sector="Birbaşa sahə seç (istəyə bağlı)")
    @app_commands.choices(sector=[
        app_commands.Choice(name="💻 Texnologiya", value="tech"),
        app_commands.Choice(name="🎨 Dizayn", value="design"),
        app_commands.Choice(name="🏥 Sağlamlıq", value="health"),
        app_commands.Choice(name="💼 Biznes", value="business"),
        app_commands.Choice(name="📱 Media", value="media"),
        app_commands.Choice(name="🧠 Psixologiya", value="psychology"),
    ])
    async def explore(self, interaction: discord.Interaction, sector: str = None):
        upsert_user(str(interaction.user.id), interaction.user.display_name)

        if sector:
            embed = build_sector_embed(sector)
            view = SectorView(sector)
        else:
            embed = build_explore_embed()
            view = ExploreView()

        await interaction.response.send_message(embed=embed, view=view)


async def setup(bot: commands.Bot):
    await bot.add_cog(CareerExplore(bot))
