from django.urls import path

from deals import views

app_name = 'deals'

urlpatterns = [
    path('create-order/', views.CreateOrderView.as_view(), name='create_order'),
]