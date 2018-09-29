# 前台
from flask import Blueprint,make_response
from flask import render_template,session
from flask import views,request,jsonify
from apps.front.froms import SendSmsCodeForm,SignupFrom,SigninFrom,FindpwdFrom,SendCodeForm
import string,random
from apps.common.baseResp import *
import json
from dysms_python.demo_sms_send import send_sms
from apps.common.captcha.xtcaptcha import Captcha
from io import BytesIO
from apps.common.memcachedUtil import saveCache,delete,getCache
from apps.front.models import *
from apps.common.models import Banner,Board
#
bp = Blueprint('front',__name__)




@bp.route("/")
def loginView():
    banners = Banner.query.order_by(Banner.priority.desc()).limit(4)
    board = Board.query.all()
    print(board[0].boardname)
    context = {
        'banners': banners,
        "boards":board
    }
    return render_template("front/index.html",**context)

class Signup(views.MethodView):
    def get(self):
        return render_template("front/signup.html")
    def post(self):
        fm = SignupFrom(formdata=request.form)
        if fm.validate():
            # 把这个用户保存到数据库中
            u = FrontUser(telephone=fm.telephone.data,
                          username=fm.username.data,
                          password=fm.password.data)
            db.session.add(u)
            db.session.commit()
            delete(fm.telephone.data)  # 注册成功，删除手机验证码
            return jsonify(respSuccess("注册成功，真不容易啊"))
        else:
            return jsonify(respParamErr(fm.err))

@bp.route("/send_sms_code/",methods=["post"])
def send_sms_code():
    fm =SendSmsCodeForm(formdata=request.form)
    if fm.validate():
        rs = string.digits
        rs = ''.join(random.sample(rs, 4))
        r = send_sms(phone_numbers=fm.telephone.data,
                     smscode=rs)
        print(json.loads(r.decode("utf-8"))['Code'])
# b'{"Message":"OK","RequestId":"26F47853-F6CD-486A-B3F7-7DFDCE119713","BizId":"102523637951132428^0","Code":"OK"}'
        if json.loads(r.decode("utf-8"))['Code'] == 'OK':
            saveCache(fm.telephone.data,rs,30*60)
            return jsonify(respSuccess(msg="短信验证码发送成功，请查收"))
        else:  # 发送失败
            return jsonify(respParamErr(msg="请检查网络"))
    else:
        return jsonify(respParamErr(fm.err))

@bp.route("/img_code/")
def ImgCode():
    # 生成6位的字符串
    # 把这个字符串放在图片上
    #  用特殊字体
    #  添加横线
    #  添加噪点
    text, img = Captcha.gene_code()  # 通过工具类生成验证码
    print(text)
    out = BytesIO()  # 初始化流对象
    img.save(out, 'png')  # 保存成png格式
    out.seek(0)  # 从文本的开头开始读
    saveCache(text, text, 60)
    resp = make_response(out.read())  # 根据流对象生成一个响应
    resp.content_type = "image/png"  # 设置响应头中content-type
    return resp

class Signin(views.MethodView):
    def get(self):
        location = request.headers.get("Referer")
        if not location:  # 如果直接输入的注册的连接，location为空
            location = '/'
        context = {
            'location': location
        }
        return render_template("front/signin.html",**context)
    def post(self):
        fm = SigninFrom(formdata=request.form)
        if fm.validate():
                rember = request.values.get("rember")
                if str(rember) == "1":  # 前端勾选了记住我
                    session.permanent = True  # 设置这个属性之后回去config访问过期天数，如果没有设置，默认是31天
                return jsonify(respSuccess(msg="登陆成功"))
        else:
            return jsonify(respParamErr(fm.err))

class FindPws(views.MethodView):
    def get(self):
        return render_template("front/findpwd.html")
    def post(self):
        fm = FindpwdFrom(formdata=request.form)
        if fm.validate():
            r = FrontUser.query.filter(FrontUser.telephone == fm.telephone.data).first()
            r.password = fm.password.data
            db.session.commit()
            return jsonify(respSuccess(msg="修改成功"))
        else:
            return jsonify(respParamErr(fm.err))
@bp.route("/sendcode/",methods=["post"])
def sendcode():
    fm =SendCodeForm(formdata=request.form)
    if fm.validate():
        rs = string.digits
        rs = ''.join(random.sample(rs, 4))
        r = send_sms(phone_numbers=fm.telephone.data,
                     smscode=rs)
# b'{"Message":"OK","RequestId":"26F47853-F6CD-486A-B3F7-7DFDCE119713","BizId":"102523637951132428^0","Code":"OK"}'

        if json.loads(r.decode("utf-8"))['Code'] == 'OK':
            saveCache(fm.telephone.data,rs,30*60)
            return jsonify(respSuccess(msg="短信验证码发送成功，请查收"))
        else:  # 发送失败
            return jsonify(respParamErr(msg="请检查网络"))
    else:
        return jsonify(respParamErr(fm.err))
bp.add_url_rule("/findpwd/",endpoint='findpwd',view_func=FindPws.as_view('findpwd'))
bp.add_url_rule("/signin/",endpoint='signin',view_func=Signin.as_view('signin'))
bp.add_url_rule("/signup/",endpoint='signup',view_func=Signup.as_view('signup'))