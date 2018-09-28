# flask_script 使用命令行管理项目
from flask_script import Manager
# flask_migrate 数据库迁移脚本
from flask_migrate import Migrate,MigrateCommand
from pjke import app
from exts import db
from apps.cms.models import *
from apps.front.models import *
# flask-script的使用
manage = Manager(app)
# 要使用flask-migrate必须绑定app和db
Migrate(app,db)
# 把MigrateCommand(数据库迁移)命令添加到manager
manage.add_command("db",MigrateCommand)
@manage.option("-u","--username",dest="username")
@manage.option("-e","--email",dest="email")
@manage.option("-p","--password",dest="password")
def addUser(username,password,email):
    user = User(username=username,email=email,password=password)
    db.session.add(user)
    db.session.commit()
# 在命令行运行的指令: python 文件名称 函数名称 -u mafeifan -p mafeifan

@manage.option('-n','--rolename',dest='rolename')
@manage.option('-d','--roledesc',dest='roledesc')
@manage.option('-p','--permissions',dest='permissions')
def addcmsrole(rolename,roledesc,permissions):
    r = Role(roleName=rolename,desc=roledesc,permissions=permissions)
    db.session.add(r)
    db.session.commit()

@manage.option('-uid','--user_id',dest='user_id')
@manage.option('-rid','--role_id',dest='role_id')
def useraddrole(user_id,role_id):
    u = User.query.get(user_id)
    r = Role.query.get(role_id)
    u.roles.append(r)
    db.session.commit()



if __name__ == '__main__':
    manage.run()