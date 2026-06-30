from sqlalchemy import create_engine, text

DB_URL = "postgresql://test:test@localhost/test_db"

engine = create_engine(DB_URL, echo=True)

# # This transaction will not be commited, sqlalchemy will automatically rollback the transaction when the connection is closed
# with engine.connect() as connection:
#     results = connection.execute(text("select 'hello world'"))
#     print(results.all())

# # This transaction will be commited, we need to explicitly call commit() method -> commit as you go pattern
# with engine.connect() as connection:
#     with connection.begin():
#         connection.execute(
#             text("CREATE TABLE IF NOT EXISTS test_table (x int, y int)"),
#         )
#         connection.execute(
#             text("INSERT INTO test_table (x, y) VALUES (:x, :y)"),
#             [{"x": 1, "y": 1}, {"x": 2, "y": 4}],
#         )
#         connection.commit()

# # This transaction will be commited, we need to explicitly call commit() method -> begin once pattern
# with engine.begin() as connection:
#     connection.execute(
#         text("INSERT INTO test_table (x, y) VALUES (:x, :y)"),
#         [{"x": 6, "y": 8}, {"x": 9, "y": 10}],
#     )
#     # No need to call commit() method, the transaction will be commited when the block is exited if no exception is raised

with engine.connect() as connection:
    results = connection.execute(text("SELECT x, y FROM test_table"))
    for row in results:
        print(row) # each row is tuple-like
        print(f"x: {row.x}, y: {row.y}")

# we can send parameters to the query using the execute() method using the :param_name syntax in the query and passing a dictionary of parameters as the second argument to the execute() method
with engine.connect() as connection:
    results = connection.execute(
        text("SELECT x, y FROM test_table WHERE y > :y"), {"y": 5}
    )
    for row in results:
        print(f"x: {row.x}  y: {row.y}")

# we can send multiple parameters to the query using the execute() method by passing a list of dictionaries of parameters as the second argument to the execute() method
# with engine.connect() as connection:
#     results = connection.execute(
#         text("INSERT INTO test_table (x, y) VALUES (:x, :y)"),
#         [{"x": 11, "y": 12}, {"x": 13, "y": 14}]
#     )
#     connection.commit()

from sqlalchemy.orm import Session

statement = text("SELECT x, y FROM test_table WHERE y > :y ORDER BY x, y")
with Session(engine) as session:
    results = session.execute(statement, {"y": 5})
    for row in results:
        print(f"x: {row.x}  y: {row.y}")

# ORM also like Core has commit as you go pattern
with Session(engine) as session:
    session.execute(
        text("UPDATE test_table SET y = :y WHERE x = :x"),
        [{"x": 9, "y": 11}, {"x": 13, "y": 15}],
    )
    session.commit()