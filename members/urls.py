from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="members"),
    path("novo/", views.criar, name="members_criar"),
    path("<int:pk>/editar/", views.editar, name="members_editar"),
]
