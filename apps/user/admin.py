from django.contrib import admin
from .models import *
# Register your models here.
# from django.contrib.auth.admin import UserAdmin
# class UserProfileAdmin(UserAdmin):
#     # list_display = ['id', 'username', ]
#     ordering = (u'id',)
#     # fieldsets = (None, {'fields': (
#     # 'age', 'dept', 'nick_name', 'gender', 'address', 'mobile', 'is_superuser', 'is_staff', 'is_active',)}),
#     list_per_page = 5

# admin.site.register(User, UserProfileAdmin)

class PermissionAdmin(admin.ModelAdmin):
    list_display = ['title', 'url'] # 展示
    list_editable = ['url'] # 可编辑

admin.site.register(User)
# admin.site.register(Permission)
admin.site.register(Permission, PermissionAdmin)
admin.site.register(Organization)
admin.site.register(Role)
admin.site.register(Menu)

