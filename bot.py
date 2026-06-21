"""
CareerCompass -- Karyera Meslehetcisi Discord Botu
Gemini 2.0 Flash AI ile isleyir
"""

import discord
from discord.ext import commands
import asyncio
import sys
import os

# Fix Windows console encoding
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from config import DISCORD_TOKEN, BOT_PREFIX, BOT_NAME, BOT_VERSION
from database import init_db

# ──────────────────────────────────────────────
#  INTENTS & BOT SETUP
# ──────────────────────────────────────────────

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix=BOT_PREFIX,
    intents=intents,
    help_command=None,
)

COGS = [
    "cogs.welcome",
    "cogs.career_test",
    "cogs.career_explore",
    "cogs.recommendations",
]

# ──────────────────────────────────────────────
#  BOT EVENTS
# ──────────────────────────────────────────────

@bot.event
async def on_ready():
    print("=" * 50)
    print(f"  [OK] {BOT_NAME} v{BOT_VERSION}")
    print(f"  [OK] {bot.user} olaraq giris edildi")
    print(f"  [OK] {len(bot.guilds)} server(ler)de aktiv")
    print("=" * 50)

    # Sync slash commands
    try:
        synced = await bot.tree.sync()
        print(f"  [SYNC] {len(synced)} slash komanda sync edildi")
    except Exception as e:
        print(f"  [ERROR] Sync xetasi: {e}")

    # Set activity
    activity = discord.Activity(
        type=discord.ActivityType.watching,
        name="karyera yollari | /start"
    )
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print("  [READY] Bot hazirdir!\n")


@bot.event
async def on_guild_join(guild: discord.Guild):
    print(f"[+] Yeni server: {guild.name} (ID: {guild.id})")
    # Try to send welcome message to first available text channel
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            embed = discord.Embed(
                title="👋 Salam! Mən CareerCompass-ım!",
                description=(
                    "Sizi bu serverə qəbul etdiyim üçün çox məmnunam! 🎉\n\n"
                    "Mən gənclərin karyera yollarını tapmalarına kömək edən AI botuyam.\n\n"
                    "**Başlamaq üçün:** `/start` yazın!\n\n"
                    "**Bütün komandalar:**\n"
                    "• `/start` — Ana menyu\n"
                    "• `/test` — Karyera testi\n"
                    "• `/explore` — Sahə kəşfi\n"
                    "• `/recommend` — AI tövsiyəsi\n"
                    "• `/chat` — AI ilə söhbət\n"
                    "• `/favorites` — Favoritlər\n"
                    "• `/about` — Bot haqqında"
                ),
                color=0x6C63FF
            )
            try:
                await channel.send(embed=embed)
            except Exception:
                pass
            break


@bot.event
async def on_command_error(ctx: commands.Context, error):
    if isinstance(error, commands.CommandNotFound):
        return
    print(f"[ERROR] {error}")


@bot.event
async def on_app_command_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
    print(f"[APP CMD ERROR] {error}")
    try:
        if interaction.response.is_done():
            await interaction.followup.send(
                "❌ Bir xəta baş verdi. Zəhmət olmasa yenidən cəhd edin.",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "❌ Bir xəta baş verdi. Zəhmət olmasa yenidən cəhd edin.",
                ephemeral=True
            )
    except Exception:
        pass


# ──────────────────────────────────────────────
#  PREFIX COMMANDS (fallback)
# ──────────────────────────────────────────────

@bot.command(name="sync", hidden=True)
@commands.is_owner()
async def sync_commands(ctx: commands.Context):
    """Bot sahibi üçün: slash komandaları manual sync et."""
    synced = await bot.tree.sync()
    await ctx.send(f"✅ {len(synced)} komanda sync edildi.", delete_after=10)


# ──────────────────────────────────────────────
#  MAIN
# ──────────────────────────────────────────────

async def main():
    # Validate config
    if not DISCORD_TOKEN:
        print("[ERROR] DISCORD_TOKEN tapilmadi! .env faylini yoxlayin.")
        sys.exit(1)

    # Initialize database
    init_db()

    # Load cogs
    async with bot:
        for cog in COGS:
            try:
                await bot.load_extension(cog)
                print(f"  [OK] Cog yuklendi: {cog}")
            except Exception as e:
                print(f"  [ERROR] Cog xetasi [{cog}]: {e}")

        print(f"\n[START] {BOT_NAME} basladilir...\n")
        await bot.start(DISCORD_TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
