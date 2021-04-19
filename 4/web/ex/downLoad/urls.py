from django.urls import path, re_path
from django.conf.urls import url
from . import views

urlpatterns = [
    re_path('report/(?P<id>.*)/', views.file_downView.as_view(), name = "downLoad"),
    re_path('uploadStuMsg/(?P<id>.*)/', views.uploadStuMsgView.as_view(), name = "uploadStuMsg")
]
