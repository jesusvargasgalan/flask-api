import os

from flask import Flask, request
from flask.json import jsonify
from flask_httpauth import HTTPTokenAuth

from services import UserService, RedisDbService

app = Flask(__name__)
auth = HTTPTokenAuth(scheme='Bearer')
app.config['DATABASE_NAME'] = 'mydb'
app.config['REDIS_URL'] = os.environ.get('REDIS_URL')
user_service = UserService(
    RedisDbService(
        UserService.RESOURCE_NAME,
        app.config['REDIS_URL'])
)

@auth.verify_token
def verify_token(token):
    return user_service.check_token(token)

@app.route('/api/v1/users')
def get_user_list():
    return jsonify(user_service.get_list())


@app.route('/api/v1/users', methods=['POST'])
@auth.login_required
def create_user():
    user = user_service.create(request.json)
    return jsonify(user)


@app.route('/api/v1/users/<user_id>')
def get_user(user_id):
    user = user_service.retrieve(user_id)
    return jsonify(user)


@app.route('/api/v1/users/<user_id>', methods=['PUT'])
@auth.login_required
def update_user(user_id):
    user = user_service.update(user_id, request.json)
    return jsonify(user)


@app.route('/api/v1/users/<user_id>', methods=['DELETE'])
@auth.login_required
def delete_user(user_id):
    user = user_service.delete(user_id)
    return '', 204
