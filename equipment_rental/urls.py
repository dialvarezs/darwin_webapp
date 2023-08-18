from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^$", views.lease_list, name="index"),
    url(r"^lease/new/$", views.lease_save, name="lease_new"),
    url(r"^lease/(?P<lease_id>[0-9]+)/save/$", views.lease_save, name="lease_return"),
]
