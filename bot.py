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
    print(f"  [OK] Signed in as {bot.user}")
    print(f"  [OK] Active in {len(bot.guilds)} server(s)")
    print("=" * 50)

    # Sync slash commands
    try:
        synced = await bot.tree.sync()
        print(f"  [SYNC] Synced {len(synced)} slash command(s)")
    except Exception as e:
        print(f"  [ERROR] Command sync failed: {e}")

    # Set activity
    activity = discord.Activity(
        type=discord.ActivityType.watching,
        name="career paths | /start"
    )
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print("  [READY] Bot is ready.\n")


@bot.event
async def on_guild_join(guild: discord.Guild):
    print(f"[+] Joined server: {guild.name} (ID: {guild.id})")
    # Try to send welcome message to first available text channel
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            embed = discord.Embed(
                title="👋 Hello! I am CareerCompass.",
                description=(
                    "Thanks for adding me to the server! 🎉\n\n"
                    "I help students and career changers explore possible paths with AI.\n\n"
                    "**Get started:** use `/start`.\n\n"
                    "**Commands:**\n"
                    "• `/start` — Main menu\n"
                    "• `/test` — Career assessment\n"
                    "• `/explore` — Explore sectors\n"
                    "• `/recommend` — AI recommendation\n"
                    "• `/chat` — Ask the AI counselor\n"
                    "• `/favorites` — Saved careers\n"
                    "• `/about` — About the bot"
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
                "❌ Something went wrong. Please try again.",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "❌ Something went wrong. Please try again.",
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
    await ctx.send(f"✅ Synchronized {len(synced)} command(s).", delete_after=10)


# ──────────────────────────────────────────────
#  MAIN
# ──────────────────────────────────────────────

async def main():
    # Validate config
    if not DISCORD_TOKEN:
        print("[ERROR] DISCORD_TOKEN is missing. Check your .env file.")
        sys.exit(1)

    # Initialize database
    init_db()

    # Load cogs
    async with bot:
        for cog in COGS:
            try:
                await bot.load_extension(cog)
                print(f"  [OK] Loaded extension: {cog}")
            except Exception as e:
                print(f"  [ERROR] Could not load extension [{cog}]: {e}")

        print(f"\n[START] Starting {BOT_NAME}...\n")
        await bot.start(DISCORD_TOKEN)


if __name__ == "__main__":
    asyncio.run(main())

