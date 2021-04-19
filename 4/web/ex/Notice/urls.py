from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'releaseNotice$', views.releaseNoticeView.as_view()),
    url(r'noticeLists$', views.noticeListsView.as_view()),
    url(r'deleteNotice$', views.deleteNoticeView.as_view()),
    url(r'topNotice$', views.topNoticeView.as_view()),
    url(r'noTopNotice$', views.noTopNoticeView.as_view()),
    url(r'editNotice$', views.editNoticeView.as_view()),
    url(r'stuNoticeLists$', views.stuNoticeListsView.as_view()),
]
