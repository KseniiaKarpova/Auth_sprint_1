import typer
import asyncio
from storages.user import UserStorage
from core.hasher import DataHasher


def create(login: str, password: str):
    try:
        storage = UserStorage()
        hashed_password = asyncio.run(DataHasher().generate_word_hash(secret_word=password))

        asyncio.run(storage.create(params={
           'password': hashed_password,
           'login': login,
           'is_superuser': True,
        }))
        print(f"Creating Super User: {login}")

    except Exception as e:
        print('Can`t create Super User')
        print(e)


if __name__ == "__main__":
    typer.run(create)
