from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# 用户模型
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    """
    back是反向引用,User和Post是一对多的关系，backref是表示在Post中新建一个属性author，关联的是Post中的user_id外键关联的User对象。
    lazy属性常用的值的含义，select就是访问到属性的时候，就会全部加载该属性的数据;joined则是在对关联的两个表进行join操作，从而获取到所有相关
    的对象;dynamic则不一样，在访问属性的时候，并没有在内存中加载数据，而是返回一个query对象, 需要执行相应方法才可以获取对象，比如.all()
    """
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    # 返回格式
    def __repr__(self):
        return '<用户名:{}>'.format(self.username)

    # 设置密码
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # 校验密码
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 头像,获取本地图片流
    def return_img_stream(self):
        import base64
        img_stream = ''
        with open('E:/test/PycharmProjects/urination_record/res/images/WALL-E.jpg', 'r') as img_f:
            img_stream = img_f.read()
            img_stream = base64.b64encode(img_stream)
        return img_stream


# 发帖模型
class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db .Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


# 在定义完数据类型以后，在Terminal中依次执行
# 数据库初始化指令：flask db init
# 数据库管理工具创建指令（针对表）：flask db migrate -m 'users_table'
# 将前一条指令提交到数据库中，即ORM数据库建表：flask db upgrade
# 数据库管理工具创建指令（针对表）：flask db migrate -m 'posts_table'
# 将前一条指令提交到数据库中，即ORM数据库建表：flask db upgrade
