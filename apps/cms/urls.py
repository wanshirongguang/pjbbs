# 后台
from flask import Blueprint
from flask import render_template
from apps.cms.froms import UserForm,pwdForm,emailForm,emailcodeFrom,\
                            bannerFrom,updatebannerFrom,addBoaderFrom,\
                            updateboardFrom,deleteboardFrom
from flask import request,jsonify
from apps.common.baseResp import *
from apps.cms.models import *
from flask import session,views
import string,random
from flask_mail import Message
from apps.common.memcachedUtil import saveCache,getCache
from exts import db,mail
from functools import wraps
from apps.common.models import Banner,Board
from qiniu import Auth

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
@bp.route('/login/')
def ssss():
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
            rs = User.query.filter(User.username == session["username"]).first()
            rs.email = email
            db.session.commit()
            return jsonify(respSuccess(msg='修改成功'))
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
    banners = Banner.query.all()
    context = {
        'banners': banners
    }
    return render_template("cms/banner.html",**context)

@bp.route("/addbanner/",methods=["post"])
@lonigDecotor
@checkPermission(Permission.BANNER)
def addbanner():
    fm = bannerFrom(formdata=request.form)
    if fm.validate():
        banner = Banner(bannerName=fm.bannerName.data,
                        imglink=fm.imglink.data,
                        link=fm.link.data,
                        priority=fm.priority.data)
        db.session.add(banner)
        db.session.commit()
        return jsonify(respSuccess(msg='添加成功'))
    else:
        return jsonify(respParamErr(msg=fm.err))

@bp.route("/updatebanner/",methods=["post"])
@lonigDecotor
@checkPermission(Permission.BANNER)
def updateDanner():
    fm = updatebannerFrom(formdata=request.form)
    if fm.validate():
        r = Banner.query.filter(Banner.id == fm.id.data).first()
        r.bannerName = fm.bannerName.data
        r.imglink = fm.imglink.data
        r.link = fm.link.data
        r.priority = fm.priority.data
        db.session.commit()
        return jsonify(respSuccess(msg='更新成功'))
    else:
        return jsonify(respParamErr(msg=fm.err))

@bp.route("/deletebanner/",methods=["post"])
@lonigDecotor
@checkPermission(Permission.BANNER)
def deleteBanner():
    # 拿到客户端提交的id
    banner_id = request.values.get("id")
    if not banner_id or not banner_id.isdigit():
        return jsonify(respParamErr(msg='请输入正确banner_id'))
    # 从数据库删除
    banner = Banner.query.filter(Banner.id == banner_id).first()
    if banner:
        db.session.delete(banner)
        db.session.commit()
        return jsonify(respSuccess(msg='删除成功'))
    else:  # 没有
        return jsonify(respParamErr(msg='请输入正确banner_id'))

@bp.route("/qiniu_token/")
@lonigDecotor
@checkPermission(Permission.BANNER)
def qiniukey():
    # 通过secer-key id 生成一个令牌，返回给客户端
    ak = "gixRZTC9nnM_ODSEyAmDtFPVBD5sBWJo1dsfszvB"
    sk = "X8TYRWzELi-hfyzl1MeAkEbS9i5DKL_8qI4m_o3l"
    q = Auth(ak, sk)
    bucket_name = 'pjssb' # 仓库的名字
    token = q.upload_token(bucket_name)
    return jsonify({'uptoken': token})

@bp.route("/board/")
@lonigDecotor
@checkPermission(Permission.POSTS)
def board():
    board = Board.query.all()
    context = {
        'boards': board
    }
    return render_template("cms/board.html", **context)
@bp.route("/addboard/",methods=["post"])
@lonigDecotor
@checkPermission(Permission.POSTS)
def addboard():
    fm = addBoaderFrom(formdata=request.form)
    if fm.validate():
        board = Board(boardname=fm.boardname.data)
        db.session.add(board)
        db.session.commit()
        return jsonify(respSuccess(msg='添加成功'))
    else:
        return jsonify(respParamErr(msg=fm.err))

@bp.route("/updateboard/",methods=["post"])
@lonigDecotor
@checkPermission(Permission.POSTS)
def updateboard():
    fm  = updateboardFrom(formdata=request.form)
    if fm.validate():
        board = Board.query.filter(Board.id == fm.id.data).first()
        board.boardname = fm.boardname.data
        db.session.commit()
        return jsonify(respSuccess(msg='修改成功'))
    else:
        return jsonify(respParamErr(msg=fm.err))
@bp.route("/deleteboard/",methods=["post"])
@lonigDecotor
@checkPermission(Permission.POSTS)
def deleteboard():
    fm = deleteboardFrom(formdata=request.form)
    if fm.validate():
        board = Board.query.filter(Board.id == fm.id.data).first()
        db.session.delete(board)
        db.session.commit()
        return jsonify(respSuccess(msg='删除成功'))
    else:
        return jsonify(respParamErr(msg=fm.err))


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
