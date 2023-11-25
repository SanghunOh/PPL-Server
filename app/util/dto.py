from flask_restx import Namespace, fields

class UserDto:
    api = Namespace('user', description='sogang-register related operations')
    user = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        'major':  fields.List(fields.String(description='user major'),required=True),
        'allow_email': fields.Boolean(required=True, description='allow email alert or not')
    })
    # 새로운 user의 email 인증과 관련해서 request를 email, access code 두 개로 하려고 하는데 괜찮겠지?
    user_verify = api.model('user_verify', {
        'email': fields.String(required=True, description='user email address'),
        'script': fields.String(required=True, description='access code sent to user email'),
    })
    user_email = api.model('user_email', {
        'email': fields.String(required=True, description='user email address'),
    })
    major_email = api.model('major_alert', {
        'major':  fields.List(fields.String(description='user major'),required=True),
        'allow_email': fields.Boolean(required=True, description='allow email alert or not')
    })
    report_email = api.model('report_email', {
        'email': fields.String(required=True, description='user email address'),
        'title': fields.String(required=True, description='title'),
        'script': fields.String(required=True, description='body'),
    })