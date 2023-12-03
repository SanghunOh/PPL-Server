from flask import Blueprint
from flask import request
from flask_restx import Resource, Namespace, fields

from ..service.user_service import save_new_user, get_user
from ..service.forms import SignInForm, SignUpForm
from app.service.auth_helper import Auth

class UserDto:
    api = Namespace('user', description='')
    signup = api.model('user_signup', {
        'email': fields.String(required=True, description='user email address'),
        'password': fields.String(required=True, description='user password'),
        'passwordcheck': fields.String(required=True, description='user password check')
    })
    signin = api.model('user_signin', {
        'email': fields.String(required=True, description='user email address'),
        'password': fields.String(required=True, description='user password'),
    })
    library = api.model('user', {
        'id': fields.Integer(required=True, description='User ID'),
    })

api = UserDto.api
parser = api.parser()
signup = UserDto.signup
signin = UserDto.signin
library = UserDto.library

@api.route('/signin')
@api.expect(parser)
class Users(Resource):
    @api.doc('user 정보 조회')
    @api.expect(signin, validate=True)
    def post(self):
        email = request.json.get('email')
        return get_user(email)

@api.route('/signup')
@api.expect(parser)
class NewUser(Resource):
    @api.doc('sign up')
    @api.expect(signup, validate=False)
    def post(self):
        userData = request.json
        return save_new_user(userData)
