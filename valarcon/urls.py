from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from . import settings

urlpatterns = [
    url(r"^admin/", include(admin.site.urls)),
    url(r"^login", auth_views.login, name="name"),
    url(r"^transport/", include("transport.urls", namespace="transport")),
]
