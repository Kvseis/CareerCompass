from views.explore_views import build_career_embed, build_explore_embed, build_sector_embed
from views.main_menu import build_greeting_embed
from views.result_views import build_result_embed
from views.test_views import QUESTIONS, build_question_embed


def test_assessment_contains_five_complete_questions():
    assert len(QUESTIONS) == 5
    assert all(question["id"] for question in QUESTIONS)
    assert all(question["options"] for question in QUESTIONS)


def test_question_embed_is_in_english():
    embed = build_question_embed(0, "Alex")
    assert "Career Assessment" in embed.title
    assert "Question 1/5" in embed.description
    assert "Alex" in embed.footer.text


def test_main_and_explorer_embeds_render():
    greeting = build_greeting_embed("Alex")
    explorer = build_explore_embed()
    sector = build_sector_embed("tech")

    assert "Alex" in greeting.description
    assert explorer.title == "🔎 Career Explorer"
    assert "Technology & Programming" in sector.title
    assert len(sector.fields) >= 3


def test_career_and_result_embeds_render():
    career = {
        "name": "Software Engineer",
        "emoji": "💻",
        "description": "Builds software.",
        "skills": ["Python", "Testing"],
        "salary_range": "Varies",
        "work_style": "hybrid",
        "demand": "high",
        "roadmap": ["Learn Python", "Build a project"],
        "resources": ["CS50"],
    }

    career_embed = build_career_embed(career)
    result_embed = build_result_embed("Try software engineering.", "Alex")

    assert career_embed.title == "💻 Software Engineer"
    assert any(field.name == "🛠️ Core Skills" for field in career_embed.fields)
    assert "Alex" in result_embed.title

