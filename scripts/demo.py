"""Credential-free CareerCompass demo.

Run from the repository root:

    python scripts/demo.py
"""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from services.career_catalog import recommend_from_answers


SAMPLE_ANSWERS = {
    "interests": "tech",
    "work_style": "team",
    "priority": "growth",
    "skills": "analytical",
    "experience": "beginner",
}


def main() -> None:
    suggestions = recommend_from_answers(SAMPLE_ANSWERS)

    print("CareerCompass - local demo")
    print("=" * 31)
    print("Sample profile:")
    for key, value in SAMPLE_ANSWERS.items():
        print(f"  {key.replace('_', ' ').title()}: {value}")

    print("\nSuggested directions:")
    for index, career in enumerate(suggestions, start=1):
        print(f"\n{index}. {career['name']}")
        print(f"   {career['description']}")
        print(f"   First step: {career['roadmap'][0]}")

    print(
        "\nNote: this deterministic demo is a starting point, not a "
        "professional career assessment."
    )


if __name__ == "__main__":
    main()

