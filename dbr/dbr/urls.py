from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^dbr/', include('django_business_rules.urls')),
    url(r'^admin/', admin.site.urls),
]
