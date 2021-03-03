# 从app模块中即从__init__.py中导入创建的webapp应用
from datetime import datetime

from werkzeug.urls import url_parse

from app import webapp, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, EditProfileForm, LoginFormWx
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User


# 建立路由，通过路由可以执行其覆盖的方法，可以多个路由指向同一个方法。


# 主页
@webapp.route('/')
@webapp.route('/index')
@login_required # 这样，必须登录后才能访问首页了,否则会自动跳转至登录页
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
@webapp.route('/login', methods=['GET', 'POST'])
def login():
    print("Entry login function:")
    # 判断当前用户是否验证，如果通过的话返回首页
    if current_user.is_authenticated:
        return redirect(url_for('index'))

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
            return redirect(url_for('login'))
        # 这是一个非常方便的方法，当用户名和密码都正确时来解决记住用户是否记住登录状态的问题
        login_user(tmp_user, remember=form.remember_me.data)
        # 此时的next_page记录的是跳转至登录页面时的地址
        next_page = request.args.get('next')
        # 如果next_page记录的地址不存在那么就返回首页
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        # 综上，登录后要么重定向至跳转前的页面，要么跳转至首页
        return redirect(next_page)
    # 首次登录/数据格式错误都会是在登录界面
    return render_template('login.html', title='登 录', form=form)


# 测试微信登录
@webapp.route('/login_wx', methods=['GET', 'POST'])
def login_wx():
    print("Entry login_wx function:")
    # 判断当前用户是否验证，如果通过的话返回首页
    if current_user.is_authenticated:
        print("login_wx: user is already authenticated")
        return redirect(url_for('index'))

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
@webapp.route('/logout')
def logout():
    print("Entry logout function:")
    logout_user()
    return redirect(url_for('index'))


# 新用户注册
@webapp.route('/register', methods=['GET', 'POST'])
def register():
    print("Entry register function:")
    # 判断当前用户是否验证，如果通过的话返回首页
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        tmp_user = User(username=form.username.data, email=form.email.data)
        tmp_user.set_password(form.password.data)
        db.session.add(tmp_user)
        db.session.commit()
        flash('新用户注册成功，即将进入登录页面')
        return redirect(url_for('login'))
    return render_template('register.html', title='注册', form=form)


# 用户资料
@webapp.route('/user/<username>')
@login_required
def user(username):
    print("Entry user function:")
    tmp_user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': tmp_user, 'body': '测试Post #1号'},
        {'author': tmp_user, 'body': '测试Post #2号'}
    ]
    return render_template('user.html', user=tmp_user, posts=posts, file='/static/images/WALL-E.jpg')


# 更新最近请求时间
@webapp.before_request
def before_request():
    print("Entry before_request function:")
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


# 编辑个人资料
@webapp.route('/edit_profile', methods=['GET', 'POST'])
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
        return redirect(url_for('edit_profile'))
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
@webapp.route('/a', methods=['GET', 'POST'])
def test_a():
    print("Entry test_a function:")
    return "this is a"


# 编辑个人资料
@webapp.route('/b', methods=['GET', 'POST'])
def test_b():
    print("Entry test_b function:")
    return "this is b"
