# 用于SQLite数据库文件地址
# import os
# BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # 设置密匙要没有规律，别被人轻易猜到哦
    SECRET_KEY = '213E0B3979ECF2562087B03F04D0273B'

    # 数据库连接串
    # MySQL
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/db_name?charset=utf8'
    # SQLite
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR,'app.db')
    # PostgreSQL
    SQLALCHEMY_DATABASE_URI = 'postgresql://smartsys:a5000_zhjkb@localhost:5432/urination'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
