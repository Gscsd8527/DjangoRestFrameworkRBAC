from django.urls import path
from apps.cororateInfo import views

app_name = 'cororateInfo'

urlpatterns = [
    path('publish/', views.PublishInfoView.as_view()),
    path('infoview/', views.InfoView.as_view({'get': 'list'})),
    path('infoview/<pk>', views.InfoView.as_view({'get': 'retrieve'})),
]
