from services.career_catalog import CAREER_DATA, iter_careers, recommend_from_answers


REQUIRED_FIELDS = {
    "id",
    "name",
    "emoji",
    "description",
    "skills",
    "roadmap",
    "resources",
    "salary_range",
    "work_style",
    "personality_match",
    "difficulty",
    "demand",
}


def test_catalog_has_expected_sectors_and_unique_ids():
    assert set(CAREER_DATA) == {
        "tech",
        "design",
        "health",
        "business",
        "media",
        "psychology",
    }

    careers = list(iter_careers())
    career_ids = [career["id"] for career in careers]
    assert len(careers) >= 18
    assert len(career_ids) == len(set(career_ids))


def test_every_career_has_complete_display_data():
    for career in iter_careers():
        assert REQUIRED_FIELDS <= set(career)
        assert career["name"].strip()
        assert career["description"].strip()
        assert career["skills"]
        assert career["roadmap"]
        assert career["resources"]


def test_local_recommendation_is_deterministic_and_sector_scoped():
    answers = {
        "interests": "tech",
        "skills": "analytical",
        "experience": "beginner",
    }

    first = recommend_from_answers(answers)
    second = recommend_from_answers(answers)

    assert first == second
    assert len(first) == 3
    assert all(career in CAREER_DATA["tech"] for career in first)


def test_local_recommendation_can_search_all_sectors():
    results = recommend_from_answers({"interests": "unknown"}, limit=4)
    assert len(results) == 4


def test_invalid_limit_returns_no_recommendations():
    assert recommend_from_answers({}, limit=0) == []

