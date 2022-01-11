from django.contrib import admin
from django.urls import path
from extrasences.urls import urlpatterns

urlpatterns += [
    path('admin/', admin.site.urls),
]