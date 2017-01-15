from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.travel_list, name='index'),
    url(r'^travel/(?P<travel_id>[0-9]+)/save/$', views.travel_save, name='travel_save'),
    url(r'^travel/new/$', views.travel_save, name='travel_new'),
    url(r'^travel/pdf/$', views.travel_pdf, name='travel_pdf'),
    url(r'^group/(?P<group_id>[0-9]+)/save/$', views.group_save, name='group_save'),
]
