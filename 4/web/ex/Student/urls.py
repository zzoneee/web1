from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'people$', views.PeopleView.as_view()),
    # path('login/',views.login,name = "login"),
    url(r'auth$', views.LoginView.as_view()),
    url(r'editPwd$', views.EditPasswordView.as_view()),
    url(r'groupInfo$', views.GetGroupInfoView.as_view()),
    url(r'isStuHasGroup$', views.isStuHasGroupView.as_view()),
    url(r'groupListMsg$', views.groupListMsgView.as_view()),
    url(r'joinGroup$', views.joinGroupView.as_view()),
    url(r'groupNameExist$', views.groupNameExistView.as_view()),
    url(r'createGroup$', views.createGroupView.as_view()),
    url(r'addStuCheck$', views.addStuCheckView.as_view()),
    url(r'addGroupNumber$', views.addGroupNumberView.as_view()),
    url(r'editRole$', views.editRoleView.as_view()),
    url(r'quitTeam$', views.quitTeamView.as_view()),
    url(r'stuMsg$', views.stuMsgView.as_view()),
    url(r'editStuMsg$', views.editStuMsgView.as_view()),
    url(r'addLoginRecord$', views.addLoginRecordView.as_view()),
    url(r'getLoginNumber$', views.getLoginNumberView.as_view()),
    url(r'getGroupName$', views.getGroupNameView.as_view()),
    url(r'groupNameByStu_name$', views.groupNameByStu_nameView.as_view()),
    url(r'getGroupNumbersMsg$', views.getGroupNumbersMsgView.as_view()),
]
