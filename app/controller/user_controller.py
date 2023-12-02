# from flask import request
# from flask_restx import Resource

# from ..util.dto import UserDto

# # user dto
# api = UserDto.api
# _user = UserDto.user
# verify_model = UserDto.user_verify
# user_email = UserDto.user_email
# major_email = UserDto.major_email
# report_email = UserDto.report_email

# parser = api.parser()
# # parser.add_argument('Authorization', location='headers')

# @api.route('')
# @api.expect(parser)
# class Users(Resource):
#     @api.doc('user 정보 조회')
#     def get(self):
#         '''user 정보 조회'''
#         # auth_header = request.headers.get('Authorization')
#         # res = Auth.middleware(data=auth_header)
#         if res['status'] == 'success':
#             return get_user(res['email'])
#         else:
#             return res

from flask import Blueprint
from flask import request
from flask_restx import Resource, Namespace, fields

from app.service.user_service import save_new_user, get_user
from ..service.forms import SignInForm, SignUpForm
from app.service.auth_helper import Auth

class UserDto:
    api = Namespace('user', description='')
    signup = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password1': fields.String(required=True, description='user password'),
        'password2': fields.String(required=True)
    })

    signin = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'password': fields.String(required=True, description='user password'),
    })

api = UserDto.api
parser = api.parser()
signup = UserDto.signup
signin = UserDto.signin

@api.route('/signin')
@api.expect(parser)
class Users(Resource):
    @api.doc('user 정보 조회')
    @api.expect(signin, validate=False)
    def post(self):
        print((request.json.get('email')))
        email = request.json.get('email')
        return get_user(email)

@api.route('/signup')
@api.expect(parser)
class NewUser(Resource):
    @api.doc('sign up')
    @api.expect(signup, validate=False)
    def post(self):
        print(request.data['email'])
        print(request.data)
        return get_user(request.data.email)
