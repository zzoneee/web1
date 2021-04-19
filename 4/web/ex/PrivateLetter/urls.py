from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'getPrivateLetterLists$', views.getPrivateLetterListsView.as_view()),
    url(r'enterPrivateLetter$', views.enterPrivateLetterView.as_view()),
    url(r'getRecentContacts$', views.getRecentContactsView.as_view()),
    url(r'closeChatBox$', views.closeChatBoxView.as_view()),
    url(r'openChatBox$', views.openChatBoxView.as_view()),
    url(r'searchContact$', views.searchContactView.as_view()),
    url(r'stuGetPrivateLetterLists$', views.stuGetPrivateLetterListsView.as_view()),
    url(r'stuEnterPrivateLetter$', views.stuEnterPrivateLetterView.as_view()),
    url(r'stuRecentContacts$', views.stuRecentContactsView.as_view()),
    url(r'stuCloseChatBox$', views.stuCloseChatBoxView.as_view()),
    url(r'stuOpenChatBox$', views.stuOpenChatBoxView.as_view()),
    url(r'stuSearchContact$', views.stuSearchContactView.as_view()),
]
