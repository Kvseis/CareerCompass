import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

BOT_PREFIX = "!"
BOT_NAME = "CareerCompass"
BOT_VERSION = "1.0.0"

# Colors for embeds
COLOR_PRIMARY = 0x6C63FF    # Purple
COLOR_SUCCESS = 0x2ECC71    # Green
COLOR_WARNING = 0xF39C12    # Orange
COLOR_INFO    = 0x3498DB    # Blue
COLOR_ERROR   = 0xE74C3C    # Red

# Test flow settings
MAX_CAREERS_IN_RESULT = 3
TEST_QUESTIONS_COUNT = 5
