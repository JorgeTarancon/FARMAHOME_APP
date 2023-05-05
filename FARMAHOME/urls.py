from django.urls import path
from . import views

app_name = 'FARMAHOME'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='user_login'),
    path('subir_datos/', views.subir_datos, name='subir_datos'),
    path('entregar_pedido/', views.entregar_pedido, name='entregar_pedido'),
    path('ver_pedidos/', views.ver_pedidos, name='ver_pedidos'),
    path('ver_pedidos/entregar_pedido/<int:id>', views.entregar_pedido, name='editar_pedido'),
    path('ver_pedidos/exportar_excel/', views.exportar_excel, name='exportar_excel'),
    path('logout/', views.user_logout, name='user_logout'),
]