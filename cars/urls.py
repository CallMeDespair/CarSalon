from django.urls import path
from cars import views


app_name = 'cars'

urlpatterns = [
    path('search/', views.CatalogView.as_view(), name='search'),
    path('<slug:category_slug>/', views.CatalogView.as_view(), name='index'),
    path('product/<slug:product_slug>/', views.ProductView.as_view(), name='product'),

    path('admin/car/add/', views.CarCreateView.as_view(), name='car_add'),
    path('admin/car/<slug:product_slug>/edit/', views.CarUpdateView.as_view(), name='car_edit'),
    path('admin/car/<slug:product_slug>/delete/', views.CarDeleteView.as_view(), name='car_delete'),
]
