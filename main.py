# 从app模块中导入webapp应用
from app import webapp

# 防止被引用后执行，只有在当前模块中才可以使用
if __name__ == '__main__':
    webapp.run(ssl_context=('D:/000/urination_record/app/static/ssl/chenth_public.crt',
                            'D:/000/urination_record/app/static/ssl/chenth.key'))
