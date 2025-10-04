from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Router para ViewSets (CRUD automático)
router = DefaultRouter()
router.register(r'reservas', views.ReservaViewSet)

app_name = 'reports'

urlpatterns = [
    # URLs del CRUD (automáticas del ViewSet)
    path('', include(router.urls)),
    
    # URLs de reportes
    path('excel/', views.ReporteExcelView.as_view(), name='reporte-excel'),
    path('pdf/', views.ReportePDFView.as_view(), name='reporte-pdf'),
]