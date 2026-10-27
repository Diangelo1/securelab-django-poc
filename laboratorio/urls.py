from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("sql-injection/", views.sql_injection, name="sql_injection"),
    path("xss/", views.xss_protegido, name="xss_protegido"),
    path("xss-vulneravel/", views.xss_vulneravel, name="xss_vulneravel"),
    path("csrf/", views.csrf_protegido, name="csrf_protegido"),
    path("csrf-vulneravel/", views.csrf_vulneravel, name="csrf_vulneravel"),
]
