"""CareerCompass Discord bot entry point."""

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
    print(f"  [OK] {bot.user} kimi daxil olundu")
    print(f"  [OK] {len(bot.guilds)} serverdə aktivdir")
    print("=" * 50)

    # Sync slash commands
    try:
        synced = await bot.tree.sync()
        print(f"  [SYNC] {len(synced)} slash komandası sinxronlaşdırıldı")
    except Exception as e:
        print(f"  [ERROR] Komandalar sinxronlaşdırılmadı: {e}")

    # Set activity
    activity = discord.Activity(
        type=discord.ActivityType.watching,
        name="karyera yolları | /start"
    )
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print("  [READY] Bot hazırdır.\n")


@bot.event
async def on_guild_join(guild: discord.Guild):
    print(f"[+] Yeni server: {guild.name} (ID: {guild.id})")
    # Try to send welcome message to first available text channel
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            embed = discord.Embed(
                title="👋 Salam! Mən CareerCompass-am.",
                description=(
                    "Məni serverə əlavə etdiyiniz üçün təşəkkür edirəm! 🎉\n\n"
                    "Azərbaycanlı şagirdlərə və karyerasını dəyişmək istəyənlərə "
                    "AI vasitəsilə uyğun istiqamətləri araşdırmağa kömək edirəm.\n\n"
                    "**Başlamaq üçün:** `/start` komandasından istifadə edin.\n\n"
                    "**Komandalar:**\n"
                    "• `/start` — Əsas menyu\n"
                    "• `/test` — Karyera testi\n"
                    "• `/explore` — Sahələri araşdır\n"
                    "• `/recommend` — AI tövsiyəsi\n"
                    "• `/chat` — AI məsləhətçisinə sual ver\n"
                    "• `/favorites` — Saxlanılmış karyeralar\n"
                    "• `/about` — Bot haqqında"
                ),
                color=0x22C55E
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
                "❌ Xəta baş verdi. Zəhmət olmasa yenidən cəhd edin.",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "❌ Xəta baş verdi. Zəhmət olmasa yenidən cəhd edin.",
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
    """Manually synchronize slash commands (bot owner only)."""
    synced = await bot.tree.sync()
    await ctx.send(f"✅ {len(synced)} komanda sinxronlaşdırıldı.", delete_after=10)


# ──────────────────────────────────────────────
#  MAIN
# ──────────────────────────────────────────────

async def main():
    # Validate config
    if not DISCORD_TOKEN:
        print("[ERROR] DISCORD_TOKEN tapılmadı. .env faylını yoxlayın.")
        sys.exit(1)

    # Initialize database
    init_db()

    # Load cogs
    async with bot:
        for cog in COGS:
            try:
                await bot.load_extension(cog)
                print(f"  [OK] Modul yükləndi: {cog}")
            except Exception as e:
                print(f"  [ERROR] Modul yüklənmədi [{cog}]: {e}")

        print(f"\n[START] {BOT_NAME} başladılır...\n")
        await bot.start(DISCORD_TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
