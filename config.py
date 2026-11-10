import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

BOT_PREFIX = "!"
BOT_NAME = "CareerCompass"
BOT_VERSION = "1.1.0"

# Colors for embeds
COLOR_PRIMARY = 0x22C55E    # CareerCompass green
COLOR_SUCCESS = 0x10B981    # Emerald
COLOR_WARNING = 0xF59E0B    # Amber
COLOR_INFO    = 0x38BDF8    # Sky blue
COLOR_ERROR   = 0xEF4444    # Red

# Test flow settings
MAX_CAREERS_IN_RESULT = 3
TEST_QUESTIONS_COUNT = 5

