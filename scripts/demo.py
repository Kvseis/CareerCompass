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

ANSWER_LABELS = {
    "interests": "Maraqlar",
    "work_style": "İş tərzi",
    "priority": "Prioritet",
    "skills": "Bacarıqlar",
    "experience": "Təcrübə",
}


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    suggestions = recommend_from_answers(SAMPLE_ANSWERS)

    print("CareerCompass - yerli demo")
    print("=" * 31)
    print("Nümunə profil:")
    for key, value in SAMPLE_ANSWERS.items():
        print(f"  {ANSWER_LABELS[key]}: {value}")

    print("\nTövsiyə olunan istiqamətlər:")
    for index, career in enumerate(suggestions, start=1):
        print(f"\n{index}. {career['name']}")
        print(f"   {career['description']}")
        print(f"   İlk addım: {career['roadmap'][0]}")

    print(
        "\nQeyd: bu deterministik demo başlanğıc nöqtəsidir, peşəkar "
        "karyera qiymətləndirməsi deyil."
    )


if __name__ == "__main__":
    main()
