from rest_framework.routers import DefaultRouter

from .views import farmViewSet

router = DefaultRouter()

router.register(
    prefix = "api/v1/farms",
    viewset = farmViewSet,
    basename = "farms"
)

urlpatterns = router.urls