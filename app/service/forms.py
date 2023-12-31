from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class SignInForm(FlaskForm):
    password1 = PasswordField('비밀번호', validators=[DataRequired()])
    email = EmailField('이메일', validators=[DataRequired(), Email()])

class SignUpForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired()])
    password1 = PasswordField('비밀번호', validators=[
        DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired()])
    email = EmailField('이메일', validators=[DataRequired(), Email()])