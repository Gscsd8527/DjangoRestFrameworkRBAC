from django.contrib import admin
from apps.cororateInfo.models import Information, AllInformation

class InformationAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', ]
    ordering = (u'id',)

class AllInformationAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', ]
    ordering = (u'id',)


admin.site.register(Information, InformationAdmin)
admin.site.register(AllInformation, AllInformationAdmin)