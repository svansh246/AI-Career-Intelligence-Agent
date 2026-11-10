import sqlite3
import json
from pathlib import Path
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "career_assistant.db"


def get_connection():

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    return conn


def initialize_database():

    with get_connection() as conn:

        conn.execute("""
            CREATE TABLE IF NOT EXISTS analysis_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name TEXT,
                resume_name TEXT,
                target_domain TEXT,
                readiness_score REAL,
                skills TEXT,
                profile TEXT,
                created_at TEXT NOT NULL
            )
        """)

        conn.commit()


def save_analysis(
    user_name,
    resume_name,
    target_domain,
    readiness_score,
    skills,
    profile
):

    created_at = datetime.now().isoformat(
        timespec="seconds"
    )

    with get_connection() as conn:

        cursor = conn.execute(
            """
            INSERT INTO analysis_history (
                user_name,
                resume_name,
                target_domain,
                readiness_score,
                skills,
                profile,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_name,
                resume_name,
                target_domain,
                readiness_score,
                json.dumps(
                    skills,
                    ensure_ascii=False
                ),
                json.dumps(
                    profile,
                    ensure_ascii=False,
                    default=str
                ),
                created_at
            )
        )

        conn.commit()

        return cursor.lastrowid


def get_analysis_history(limit=50):

    with get_connection() as conn:

        rows = conn.execute(
            """
            SELECT *
            FROM analysis_history
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,)
        ).fetchall()


    results = []


    for row in rows:

        item = dict(row)

        item["skills"] = json.loads(
            item["skills"] or "[]"
        )

        item["profile"] = json.loads(
            item["profile"] or "{}"
        )

        results.append(item)


    return results


def get_analysis_by_id(analysis_id):

    with get_connection() as conn:

        row = conn.execute(
            """
            SELECT *
            FROM analysis_history
            WHERE id = ?
            """,
            (analysis_id,)
        ).fetchone()


    if row is None:

        return None


    item = dict(row)

    item["skills"] = json.loads(
        item["skills"] or "[]"
    )

    item["profile"] = json.loads(
        item["profile"] or "{}"
    )


    return item


def delete_analysis(analysis_id):

    with get_connection() as conn:

        conn.execute(
            """
            DELETE FROM analysis_history
            WHERE id = ?
            """,
            (analysis_id,)
        )

        conn.commit()


def clear_analysis_history():

    with get_connection() as conn:

        conn.execute(
            "DELETE FROM analysis_history"
        )

        conn.commit()