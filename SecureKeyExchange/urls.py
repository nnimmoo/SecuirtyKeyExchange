from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from security.views import ChannelViewSet, SecretExchangeView, KeyGenerationView


router = DefaultRouter()
router.register(r'channels', ChannelViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/secret_exchange/<int:channel_id>/', SecretExchangeView.as_view(), name='secret-exchange'),
    path('api/key_generation/<int:channel_id>/', KeyGenerationView.as_view(), name='key-generation'),
]

