import discord
from config import COLOR_INFO, COLOR_PRIMARY
from services.career_catalog import CAREER_DATA

SECTORS = {
    "tech":       ("💻", "Technology & Programming"),
    "design":     ("🎨", "Design & Creativity"),
    "health":     ("🏥", "Health & Medicine"),
    "business":   ("💼", "Business & Marketing"),
    "media":      ("📱", "Media & Communication"),
    "psychology": ("🧠", "Psychology & Coaching"),
}


def build_explore_embed() -> discord.Embed:
    embed = discord.Embed(
        title="🔎 Career Explorer",
        description=(
            "Which field would you like to explore?\n"
            "Choose a sector from the menu below:\n\n"
            + "\n".join(
                f"{emoji} **{name}**"
                for emoji, name in SECTORS.values()
            )
        ),
        color=COLOR_INFO
    )
    embed.set_footer(text="CareerCompass 🧭 • Explore before you decide")
    return embed


def build_sector_embed(sector: str) -> discord.Embed:
    emoji, name = SECTORS[sector]
    careers = CAREER_DATA.get(sector, [])

    embed = discord.Embed(
        title=f"{emoji} {name} — Careers",
        description=f"The catalog currently includes **{len(careers)}** paths in this sector. Select one for details:",
        color=COLOR_PRIMARY
    )
    for c in careers:
        embed.add_field(
            name=f"{c['emoji']} {c['name']}",
            value=(
                f"📌 {c['description'][:80]}...\n"
                f"💰 {c['salary_range']}\n"
                f"📈 Demand: `{c['demand']}`"
            ),
            inline=False
        )
    embed.set_footer(text=f"CareerCompass 🧭 • {name}")
    return embed


def build_career_embed(career: dict) -> discord.Embed:
    embed = discord.Embed(
        title=f"{career['emoji']} {career['name']}",
        description=career['description'],
        color=COLOR_PRIMARY
    )
    embed.add_field(
        name="🛠️ Core Skills",
        value=", ".join(career['skills']),
        inline=False
    )
    embed.add_field(
        name="💰 Salary Range",
        value=career['salary_range'],
        inline=True
    )
    embed.add_field(
        name="🏠 Work Style",
        value=career['work_style'],
        inline=True
    )
    embed.add_field(
        name="📈 Market Demand",
        value=career['demand'],
        inline=True
    )
    embed.add_field(
        name="🚀 Starting Roadmap",
        value="\n".join(f"• {step}" for step in career['roadmap'][:3]),
        inline=False
    )
    embed.add_field(
        name="📚 Resources",
        value=", ".join(career.get('resources', [])[:4]),
        inline=False
    )
    embed.set_footer(text="CareerCompass 🧭 • Use the controls below to go deeper")
    return embed


# ──────────────────────────────────────────────
#  VIEWS
# ──────────────────────────────────────────────

class ExploreView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)
        self.add_item(SectorSelect())
        self.add_item(BackToMenuButton())


class SectorSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label=name,
                value=key,
                emoji=emoji
            )
            for key, (emoji, name) in SECTORS.items()
        ]
        super().__init__(
            placeholder="Choose a sector...",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="explore_sector_select"
        )

    async def callback(self, interaction: discord.Interaction):
        sector = self.values[0]
        from database import upsert_user, log_explore
        upsert_user(str(interaction.user.id), interaction.user.display_name)
        log_explore(str(interaction.user.id), sector)

        embed = build_sector_embed(sector)
        view = SectorView(sector)
        await interaction.response.edit_message(embed=embed, view=view)


class SectorView(discord.ui.View):
    def __init__(self, sector: str):
        super().__init__(timeout=300)
        self.sector = sector
        careers = CAREER_DATA.get(sector, [])
        self.add_item(CareerSelect(careers, sector))
        self.add_item(BackToExploreButton())
        self.add_item(BackToMenuButton())


class CareerSelect(discord.ui.Select):
    def __init__(self, careers: list, sector: str):
        options = [
            discord.SelectOption(
                label=c['name'],
                value=c['id'],
                emoji=c['emoji'],
                description=c['description'][:50]
            )
            for c in careers
        ]
        super().__init__(
            placeholder="Choose a career...",
            min_values=1,
            max_values=1,
            options=options,
            custom_id=f"career_select_{sector}"
        )
        self.careers = careers
        self.sector = sector

    async def callback(self, interaction: discord.Interaction):
        career_id = self.values[0]
        career = next((c for c in self.careers if c['id'] == career_id), None)
        if not career:
            await interaction.response.send_message("Career not found.", ephemeral=True)
            return

        embed = build_career_embed(career)
        view = CareerDetailView(career, self.sector)
        await interaction.response.edit_message(embed=embed, view=view)


class CareerDetailView(discord.ui.View):
    def __init__(self, career: dict, sector: str):
        super().__init__(timeout=300)
        self.career = career
        self.sector = sector
        self.add_item(AIDetailButton(career, sector))
        self.add_item(RoadmapButton(career, sector))
        self.add_item(FavoriteButton(career))
        self.add_item(BackToSectorButton(sector))
        self.add_item(BackToMenuButton())


