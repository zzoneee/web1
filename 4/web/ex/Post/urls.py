from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'postMsg$', views.postMsgView.as_view()),
    url(r'releasePost$', views.releasePostView.as_view()),
    url(r'deletePost$', views.deletePostView.as_view()),
    url(r'commentPost$', views.commentPostView.as_view()),
    url(r'commentMsg$', views.commentMsgView.as_view()),
    url(r'deleteComment$', views.deleteCommentView.as_view()),
    url(r'thumbsUp$', views.thumbsUpView.as_view()),
    url(r'thumbsDown$', views.thumbsDownView.as_view()),
    url(r'replyLists$', views.replyListsView.as_view()),
    url(r'replyPost$', views.replyPostView.as_view()),
    url(r'stuPostMsg$', views.stuPostMsgView.as_view()),
    url(r'stuReleasePost$', views.stuReleasePostView.as_view()),
    url(r'stuCommentPost$', views.stuCommentPostView.as_view()),
    url(r'stuThumbsUp$', views.stuThumbsUpView.as_view()),
    url(r'stuThumbsDown$', views.stuThumbsDownView.as_view()),
    url(r'stuReplyLists$', views.stuReplyListsView.as_view()),
    url(r'stuReplyPost$', views.stuReplyPostView.as_view()),
]
