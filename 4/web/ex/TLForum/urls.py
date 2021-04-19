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
    url(r'votePostCommentMsg$', views.votePostCommentMsgView.as_view()),
    url(r'initiateVote$', views.initiateVoteView.as_view()),
    url(r'voteLists$', views.voteListsView.as_view()),
    url(r'myVoteLists$', views.myVoteListsView.as_view()),
    url(r'toVote$', views.toVoteView.as_view()),
    url(r'voteDetail$', views.voteDetailView.as_view()),
]
