from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.DashboardView.as_view(), name='dashboard'),
]
