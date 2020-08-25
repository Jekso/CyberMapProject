from django.urls import path
from api import views

urlpatterns = [
    path('start-scan/', views.StartScanView.as_view(), name='start-scan'),
    path('get-results/', views.GetResultsView.as_view(), name='get-results'),
]