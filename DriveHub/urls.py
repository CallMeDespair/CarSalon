from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from DriveHub import settings




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls', namespace='main')),
    path('catalog/', include('cars.urls', namespace='catalog')),
    path('user/', include('users.urls', namespace='user')),
    path('cart/', include('carts.urls', namespace='carts')),
    path('deals/', include('deals.urls', namespace='deals')),
    path('chatbot/', include('chatbotapp.urls', namespace='chatbot')),
]

if settings.DEBUG:
    urlpatterns += [
        path("__degug__/", include("debug_toolbar.urls")),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root =settings.MEDIA_ROOT)
