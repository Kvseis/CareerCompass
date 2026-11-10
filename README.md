<div align="center">

<img src="./assets/careercompass-banner.jpg" width="100%" alt="CareerCompass — AI Career Guidance" />

# CareerCompass

### An AI-powered Discord bot for structured career exploration

[![Tests](https://github.com/Kvseis/CareerCompass/actions/workflows/tests.yml/badge.svg)](https://github.com/Kvseis/CareerCompass/actions/workflows/tests.yml)
[![Python](https://img.shields.io/badge/Python-3.11%2B-07111F?style=flat-square&logo=python&logoColor=38BDF8)](https://www.python.org/)
[![discord.py](https://img.shields.io/badge/discord.py-2.x-07111F?style=flat-square&logo=discord&logoColor=22C55E)](https://discordpy.readthedocs.io/)
[![Gemini](https://img.shields.io/badge/Gemini-AI-07111F?style=flat-square&logo=googlegemini&logoColor=38BDF8)](https://ai.google.dev/)
[![SQLite](https://img.shields.io/badge/SQLite-Local_Data-07111F?style=flat-square&logo=sqlite&logoColor=22C55E)](https://www.sqlite.org/)

</div>

CareerCompass helps Azerbaijani students and career changers move from vague
interests to concrete directions. It combines a short interactive assessment,
a curated offline career catalog, and Gemini-powered explanations inside
Discord. The product experience is Azerbaijani-first, while the repository
documentation is written in English for international reviewers and
contributors.

The project is designed as an exploration aid—not a psychological assessment
and not a replacement for a qualified career counselor.

## Why this project exists

Career information is often scattered, generic, or difficult to turn into a
first step. CareerCompass creates a guided flow:

1. understand a user's interests and priorities;
2. suggest a small number of relevant directions;
3. explain the skills and learning path for each direction;
4. encourage further research and real-world experimentation.

## Features

- Five-question interactive career assessment
- Azerbaijani-first Discord interface, catalog, and AI responses
- Career exploration across six sectors
- Free-text AI recommendations and career Q&A
- Detailed career overviews and learning roadmaps
- Saved favorites and assessment history
- SQLite persistence
- Credential-free deterministic fallback when Gemini is unavailable
- Automated tests on Python 3.11 and 3.12

## Demo

Run the offline demo without Discord credentials or an AI key:

```bash
python scripts/demo.py
```

Example:

```text
CareerCompass - yerli demo
===============================
Nümunə profil:
  Maraqlar: texnologiya
  İş tərzi: komanda
  Prioritet: inkişaf
  Bacarıqlar: analitik düşüncə
  Təcrübə: başlanğıc

Tövsiyə olunan istiqamətlər:

1. Data Analitiki
   Məlumatları təhlil edir və qərarvermə üçün aydın nəticələr hazırlayır...
   İlk addım: Python və Pandas əsaslarını öyrən (2 ay)
```

See the complete [demo guide](./docs/DEMO.md).

## Architecture

```mermaid
flowchart LR
    U[Discord user] --> C[Cogs and commands]
    C --> V[Interactive views]
    C --> G[Gemini service]
    C --> S[Local catalog service]
    C --> DB[(SQLite)]
    S --> J[(Azerbaijani career catalog)]
    G -. fallback .-> S
```

The Discord presentation layer is separated from the local recommendation
service, data catalog, AI client, and persistence layer. This keeps the core
logic testable without external credentials.

Read the full [architecture document](./docs/ARCHITECTURE.md).

## Commands

| Command | Purpose |
| --- | --- |
| `/start` | Open the main menu |
| `/test` | Complete the five-question assessment |
| `/explore [sector]` | Browse careers by sector |
| `/recommend [description]` | Receive suggestions from a free-text profile |
| `/chat [message]` | Ask a short career-related question |
| `/favorites` | View saved careers |
| `/about` | Display project information |

## Quick start

### 1. Clone and create an environment

```bash
git clone https://github.com/Kvseis/CareerCompass.git
cd CareerCompass
python -m venv .venv
```

Activate the environment:

```bash
# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure credentials

Copy `.env.example` to `.env` and provide:

```dotenv
DISCORD_TOKEN=your_discord_bot_token
GEMINI_API_KEY=your_gemini_api_key
```

Create the Discord application in the Discord Developer Portal, enable the
required bot intents, and invite it with the `bot` and
`applications.commands` scopes.

### 4. Start the bot

```bash
python bot.py
```

## Testing

```bash
pip install -r requirements-dev.txt
python -m compileall -q .
pytest -q
```

The suite covers catalog integrity, deterministic fallback recommendations,
SQLite persistence, favorites, assessment history, and Discord embed builders.

## Project structure

```text
CareerCompass/
├── .github/workflows/     # CI test workflow
├── assets/                # Repository visuals
├── cogs/                  # Discord slash commands and events
├── docs/                  # Architecture and demo documentation
├── scripts/               # Credential-free local demo
├── services/              # Reusable catalog logic
├── tests/                 # Automated test suite
├── views/                 # Interactive Discord UI
├── bot.py                 # Application entry point
├── career_catalog.json    # Default Azerbaijani career data
├── career_catalog_en.json # Optional English reference dataset
├── database.py            # SQLite persistence
└── gemini_client.py       # Gemini prompts and client
```

## Responsible AI and privacy

- AI output is presented as exploratory guidance, not a guaranteed decision.
- Salary ranges are illustrative and vary significantly by location and experience.
- The application falls back to a transparent local catalog if Gemini fails.
- Discord IDs, display names, answers, results, and favorites are stored in a
  local SQLite database.
- Free-text descriptions and assessment answers may be sent to Gemini.
- Secrets are loaded from environment variables and excluded from version
  control.

## Roadmap

- Add recommendation-quality evaluation fixtures
- Add optional English and Turkish interfaces while keeping Azerbaijani as the default
- Add administrator-configurable privacy and retention controls
- Collect consent-based pilot feedback from students
- Build a lightweight web dashboard

## Contributing

Read [CONTRIBUTING.md](./CONTRIBUTING.md) before opening a pull request.

---

<div align="center">

Built by [Kvseis](https://github.com/Kvseis) as an exploration of responsible
AI, product design, and accessible career guidance.

</div>
