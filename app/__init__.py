# For SQL support : Type "pip install flask-sqlalchemy" in Terminal in directory of project
# For ORM support : Type "pip install flask-migrate" in Terminal in directory of project
# For PG support : Type "pip install psycopg2" in Terminal in directory of project
# For Login plugins : Type "pip install flask-login" in Terminal in directory of project

from flask import Flask

from app.routes import profile
from config import Config
from app.models import db, login
from flask_migrate import Migrate


# 创建webapp应用,__name__是python预定义变量，被设置为使用本模块.
webapp = Flask(__name__)
webapp.register_blueprint(profile)
# 添加配置信息
webapp.config.from_object(Config)
# 建立数据库关系
db.init_app(webapp)
# 绑定app和数据库，以便进行操作
migrate = Migrate(webapp, db)
# 建立login和应用的关系
login.init_app(webapp)


# 如果你使用的IDE，在routes这里会报错，因为我们还没有创建呀，为了一会不要再回来写一遍，因此我先写上了
from app import routes, models
