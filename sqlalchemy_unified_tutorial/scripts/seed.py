from sqlalchemy import insert, text

from models import engine, user_table, address_table, Base


def seed() -> None:
    # Reset so seeding is deterministic on every `docker compose up`.
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    with engine.begin() as conn:
        conn.execute(
            insert(user_table),
            [
                {"name": "Spongebob", "fullname": "Spongebob Squarepants"},
                {"name": "Sandy", "fullname": "Sandy Cheeks"},
                {"name": "Patrick", "fullname": "Patrick Star"},
            ],
        )
        conn.execute(
            insert(address_table),
            [
                {"user_id": 1, "email_address": "spongebob@sqlalchemy.org"},
                {"user_id": 2, "email_address": "sandy@sqlalchemy.org"},
                {"user_id": 3, "email_address": "patrick@sqlalchemy.org"},
            ],
        )

        # Raw table used by working_with_transactions_and_dbapi.py, which
        # expects it to already exist (its own CREATE is commented out).
        conn.execute(text("DROP TABLE IF EXISTS test_table"))
        conn.execute(text("CREATE TABLE test_table (x int, y int)"))
        conn.execute(
            text("INSERT INTO test_table (x, y) VALUES (:x, :y)"),
            [
                {"x": 1, "y": 1},
                {"x": 2, "y": 4},
                {"x": 6, "y": 8},
                {"x": 9, "y": 10},
            ],
        )

    print("Database seeded.")


if __name__ == "__main__":
    seed()
