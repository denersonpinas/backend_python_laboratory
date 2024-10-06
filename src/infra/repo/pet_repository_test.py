from faker import Faker
from src.infra.entities import Pets
from src.infra.config import DBConnectionHandler
from src.infra.entities.animal_types import AnimalTypes
from sqlalchemy import text
from .pet_repository import PetRepository


faker = Faker()
pet_repository = PetRepository()
db_connection_handler = DBConnectionHandler()


def test_insert_pet():
    """Should insert pet in Pet table and return it"""

    name = faker.name()
    specie = "fish"
    age = faker.random_number(digits=1)
    user_id = faker.random_number()

    # SQL Commands
    new_pet = pet_repository.insert_pet(name, specie, age, user_id)
    engine = db_connection_handler.get_engine()

    with engine.begin() as conn:
        query_user = conn.execute(
            text("SELECT * FROM pets WHERE id='{}';".format(new_pet.id))
        ).fetchone()
        conn.commit()

    assert new_pet.id == query_user.id
    assert new_pet.name == query_user.name
    assert new_pet.specie == query_user.specie
    assert new_pet.age == query_user.age
    assert new_pet.user_id == query_user.user_id

    with engine.begin() as conn:
        conn.execute(text("DELETE FROM pets WHERE id='{}';".format(new_pet.id)))
        conn.commit()


def test_select_pet():
    """Should select a pet in Pets table and compare it"""

    pet_id = faker.random_number(digits=4)
    name = faker.name()
    specie = "fish"
    age = faker.random_number(digits=1)
    user_id = faker.random_number()

    specie_mock = AnimalTypes("fish")
    data = Pets(id=pet_id, name=name, specie=specie_mock, age=age, user_id=user_id)

    # SQL COmmands

    engine = db_connection_handler.get_engine()
    with engine.begin() as conn:
        conn.execute(
            text(
                "INSERT INTO pets (id, name, specie, age, user_id) VALUES ('{}', '{}', '{}', '{}', '{}');".format(
                    pet_id, name, specie, age, user_id
                )
            )
        )
        conn.commit()

    query_pets1 = pet_repository.select_pet(pet_id=pet_id)
    query_pets2 = pet_repository.select_pet(user_id=user_id)
    query_pets3 = pet_repository.select_pet(pet_id=pet_id, user_id=user_id)

    assert data in query_pets1
    assert data in query_pets2
    assert data in query_pets3

    with engine.begin() as conn:
        conn.execute(text("DELETE FROM pets WHERE id='{}';".format(pet_id)))
        conn.commit()
