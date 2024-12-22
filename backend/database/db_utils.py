import psycopg2

from backend.database.connection import get_connection


def load_words_to_db(file_path: str):
    with open(file_path, 'r') as f:
        all_words = [line.strip() for line in f if line.strip()]

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.executemany("""
                    INSERT INTO words (word, sorted_word)
                    VALUES (%s, %s)
                    ON CONFLICT (word) DO NOTHING;
                """, [(w, ''.join(sorted(w))) for w in all_words])
                conn.commit()

    except FileNotFoundError as e:
        raise FileNotFoundError(f"File error: {e}")
    except psycopg2.DatabaseError as e:
        raise psycopg2.DatabaseError(f"Database error: {e}")
    except ValueError as e:
        raise ValueError(f"Data error: {e}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {e}")