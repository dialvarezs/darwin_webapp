from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import settings


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login', auth_views.login, name='name'),
    url(r'^transport/', include('transport.urls', namespace="transport")),
    url(r'^equipment_leasing/', include('equipment_leasing.urls', namespace="equipment_leasing")),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
