from django.urls import path
from . import views

app_name = 'FARMAHOME'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='user_login'),
    path('subir_datos/', views.subir_datos, name='subir_datos'),
    path('entregar_pedido/', views.entregar_pedido, name='entregar_pedido'),
    path('ver_pedidos/<str:fecha>', views.ver_pedidos, name='ver_pedidos'),
    path('logout/', views.user_logout, name='user_logout'),

    path('entregar_pedido/<int:id>', views.entregar_pedido, name='editar_pedido'),

    path('exportar_excel/<str:fecha>', views.exportar_excel, name='exportar_excel'),
]