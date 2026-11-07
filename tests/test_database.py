import database


def configure_test_database(tmp_path, monkeypatch):
    db_path = tmp_path / "career_compass_test.db"
    monkeypatch.setattr(database, "DB_PATH", str(db_path))
    database.init_db()
    return db_path


def test_user_is_created_and_updated(tmp_path, monkeypatch):
    configure_test_database(tmp_path, monkeypatch)

    database.upsert_user("42", "First Name")
    database.upsert_user("42", "Updated Name")

    user = database.get_user("42")
    assert user["discord_id"] == "42"
    assert user["username"] == "Updated Name"


def test_assessment_results_round_trip(tmp_path, monkeypatch):
    configure_test_database(tmp_path, monkeypatch)
    database.upsert_user("42", "Student")

    answers = {"interests": "tech", "skills": "analytical"}
    recommendations = ["Backend Developer", "Data Scientist"]
    database.save_test_result("42", answers, recommendations)

    latest = database.get_latest_test_result("42")
    assert latest["answers"] == answers
    assert latest["recommendations"] == recommendations
    assert len(database.get_all_test_results("42")) == 1


def test_favorites_are_unique_and_removable(tmp_path, monkeypatch):
    configure_test_database(tmp_path, monkeypatch)
    database.upsert_user("42", "Student")
    career = {
        "id": "backend_dev",
        "name": "Backend Developer",
        "description": "Builds APIs.",
    }

    assert database.add_favorite("42", career["id"], career["name"], career)
    assert not database.add_favorite("42", career["id"], career["name"], career)
    assert database.is_favorite("42", career["id"])
    assert database.get_favorites("42")[0]["career_data"] == career
    assert database.remove_favorite("42", career["id"])
    assert not database.is_favorite("42", career["id"])


def test_explore_history_is_recorded(tmp_path, monkeypatch):
    configure_test_database(tmp_path, monkeypatch)
    database.log_explore("42", "tech")

    conn = database.get_connection()
    row = conn.execute(
        "SELECT discord_id, sector FROM explore_history"
    ).fetchone()
    conn.close()

    assert dict(row) == {"discord_id": "42", "sector": "tech"}

