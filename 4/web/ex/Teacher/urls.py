from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'login$', views.LoginView.as_view()),
    url(r'classMessage$', views.ClassMessageView.as_view()),
    url(r'studentMessageReport$', views.studentMessageReportView.as_view()),
    url(r'teacherMessage$', views.teacherMessageView.as_view()),
    url(r'editTeacherMessage$', views.editTeacherMessageView.as_view()),
    url(r'editPwd$', views.editPwdView.as_view()),
    url(r'addTeacher$', views.addTeacherView.as_view()),
    url(r'teacherIDExist$', views.teacherIDExistView.as_view()),
    url(r'stuNumExist$', views.stuNumExistView.as_view()),
    url(r'getGroupList$', views.getGroupListView.as_view()),
    url(r'addStudent$', views.addStudentView.as_view()),
    url(r'updateStuMsg$', views.updateStuMsgView.as_view()),
    url(r'deleteStu$', views.deleteStuView.as_view()),
    url(r'resetPassword$', views.resetPasswordView.as_view()),
    url(r'groupNumberDetail$', views.groupNumberDetailView.as_view()),
    url(r'reportDetail$', views.reportDetailView.as_view()),
    url(r'teaReportMark$', views.teaReportMarkView.as_view()),
    url(r'getReportUrl$', views.getReportUrlView.as_view()),
    url(r'deleteReport$', views.deleteReportView.as_view()),
    url(r'importExcel$', views.importExcelView.as_view()),
    url(r'getGroupListDetail$', views.getGroupListDetailView.as_view())
]
