from typing import List
import json
import uuid
from abc import abstractmethod, ABC

import redis

from models import User


class DbService(ABC):
    @abstractmethod
    def get_list(self) -> List[User]: pass

    @abstractmethod
    def retrieve(self, user_id: str) -> User: pass

    @abstractmethod
    def create(self, data: dict) -> User: pass

    @abstractmethod
    def update(self, user_id: str, data: dict) -> User: pass

    @abstractmethod
    def delete(self, user_id: str) -> User: pass


class RedisDbService(DbService):
    def __init__(self, resource_name: str, url: str):
        self.resource_name = resource_name
        self.client = redis.Redis.from_url(url)

    def init_db(self, data: str):
        self.client.set(self.resource_name, data)

    def retrieve(self, user_id):
        users = self.get_resource()
        return users[user_id]

    def create(self, data):
        users = self.get_resource()
        newid = str(uuid.uuid4())
        data['id'] = newid
        users[newid] = data
        self.set_resource(users)
        return data

    def update(self, user_id, data):
        users = self.get_resource()
        users[user_id].update(data)
        self.set_resource(users)
        return data

    def delete(self, user_id):
        users = self.get_resource()
        del users[user_id]
        self.set_resource(users)

    def get_list(self):
        user_list = []
        users = self.get_resource()

        for key, item in users.items():
            user_list.append(item)

        return user_list

    def get_resource(self):
        return json.loads(self.client.get(self.resource_name))['users']

    def set_resource(self, users):
        self.client.set(self.resource_name, json.dumps(users))


class FileDbService(DbService):
    def __init__(self, resource_name: str, filename: str = 'mydb'):
        self.filename = filename
        self.resource_name = resource_name

    def retrieve(self, user_id):
        with open(self.filename, 'r') as mydb:
            tables = json.loads(mydb.read())
            return tables[self.resource_name][user_id]

    def create(self, data):
        with open(self.filename, 'r') as mydb:
            tables = json.loads(mydb.read())
            tables_changed = tables.copy()
            newid = str(uuid.uuid4())
            data['id'] = newid
            tables_changed['users'][newid] = data

        self.persist(tables_changed)
        return data

    def update(self, user_id, data):
        with open(self.filename, 'r') as mydb:
            tables = json.loads(mydb.read())
            tables_changed = tables.copy()
            tables_changed['users'][user_id].update(data)

        self.persist(tables_changed)
        return tables_changed['users'][user_id]

    def delete(self, user_id):
        with open(self.filename, 'r') as mydb:
            tables = json.loads(mydb.read())
            tables_changed = tables.copy()
            del tables_changed['users'][user_id]

        self.persist(tables_changed)

    def persist(self, data):
        with open(self.filename, 'w') as mydb:
            mydb.write(json.dumps(data))

    def get_list(self):
        with open(self.filename, 'r') as mydb:
            resource_list = []

            tables = json.loads(mydb.read())
            resources = tables[self.resource_name]

            for key, item in resources.items():
                resource_list.append(item)

            return resource_list


class UserService:
    RESOURCE_NAME = 'users'

    def __init__(self, db: DbService):
        self.db = db

    def retrieve(self, user_id: int) -> User:
        return self.as_user(self.db.retrieve(user_id))

    def create(self, data: dict) -> User:
        return self.as_user(self.db.create(data))

    def update(self, user_id: int, data: dict) -> User:
        return self.as_user(self.db.update(user_id, data))

    def as_user(self, data: dict) -> User:
        return User(**data)

    def delete(self, user_id: int) -> None:
        self.db.delete(user_id)

    def check_token(self, token: str) -> str:
        user_list = self.get_list()

        for user in user_list:
            if token == user.get('token', ''):
                return token
        return False

    def get_list(self):
        return self.db.get_list()
