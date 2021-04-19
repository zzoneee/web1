from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'reportList$', views.ReportListView.as_view()),
    url(r'hpReportList$', views.hp_reportListView.as_view()),
    url(r'hpReportMark$', views.hp_reportMarkView.as_view()),
    url(r'StuReportMsgLists$', views.StuReportMsgListsView.as_view()),
    url(r'createReport$', views.createReportView.as_view()),
]
