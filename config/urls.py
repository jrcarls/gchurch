from django.contrib import admin
from django.urls import include, path
from config.views import dashboard

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/", include("accounts.urls")),
    path("membros/", include("members.urls")),
    path("", dashboard, name="dashboard"),
]
