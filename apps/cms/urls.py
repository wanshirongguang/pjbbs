# 后台
from flask import Blueprint
from flask import render_template
from apps.cms.froms import UserForm,pwdForm,emailForm,emailcodeFrom
from flask import request,jsonify
from apps.common.baseResp import *
from apps.cms.models import *
from flask import session,views
import string,random
from flask_mail import Message
from apps.common.memcachedUtil import saveCache,getCache
from exts import db,mail
from functools import wraps

bp = Blueprint('cms',__name__,url_prefix="/cms")
def lonigDecotor(func):
    """限制登录的装饰器"""
    @wraps(func)
    def inner(*args,**kwargs):
        if not session.get("username"):
            return render_template("cms/login.html")
        else:
            r = func(*args,**kwargs)
            return r
    return inner

def checkPermission(permission):
    def outer(func):
        @wraps(func)
        def inner(*args,**kwargs):
            # 取出来当前的用户， 判断这个用户有没有这个权限
            username = session.get("username")
            print("这是用户名"+username)
            user = User.query.filter(User.username ==username).first()
            print("这是整个信息"+str(user))
            r = user.checkpermission(permission)
            if r:
                return func(*args,**kwargs)
            else:
                return render_template("cms/login.html")
        return inner
    return outer


@bp.route("/")
def loginView():
    return render_template("cms/login.html")

@bp.route('/login/',methods=["post"])
def login():
    fm = UserForm(formdata=request.form)
    if fm.validate():
        email = fm.email.data
        password = fm.password.data
        r = User.query.filter(User.email == email).first()
        if not r :
            return jsonify(respParamErr(msg="用户名错误"))
        else:
            session["username"] = r.username
            if r.checkPwd(password):
                rember = request.values.get("rember")
                if str(rember) == "1":  # 前端勾选了记住我
                    session.permanent = True  # 设置这个属性之后回去config访问过期天数，如果没有设置，默认是31天
                return jsonify(respSuccess('登陆成功'))
            else:
                return jsonify(respParamErr("密码错误"))
    else:
        return jsonify(respParamErr(msg=fm.err))

@bp.route("/index/")
@lonigDecotor
def cms_index():
        return render_template("cms/index.html")


@bp.route("/information/")
@lonigDecotor
@checkPermission(Permission.USER_INFO)
def information():
        r = User.query.filter(User.username == session["username"]).first()
        context = {
            "user":r,
        }
        return render_template("cms/personalInfo.html",**context)

class resetPwd(views.MethodView):
    # 给类视图添加装饰器
    decorators = [checkPermission(Permission.USER_INFO),lonigDecotor]
    def get(self):
        return render_template("cms/resetpwd.html")
    def post(self):
        fm = pwdForm(formdata=request.form)
        if fm.validate():
            username = session["username"]
            r = User.query.filter(User.username == username).first()
            r.password = fm.newpassword1.data
            db.session.commit()
            return jsonify(respSuccess("修改成功"))
        else:
            return jsonify(respParamErr(msg=fm.err))

class resetEamil(views.MethodView):

    decorators = [checkPermission(Permission.USER_INFO),lonigDecotor]

    def get(self):
        return render_template("cms/resetemail.html")
    def post(self):
        fm = emailcodeFrom(formdata=request.form)
        if fm.validate():
            email = fm.email.data
            # if getCache(fm.email.data) == fm.code.data.upper():
            #     r = User.query.filter(User.email == email).first()
            #     if not r:
            rs = User.query.filter(User.username == session["username"]).first()
            rs.email = email
            db.session.commit()
            return jsonify(respSuccess(msg='修改成功'))
            #     else:
            #         return jsonify(respParamErr(msg="邮箱已被使用"))
            # else:
            #     return jsonify(respParamErr(msg="验证码错误"))
        else:
            return jsonify(respParamErr(msg=fm.err))

bp.add_url_rule("/reseteamil/",endpoint="reseteamil",view_func=resetEamil.as_view("reseteamil"))
bp.add_url_rule("/resetpwd/",endpoint="resetpwd",view_func=resetPwd.as_view("resetpwd"))

@bp.route("/send_email/",methods=["post"])
@lonigDecotor
@checkPermission(Permission.USER_INFO)
def send_email():
    fm = emailForm(formdata=request.form)
    if fm.validate():
        email = fm.email.data
        r = User.query.filter(User.email == email).first()
        if not r :
            r = string.ascii_letters + string.digits
            r = ''.join(random.sample(r, 6))
            saveCache(fm.email.data, r.upper(), 30 * 60)
            msg = Message("破茧科技更新邮箱验证码", recipients=[fm.email.data], body="验证码为" + r)
            mail.send(msg)
            return jsonify(respSuccess(msg='发送成功，请查看邮箱'))
    else:
        return jsonify(respParamErr(msg=fm.err))

@bp.route("/banner/")
@lonigDecotor
@checkPermission(Permission.BANNER)
def banner():
    return render_template("cms/banner.html")




# 每次请求的时候都会执行，返回字典可以直接在模板中使用
@bp.context_processor
def requestUser():
    username = session.get("username")
    if username == None:
        return {}
    else:
        r = User.query.filter(User.username == username).first()
        return {"user":r}

@bp.route("/send_email/",methods=["get"])
def ss():
    return render_template("cms/login.html")
