from django.urls import path,include,re_path
from apps.users.views import UserinfoView, UploadImageView

app_name = 'users'

urlpatterns = [
    #用户信息
    path("info/", UserinfoView.as_view(),name='user_info'),
#用户图像上传
    path("image/upload", UploadImageView.as_view(),name='image_upload'),


]