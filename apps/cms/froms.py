# 进行表单校验
from flask_wtf import FlaskForm
from wtforms import IntegerField,StringField
from wtforms.validators import Email,InputRequired,Length,EqualTo
from apps.cms.models import User
from wtforms.validators import ValidationError
from apps.common.memcachedUtil import getCache
class BaseForm(FlaskForm):
    @property    # 把函数变成了属性来调用
    def err(self):
        return self.errors.popitem()[1][0]


class UserForm(BaseForm):
    email = StringField(validators=[Email(message="必须为邮箱"),InputRequired(message="不能为空")])
    password = StringField(validators=[InputRequired(message="必须输入密码"),Length(min=6,max=40,message="密码长度是6-40位")])


class pwdForm(BaseForm):
    oldpassword = StringField(validators=[InputRequired(message="必须输入密码"),Length(min=6,max=40,message="密码长度是6-40位")])
    newpassword1 = StringField(validators=[InputRequired(message="必须输入密码"),Length(min=6,max=40,message="密码长度是6-40位")])
    newpassword2 = StringField(validators=[InputRequired(message="必须输入密码"),EqualTo("newpassword1",message="两次密码不一致"),Length(min=6,max=40,message="密码长度是6-40位")])

class emailForm(BaseForm):
    email = StringField(validators=[Email(message="必须为邮箱"), InputRequired(message="不能为空")])
    def validate_email(self,filed):
        user = User.query.filter(User.email == filed.data).first()
        if user:
            raise ValidationError('邮箱已注册')
class emailcodeFrom(emailForm):
    email = StringField(validators=[Email(message="必须为邮箱"), InputRequired(message="不能为空")])
    code = StringField(validators=[InputRequired(message="必须输入验证码"),Length(min=6,max=6,message="密码长度是6位")])
    def validate_code(self,filed):
        emailcode = getCache(filed.data)
        # upper()  不区别大小写
        print("校验验证码")
        if not emailcode or emailcode != filed.data.upper():
            raise ValidationError('请输入正确的邮箱验证码')


