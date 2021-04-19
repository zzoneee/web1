from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'exLists$', views.exListsView.as_view()),
    url(r'addEx$', views.addExView.as_view()),
    url(r'deleteEx$', views.deleteExView.as_view()),
    url(r'getExName$', views.getExNameView.as_view()),
]
