from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'classesLists$', views.classesListsView.as_view()),
    url(r'classesInfo$', views.classesInfoView.as_view()),
    url(r'classesExist$', views.classesExistView.as_view()),
    url(r'addClass$', views.addClassView.as_view()),
    url(r'deleteClass$', views.deleteClassView.as_view()),
]
