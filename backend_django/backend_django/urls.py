from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from backend_django.api import views

router = DefaultRouter()
router.register(r"Stock", views.StockViewSet)
router.register(r"Historical", views.HistoricalViewSet)
router.register(r"BackTesting", views.BackTestingViewSet)
router.register(r"StrategySteps", views.StrategyStepsViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/docs/", SpectacularSwaggerView.as_view(url_name="schema")),
]
