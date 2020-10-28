from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='orders'),
    path('<int:order_id>', views.detail),
    path('cancel/<int:order_id>', views.cancel),
    path('update/<int:order_id>', views.update),
    path('messages/<int:order_id>', views.order_messages),
    path('create', views.create, name='create')
]
