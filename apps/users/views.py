from django.http import HttpResponse
from django.shortcuts import render,redirect,reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.backends import ModelBackend
from apps.users.models import UserProfile
from django.db.models import Q
from django.views.generic.base import View
from apps.users.forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm, UploadImageForm
from django.contrib.auth.hashers import make_password
from apps.utils.email_send import send_register_eamil
from apps.users.models import EmailVerifyRecord

#邮箱和用户名都可以登录
# 基础ModelBackend类，因为它有authenticate方法
from apps.utils.mixin_utils import LoginRequiredMixin


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 不希望用户存在两个，get只能有一个。两个是get失败的一种原因 Q为使用并集查询
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))

            # django的后台中密码加密：所以不能password==password
            # UserProfile继承的AbstractUser中有def check_password(self, raw_password):
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):
    def get(self,request):
        return render(request, 'login.html')

    def post(self,request):
        # 实例化
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # 获取用户提交的用户名和密码
            user_name = request.POST.get('username', None)
            pass_word = request.POST.get('password', None)
            # 成功返回user对象,失败None
            user = authenticate(username=user_name, password=pass_word)
            # 如果不是null说明验证成功
            if user is not None:
                if user.is_active==1:
                    # 著有注册激活才能登录
                    login(request, user)
                    return render(request, 'index.html')
                elif user.is_active == 0:
                    return render(request, 'login.html', {'msg': '用户未激活'})


            # 只有当用户名或密码不存在时，才返回错误信息到前端
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误','login_form':login_form})

        # form.is_valid（）已经判断不合法了，所以这里不需要再返回错误信息到前端了
        else:
            return render(request,'login.html',{'msg':'用户名或密码错误','login_form':login_form})




class RegisterView(View):
    # 用户注册
    def get(selfself,request):
        register_form=RegisterForm()
        return render(request,'register.html',{'register_form':register_form})
    def post(self,request):
        register_form=RegisterForm(request.POST)
        if register_form.is_valid():
            user_name=request.POST.get('email',None)
            # 如果用户已存在，则提示错误信息
            if UserProfile.objects.filter(email=user_name):
                return render(request,'register.html',{'register_form':register_form,'msg':'用户已存在'})
            pass_word=request.POST.get('password',None)
            # 实例化一个user_profile对象
            user_profile=UserProfile()
            user_profile.username=user_name
            user_profile.email=user_name
            user_profile.is_active=False
            # 对保存到数据库的密码加密
            user_profile.password=make_password(pass_word)
            user_profile.save()
            send_register_eamil(user_name,'register')
            return render(request,'login.html')
        else:
            return render(request,'register.html',{'register_form':register_form})


# 激活用户
class ActiveUserView(View):
    def get(self,request,active_code):
        # 查询邮箱验证记录是否存在
        all_record=EmailVerifyRecord.objects.filter(code=active_code)

        if all_record:
            for record in all_record:
                # 获取到对应的邮箱
                email=record.email
                # 查找到邮箱对应的user
                user =UserProfile.objects.get(email=email)
                user.is_active=True
                user.save()
                # 激活成功跳转到登陆页面
                return redirect(reverse('login'))
        else:
            return render(request,'register.html',{'msg':'激活失效'})

class ForgetPwdView(View):
    # 找回密码
    def get(self,request):
        forget_form = ForgetPwdForm()
        return render(request,'forgetpwd.html',{'forget_form':forget_form})

    def post(self,request):
        forget_form = ForgetPwdForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email',None)
            send_register_eamil(email,'forget')
            return render(request, 'send_success.html')
        else:
            return render(request,'forgetpwd.html',{'forget_form':forget_form})


class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "password_reset.html", {"email":email})
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")

class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email":email, "msg":"密码不一致！"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()

            return render(request, "login.html")
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email":email, "modify_form":modify_form })

class UserinfoView(LoginRequiredMixin,View):
    '''用户个人信息'''
    def get(self,request):
        return render(request,'users/usercenter-info.html',{})


class UploadImageView(LoginRequiredMixin,View):
    '''用户图像修改'''
    def post(self,request):
        #上传的文件都在request.FILES里面获取，所以这里要多传一个这个参数
        image_form = UploadImageForm(request.POST,request.FILES)
        if image_form.is_valid():
            image = image_form.cleaned_data['image']
            request.user.image = image
            request.user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')




