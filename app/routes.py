# 从app模块中即从__init__.py中导入创建的webapp应用
import base64
import json
import os
from datetime import datetime

import cv2
import requests
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename

from app.models import db
from flask import render_template, flash, redirect, url_for, request, Blueprint, g
from app.forms import LoginForm, RegistrationForm, EditProfileForm, LoginFormWx
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User


# 使用蓝图建立统一路由前缀，便于nginx部署多应用
profile = Blueprint('profile', __name__, url_prefix='/uu', static_folder='', static_url_path='')


# 主页
@profile.route('/')
@profile.route('/index')
# @login_required  # 这样，必须登录后才能访问首页了,否则会自动跳转至登录页
def index():
    print("Entry index function:")
    """
    user = {'username': 'duke'}
    posts = [
        {
            'author': {'username': '张三'},
            'body': '这是模板模块中的循环例子～1'

        },
        {
            'author': {'username': '李四'},
            'body': '这是模板模块中的循环例子～2'
        }
    ]
    return render_template('index.html', title='我的', user=user, posts=posts)
    """
    return render_template('index.html', title='我的')


# 登录
@profile.route('/login', methods=['GET', 'POST'])
def login():
    print("Entry login function:")
    # 判断当前用户是否验证，如果通过的话返回首页
    if current_user.is_authenticated:
        return redirect(url_for('profile.index'))

    # 创建一个表单实例
    form = LoginForm()
    # 验证表格中的数据格式是否正确
    if form.validate_on_submit():
        # 根据表格里的数据进行查询，如果查询到数据返回User对象，否则返回None
        tmp_user = User.query.filter_by(username=form.username.data).first()
        # 判断用户不存在或者密码不正确
        if tmp_user is None or not tmp_user.check_password(form.password.data):
            # 如果用户不存在或者密码不正确就会闪现这条信息
            flash('无效的用户名或密码')
            # 然后重定向到登录页面
            return redirect(url_for('profile.login'))
        # 这是一个非常方便的方法，当用户名和密码都正确时来解决记住用户是否记住登录状态的问题
        login_user(tmp_user, remember=form.remember_me.data)
        # 此时的next_page记录的是跳转至登录页面时的地址
        next_page = request.args.get('next')
        # 如果next_page记录的地址不存在那么就返回首页
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('profile.index')
        # 综上，登录后要么重定向至跳转前的页面，要么跳转至首页
        return redirect(next_page)
    # 首次登录/数据格式错误都会是在登录界面
    return render_template('login.html', title='登 录', form=form)


# 测试微信登录
@profile.route('/login_wx', methods=['GET', 'POST'])
def login_wx():
    print("Entry login_wx function:")
    # 判断当前用户是否验证，如果通过的话返回首页
    if current_user.is_authenticated:
        print("login_wx: user is already authenticated")
        return redirect(url_for('profile.index'))

    # 创建一个表单实例
    form = LoginFormWx()
    print("login_wx: username=%s, password=%s" % (form.username.data, form.password.data))
    # 根据表格里的数据进行查询，如果查询到数据返回User对象，否则返回None
    tmp_user = User.query.filter_by(username=form.username.data).first()
    # 判断用户不存在或者密码不正确
    if tmp_user is None or not tmp_user.check_password(form.password.data):
        # 如果用户不存在或者密码不正确就会闪现这条信息
        flash('无效的用户名或密码')
        print('登陆失败')
        return "Login fail"
    # 这是一个非常方便的方法，当用户名和密码都正确时来解决记住用户是否记住登录状态的问题
    login_user(tmp_user)
    print('登录成功')
    return "Login success"


# 登出
@profile.route('/logout')
def logout():
    print("Entry logout function:")
    logout_user()
    return redirect(url_for('profile.index'))


# 新用户注册
@profile.route('/register', methods=['GET', 'POST'])
def register():
    print("Entry register function:")
    # 判断当前用户是否验证，如果通过的话返回首页
    if current_user.is_authenticated:
        return redirect(url_for('profile.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        tmp_user = User(username=form.username.data, email=form.email.data)
        tmp_user.set_password(form.password.data)
        db.session.add(tmp_user)
        db.session.commit()
        flash('新用户注册成功，即将进入登录页面')
        return redirect(url_for('profile.login'))
    return render_template('register.html', title='注册', form=form)


# 用户资料
@profile.route('/user/<username>')
@login_required
def user(username):
    print("Entry user function:")
    tmp_user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': tmp_user, 'body': '测试Post #1号'},
        {'author': tmp_user, 'body': '测试Post #2号'}
    ]
    return render_template('user.html', user=tmp_user, posts=posts,
                           file=profile.url_prefix + '/static/images/WALL-E.jpg')


# 更新最近请求时间
@profile.before_request
def before_request():
    print("Entry before_request function:")
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


# 编辑个人资料
@profile.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    print("Entry edit_profile function:")
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data

        current_user.nickname = form.nickname.data
        current_user.gender = form.gender.data
        current_user.id_card = form.id_card.data
        current_user.phone = form.phone.data
        current_user.birthday = form.birthday.data
        current_user.drg = form.drg.data
        current_user.description = form.description.data
        db.session.commit()
        flash('你的提交已变更.')
        return redirect(url_for('profile.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
        form.nickname.data = current_user.nickname
        form.gender.data = current_user.gender
        form.id_card.data = current_user.id_card
        form.phone.data = current_user.phone
        form.birthday.data = current_user.birthday
        form.drg.data = current_user.drg
        form.description.data = current_user.description
    return render_template('edit_profile.html', title='个人资料编辑', form=form)


# 编辑个人资料
@profile.route('/a', methods=['GET', 'POST'])
def test_a():
    print("Entry test_a function:")
    return "this is a"


# 编辑个人资料
@profile.route('/b', methods=['GET', 'POST'])
def test_b():
    print("Entry test_b function:")
    return "this is b"


# OCR测试
@profile.route('/ocr', methods=['POST', 'GET'])
def ocr():
    basepath = os.path.dirname(__file__)  # 当前文件所在路径
    print(request.method)
    if request.method == 'POST':
        f = request.files['file']
        upload_path = os.path.join(basepath, 'static/uploads', secure_filename(f.filename))  # 注意：没有的文件夹要先创建
        f.save(upload_path)
        return redirect(url_for('profile.ocr_result', pic_name=f.filename))
    else:
        return render_template('ocr.html')


# OCR测试结果
@profile.route('/ocr/<pic_name>', methods=['POST', 'GET'])
def ocr_result(pic_name):
    basepath = os.path.dirname(__file__)  # 当前文件所在路径
    print(request.method)
    if pic_name != "":
        upload_path = os.path.join(basepath, 'static/uploads', secure_filename(pic_name))
        data = {'images': [cv2_to_base64(cv2.imread(upload_path))]}
        headers = {"Content-type": "application/json"}
        url = "http://127.0.0.1:8866/predict/chinese_ocr_db_crnn_mobile"
        # 图像识别服务： hub.exe serving start -m chinese_ocr_db_crnn_mobile -p 8866
        r = requests.post(url=url, headers=headers, data=json.dumps(data))
        # 打印预测结果
        results = r.json()["results"][0]["data"]
        print(upload_path.replace(basepath, profile.url_prefix))
        return render_template('ocr.html', results=results, file=upload_path.replace(basepath, profile.url_prefix))
    else:
        return render_template('ocr.html')


def cv2_to_base64(image):
    data = cv2.imencode('.jpg', image)[1]
    return base64.b64encode(data.tostring()).decode('utf8')
