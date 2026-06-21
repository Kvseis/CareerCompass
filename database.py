import sqlite3
import json
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "career_compass.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create all tables if they don't exist."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            discord_id  TEXT    UNIQUE NOT NULL,
            username    TEXT    NOT NULL,
            created_at  TEXT    DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS test_results (
            id                  INTEGER PRIMARY KEY AUTOINCREMENT,
            discord_id          TEXT    NOT NULL,
            answers_json        TEXT    NOT NULL,
            recommendations_json TEXT   NOT NULL,
            created_at          TEXT    DEFAULT (datetime('now')),
            FOREIGN KEY (discord_id) REFERENCES users(discord_id)
        );

        CREATE TABLE IF NOT EXISTS favorites (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            discord_id      TEXT    NOT NULL,
            career_id       TEXT    NOT NULL,
            career_name     TEXT    NOT NULL,
            career_data_json TEXT   NOT NULL,
            added_at        TEXT    DEFAULT (datetime('now')),
            UNIQUE(discord_id, career_id),
            FOREIGN KEY (discord_id) REFERENCES users(discord_id)
        );

        CREATE TABLE IF NOT EXISTS explore_history (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            discord_id  TEXT    NOT NULL,
            sector      TEXT    NOT NULL,
            viewed_at   TEXT    DEFAULT (datetime('now'))
        );
    """)

    conn.commit()
    conn.close()
    print("[DB] Database initialized successfully.")


# ──────────────────────────────────────────────
#  USER helpers
# ──────────────────────────────────────────────

def upsert_user(discord_id: str, username: str):
    conn = get_connection()
    conn.execute(
        "INSERT OR IGNORE INTO users (discord_id, username) VALUES (?, ?)",
        (str(discord_id), username)
    )
    conn.commit()
    conn.close()


def get_user(discord_id: str):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM users WHERE discord_id = ?", (str(discord_id),)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


# ──────────────────────────────────────────────
#  TEST RESULTS helpers
# ──────────────────────────────────────────────

def save_test_result(discord_id: str, answers: dict, recommendations: list):
    conn = get_connection()
    conn.execute(
        "INSERT INTO test_results (discord_id, answers_json, recommendations_json) VALUES (?, ?, ?)",
        (str(discord_id), json.dumps(answers, ensure_ascii=False), json.dumps(recommendations, ensure_ascii=False))
    )
    conn.commit()
    conn.close()


def get_latest_test_result(discord_id: str):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM test_results WHERE discord_id = ? ORDER BY created_at DESC LIMIT 1",
        (str(discord_id),)
    ).fetchone()
    conn.close()
    if row:
        r = dict(row)
        r["answers"] = json.loads(r["answers_json"])
        r["recommendations"] = json.loads(r["recommendations_json"])
        return r
    return None


def get_all_test_results(discord_id: str):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM test_results WHERE discord_id = ? ORDER BY created_at DESC",
        (str(discord_id),)
    ).fetchall()
    conn.close()
    results = []
    for row in rows:
        r = dict(row)
        r["answers"] = json.loads(r["answers_json"])
        r["recommendations"] = json.loads(r["recommendations_json"])
        results.append(r)
    return results


# ──────────────────────────────────────────────
#  FAVORITES helpers
# ──────────────────────────────────────────────

def add_favorite(discord_id: str, career_id: str, career_name: str, career_data: dict) -> bool:
    """Returns True if added, False if already exists."""
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO favorites (discord_id, career_id, career_name, career_data_json) VALUES (?, ?, ?, ?)",
            (str(discord_id), career_id, career_name, json.dumps(career_data, ensure_ascii=False))
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def remove_favorite(discord_id: str, career_id: str) -> bool:
    conn = get_connection()
    cursor = conn.execute(
        "DELETE FROM favorites WHERE discord_id = ? AND career_id = ?",
        (str(discord_id), career_id)
    )
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted


def get_favorites(discord_id: str):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM favorites WHERE discord_id = ? ORDER BY added_at DESC",
        (str(discord_id),)
    ).fetchall()
    conn.close()
    results = []
    for row in rows:
        r = dict(row)
        r["career_data"] = json.loads(r["career_data_json"])
        results.append(r)
    return results


def is_favorite(discord_id: str, career_id: str) -> bool:
    conn = get_connection()
    row = conn.execute(
        "SELECT id FROM favorites WHERE discord_id = ? AND career_id = ?",
        (str(discord_id), career_id)
    ).fetchone()
    conn.close()
    return row is not None


# ──────────────────────────────────────────────
#  EXPLORE HISTORY helpers
# ──────────────────────────────────────────────

def log_explore(discord_id: str, sector: str):
    conn = get_connection()
    conn.execute(
        "INSERT INTO explore_history (discord_id, sector) VALUES (?, ?)",
        (str(discord_id), sector)
    )
    conn.commit()
    conn.close()
