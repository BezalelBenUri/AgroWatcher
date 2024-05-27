from rest_framework.routers import DefaultRouter

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from .views import farmViewSet

router = DefaultRouter()

router.register(
    prefix = "api/v1/farms",
    viewset = farmViewSet,
    basename = "farms"
)

urlpatterns = [
    path('', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.SATELLITE_IMAGES_URL, document_root=settings.SATELLITE_IMAGES_DIR)
    urlpatterns += static(settings.NDVI_IMAGES_URL, document_root=settings.NDVI_IMAGES_DIR)
    urlpatterns += static(settings.NDMI_IMAGES_URL, document_root=settings.NDMI_IMAGES_DIR)
    urlpatterns += static(settings.NDWI_IMAGES_URL, document_root=settings.NDWI_IMAGES_DIR)
    