class AIDetailButton(discord.ui.Button):
    def __init__(self, career: dict, sector: str):
        super().__init__(label="📘 AI Details", style=discord.ButtonStyle.primary, row=0)
        self.career = career
        self.sector = sector

    async def callback(self, interaction: discord.Interaction):
        loading = discord.Embed(
            title="⏳ Preparing details...",
            description="Gemini is preparing a deeper overview of this career.",
            color=0xF39C12
        )
        await interaction.response.edit_message(embed=loading, view=discord.ui.View())
        try:
            from gemini_client import get_career_detail
            text = await get_career_detail(self.career['name'], self.career)
            footer_text = "CareerCompass 🧭 • Generated with AI"
        except Exception as e:
            print(f"[FALLBACK] Detail API error: {e}")
            text = (
                f"🌍 **Career overview:**\n{self.career.get('description', '')}\n\n"
                f"🛠️ **Core skills:**\n" + "\n".join(f"• {s}" for s in self.career.get('skills', [])) + "\n\n"
                f"💰 **Salary range:** {self.career.get('salary_range', '')}\n"
                f"🏠 **Work style:** {self.career.get('work_style', '')}\n"
                f"📈 **Market demand:** {self.career.get('demand', '')}"
            )
            footer_text = "CareerCompass 🧭 • Local career catalog"

        embed = discord.Embed(
            title=f"{self.career['emoji']} {self.career['name']} — Details",
            description=text[:4000],
            color=COLOR_PRIMARY
        )
        embed.set_footer(text=footer_text)
        view = BackOnlyView(self.career, self.sector)
        await interaction.edit_original_response(embed=embed, view=view)

class RoadmapButton(discord.ui.Button):
    def __init__(self, career: dict, sector: str):
        super().__init__(label="🛣️ Roadmap", style=discord.ButtonStyle.secondary, row=0)
        self.career = career
        self.sector = sector

    async def callback(self, interaction: discord.Interaction):
        loading = discord.Embed(
            title="⏳ Preparing a roadmap...",
            description="Gemini is building a practical step-by-step roadmap. 🗺️",
            color=0xF39C12
        )
        await interaction.response.edit_message(embed=loading, view=discord.ui.View())
        try:
            from gemini_client import get_roadmap
            text = await get_roadmap(self.career['name'])
            footer_text = "CareerCompass 🧭 • Generated with AI"
        except Exception as e:
            print(f"[FALLBACK] Roadmap API error: {e}")
            steps = self.career.get('roadmap', [])
            resources = self.career.get('resources', [])
            text = (
                "📍 **Career roadmap:**\n\n" +
                "\n".join(f"{s}" for s in steps) + "\n\n"
                "📚 **Recommended resources:**\n" +
                ", ".join(resources)
            )
            footer_text = "CareerCompass 🧭 • Local career catalog"

        embed = discord.Embed(
            title=f"🛣️ {self.career['name']} — Roadmap",
            description=text[:4000],
            color=0x2ECC71
        )
        embed.set_footer(text=footer_text)
        view = BackOnlyView(self.career, self.sector)
        await interaction.edit_original_response(embed=embed, view=view)


class FavoriteButton(discord.ui.Button):
    def __init__(self, career: dict):
        super().__init__(label="⭐ Save Career", style=discord.ButtonStyle.success, row=1)
        self.career = career

    async def callback(self, interaction: discord.Interaction):
        from database import upsert_user, add_favorite
        upsert_user(str(interaction.user.id), interaction.user.display_name)
        added = add_favorite(
            str(interaction.user.id),
            self.career['id'],
            self.career['name'],
            self.career
        )
        if added:
            await interaction.response.send_message(
                f"⭐ **{self.career['name']}** was added to your saved careers.", ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"ℹ️ **{self.career['name']}** is already in your saved careers.", ephemeral=True
            )


class BackToSectorButton(discord.ui.Button):
    def __init__(self, sector: str):
        super().__init__(label="← Back to Sector", style=discord.ButtonStyle.secondary, row=1)
        self.sector = sector

    async def callback(self, interaction: discord.Interaction):
        embed = build_sector_embed(self.sector)
        view = SectorView(self.sector)
        await interaction.response.edit_message(embed=embed, view=view)


class BackToExploreButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="← Back to Explorer", emoji="🔎", style=discord.ButtonStyle.secondary, row=2)

    async def callback(self, interaction: discord.Interaction):
        embed = build_explore_embed()
        view = ExploreView()
        await interaction.response.edit_message(embed=embed, view=view)


class BackToMenuButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="🏠 Main Menu", style=discord.ButtonStyle.secondary, row=3)

    async def callback(self, interaction: discord.Interaction):
        from views.main_menu import MainMenuView, build_greeting_embed
        embed = build_greeting_embed(interaction.user.display_name)
        view = MainMenuView()
        await interaction.response.edit_message(embed=embed, view=view)


class BackOnlyView(discord.ui.View):
    def __init__(self, career: dict, sector: str):
        super().__init__(timeout=300)
        self.add_item(BackToSectorButton(sector))
        self.add_item(BackToMenuButton())

