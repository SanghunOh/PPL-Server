from flask import Blueprint
from flask import request
from flask_restx import Resource, Namespace, fields

from app.service.user_service import save_new_user, get_user, add_user_paper, delete_user_paper, delete_user_interest
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
    add_library = api.model('library_add', {
        'abstract':fields.String(required=True, description='abstract'),
        'author': fields.String(required=True, description='author'),
        'category': fields.String(required=True, description='category'),
        'link': fields.String(required=True, description='link'),
        'title': fields.String(required=True, description='title'),
        'year': fields.Integer(required=True, description='year'),
        'user_id': fields.Integer(required=True, description='User ID')
    })
    del_library = api.model('library_del', {
        'id': fields.Integer(required=True, description='User ID'),
        'user_id': fields.Integer(required=True, description='User ID')
    })
    add_interest = api.model('interest_add', {
    })
    del_category = api.model('interest_del', {
        'id': fields.Integer(required=True, description='User ID'),
        'user_id': fields.Integer(required=True, description='User ID')
    })

api = UserDto.api
parser = api.parser()
signup = UserDto.signup
signin = UserDto.signin
add_library = UserDto.add_library
del_library = UserDto.del_library

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
    
@api.route('/library')
@api.expect(parser)
class Users(Resource):
    @api.doc('library에 추가')
    @api.expect(add_library, validate=True)
    def post(self):
        return add_user_paper(request.json)
    
    @api.doc('library에서 삭제')
    @api.expect(del_library, validate=False)
    def delete(self):
        return delete_user_paper(request.json)
    
@api.route('/interest')
@api.expect(parser)
class Users(Resource):
    # @api.doc('library에 추가')
    # @api.expect(add_library, validate=True)
    # def post(self):
    #     return add_user_interest(request.json)
    
    @api.doc('interest에서 삭제')
    @api.expect(del_library, validate=False)
    def delete(self):
        return delete_user_interest(request.json)
