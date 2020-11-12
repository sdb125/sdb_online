import xadmin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.views.static import serve
from MxOnline.settings import MEDIA_ROOT
from apps.users.views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, ResetView, ModifyPwdView
# from apps.organization.views import OrgView

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('media/<path:path>',serve,{'document_root':MEDIA_ROOT}),
    path('ueditor/',include('DjangoUeditor.urls')),
    path('', TemplateView.as_view(template_name='index.html'),name='index'),
    # path('login/', TemplateView.as_view(template_name='login.html'),name='login'),
    path('login/',LoginView.as_view(),name = 'login'),     #修改login路由
    path('register/',RegisterView.as_view(),name = 'register'),
    path('captcha/', include('captcha.urls')),
    re_path('active/(?P<active_code>.*)/',ActiveUserView.as_view(),name='user_active'),
    path('forget/', ForgetPwdView.as_view(), name='forget_pwd'),
    re_path('reset/(?P<active_code>.*)/', ResetView.as_view(), name='reset_pwd'),
    path('modify_pwd/', ModifyPwdView.as_view(), name='modify_pwd'),
    path("org/", include('apps.organization.urls', namespace="org")),
    # 处理图片显示的url,使用Django自带serve,传入参数告诉它去哪个路径找，我们有配置好的路径MEDIAROOT
    re_path(r'^media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT }),
    path("course/", include('apps.course.urls', namespace="course")),
    path("users/", include('apps.users.urls', namespace="users")),

]