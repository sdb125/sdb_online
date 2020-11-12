from .models import UserProfile
import xadmin
from xadmin import views

class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

class GlobalSettings(object):
#     设置网站标题和页面
    site_title='在线教育'
    site_footer="Powered By 1906c-2020"
    menu_style = 'accordion'


class UserProfileAdmin(object):
    list_display =['username','gender','mobile','address']
    search_fields = ['username','gender','mobile','address']
    list_filter = ['username','gender','mobile','address']
    model_icon = 'fa fa-user'
    style_fields = {"address": "ueditor"}
    ordering = ['date_joined']    #排序
    readonly_fields = ['nick_name']    #只读字段，不能编辑
    exclude = ['gender']   #不显示字段
    list_editable = ['mobile']  #编辑字段
    # refresh_times = [3,5]


xadmin.site.unregister(UserProfile)
xadmin.site.register(UserProfile,UserProfileAdmin)
xadmin.site.register(views.CommAdminView,GlobalSettings)
xadmin.site.register(views.BaseAdminView,BaseSetting)