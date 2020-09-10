import os
import json

from services import RedisDbService, UserService

def main():
    data = os.environ.get('DATABASE_DATA')
    db_service = RedisDbService(
        UserService.RESOURCE_NAME,
        os.environ.get('REDIS_URL'))
    db_service.init_db(data)

if __name__ == '__main__':
    main()
