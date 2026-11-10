# Demo Guide

## Credential-free demo

The local demo exercises the offline recommendation path without Discord or an
AI API key.

```bash
python scripts/demo.py
```

It loads a sample student profile, ranks the Azerbaijani career catalog, and
prints three suggested directions with a practical first step in Azerbaijani.

## Full Discord walkthrough

After completing the setup in the main README:

1. Use `/start` to open the main navigation.
2. Use `/test` to complete the five-question assessment.
3. Review the three AI-generated paths or the local fallback result.
4. Use `/explore` to compare sectors and inspect detailed roadmaps.
5. Save a path and retrieve it with `/favorites`.
6. Use `/recommend` for a free-text recommendation.
7. Use `/chat` for a short career-related question.

## Honest demo status

This repository does not currently provide a permanently hosted public bot.
Reviewers can run the credential-free demo immediately or configure their own
Discord application for the complete interactive experience.

## Language note

The product is Azerbaijani-first because its primary audience is Azerbaijani
students. The README and technical documentation are intentionally English so
international reviewers can assess the project without losing the local focus
of the user experience.
