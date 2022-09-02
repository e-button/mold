from django.urls import path
from app.statistics import views

urlpatterns = [
    path('<int:id>', views.statistic),
    path('', views.statistics),
    path('generate', views.generate),
    path('download', views.file_view),
    path('delete', views.delete)
]