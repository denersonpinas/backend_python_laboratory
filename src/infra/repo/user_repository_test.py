from faker import Faker
from src.infra.config import DBConnectionHandler
from .user_repository import UserRepository
from sqlalchemy import text

faker = Faker()
user_repository = UserRepository()
db_connection_handler = DBConnectionHandler()


def test_insert_user():
    """Should Insert User"""

    name = faker.name()
    password = faker.word()
    engine = db_connection_handler.get_engine()

    # SQL Commands
    new_user = user_repository.insert_user(name, password)
    with engine.begin() as conn:
        query_user = conn.execute(
            text("SELECT * FROM users WHERE id='{}';".format(new_user.id))
        ).fetchone()
        conn.commit()

    with engine.begin() as conn:
        conn.execute(text("DELETE FROM users WHERE id='{}';".format(new_user.id)))
        conn.commit()

    assert new_user.id == 1
    assert new_user.name == query_user.name
    assert new_user.password == query_user.password
