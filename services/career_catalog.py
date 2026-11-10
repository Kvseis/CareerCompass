"""Read and query the offline career catalog.

The catalog is intentionally independent from Discord and Gemini so it can be
used as a reliable fallback, exercised in tests, and demonstrated without API
credentials.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

CATALOG_PATH = Path(__file__).resolve().parents[1] / "career_catalog.json"


def load_catalog(path: Path = CATALOG_PATH) -> dict[str, list[dict]]:
    """Load and validate the top-level shape of the career catalog."""
    with path.open(encoding="utf-8") as catalog_file:
        catalog = json.load(catalog_file)

    if not isinstance(catalog, dict) or not catalog:
        raise ValueError("Career catalog must contain at least one sector.")

    for sector, careers in catalog.items():
        if not isinstance(sector, str) or not isinstance(careers, list):
            raise ValueError("Each catalog sector must map to a list of careers.")

    return catalog


CAREER_DATA = load_catalog()


def iter_careers(catalog: dict[str, list[dict]] = CAREER_DATA) -> Iterable[dict]:
    """Yield every career in sector order."""
    for careers in catalog.values():
        yield from careers


def recommend_from_answers(
    answers: dict[str, str],
    limit: int = 3,
    catalog: dict[str, list[dict]] = CAREER_DATA,
) -> list[dict]:
    """Return deterministic catalog suggestions for assessment answers.

    This lightweight scorer is a transparent fallback, not a psychological
    assessment. It prioritizes the selected sector and then matches answer
    values against each career's personality tags.
    """
    if limit < 1:
        return []

    selected_sector = answers.get("interests", "")
    if selected_sector in catalog:
        candidates = list(catalog[selected_sector])
    else:
        candidates = list(iter_careers(catalog))

    answer_traits = {str(value).lower() for value in answers.values() if value}

    def score(career: dict) -> int:
        traits = {str(value).lower() for value in career.get("personality_match", [])}
        trait_score = len(answer_traits & traits) * 3
        beginner_bonus = int(
            answers.get("experience") == "beginner"
            and career.get("difficulty") in {"easy-medium", "medium"}
        )
        return trait_score + beginner_bonus

    ranked = sorted(
        enumerate(candidates),
        key=lambda item: (-score(item[1]), item[0]),
    )
    return [career for _, career in ranked[:limit]]

