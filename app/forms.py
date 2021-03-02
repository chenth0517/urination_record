# For form component： Type "pip install flask-wtf" in Terminal in directory of project
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, RadioField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from app.models import User


# 登录表单
class LoginForm(FlaskForm):
    # DataRequired，当你在当前表格没有输入而直接到下一个表格时会提示你输入
    username = StringField('用户名', validators=[DataRequired(message='请输入名户名')])
    password = PasswordField('密码', validators=[DataRequired(message='请输入密码')])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')


# 微信登录表单
class LoginFormWx(FlaskForm):
    # DataRequired，当你在当前表格没有输入而直接到下一个表格时会提示你输入
    username = StringField()
    password = PasswordField()


# 注册表单
# For email validation support： Type "pip install email-validator" in Terminal in directory of project
class RegistrationForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    password2 = PasswordField('重复密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('注册')

    # 校验用户名是否重复
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('用户名重复')

    # 校验邮箱是否重复
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('邮箱重复')


# 个人资料
class EditProfileForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(message='请输入用户名!')])
    about_me = TextAreaField('关于我', validators=[Length(min=0, max=140)])
    nickname = StringField('真实姓名')
    gender = RadioField('性别', choices=['男', '女'])
    id_card = StringField('身份证号')
    phone = StringField('手机号')
    birthday = StringField('yyyy-mm-dd')
    # region = db.Column(db.Integer)  # 新增。区域
    drg = StringField('主诉类型')
    # type = db.Column(db.Integer, default=0)  # 新增。患者类型：1-估算，0-精确
    description = StringField('症状描述')
    submit = SubmitField('提交')
    form_widget_args = {
        'username': {
            'readonly': True
        }
    }
