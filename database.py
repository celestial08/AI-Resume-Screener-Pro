import sqlite3

# =========================
# DATABASE CONNECTION
# =========================

conn = sqlite3.connect(
    "resume_screener.db",
    check_same_thread=False
)

cursor = conn.cursor()

# =========================
# CREATE TABLE
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidate_name TEXT,
    email TEXT,
    phone TEXT,
    score REAL,
    skills TEXT
)
""")

conn.commit()

# =========================
# INSERT CANDIDATE
# =========================

def insert_candidate(
    name,
    email,
    phone,
    score,
    skills
):

    cursor.execute(
        """
        INSERT INTO candidates
        (
            candidate_name,
            email,
            phone,
            score,
            skills
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            name,
            email,
            phone,
            score,
            skills
        )
    )

    conn.commit()

# =========================
# GET ALL CANDIDATES
# =========================

def get_candidates():

    cursor.execute(
        """
        SELECT *
        FROM candidates
        ORDER BY score DESC
        """
    )

    return cursor.fetchall()

# =========================
# DELETE CANDIDATE
# =========================

def delete_candidate(candidate_id):

    cursor.execute(
        """
        DELETE FROM candidates
        WHERE id = ?
        """,
        (candidate_id,)
    )

    conn.commit()

# =========================
# TEST DATABASE
# =========================

if __name__ == "__main__":

    print("Database Connected Successfully ✅")

    data = get_candidates()

    print(data)