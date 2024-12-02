from django.urls import path

from .views import VRegistro,cerrar_sesion,logear

app_name="register"
urlpatterns = [
    path("",VRegistro.as_view(),name="register"),
    path("cerrar_sesion",cerrar_sesion,name="cerrar_sesion"),
    path("logear",logear,name="logear"),
]
