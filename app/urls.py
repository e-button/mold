from django.urls import path
from app import views

urlpatterns = [
    path('doWork', views.doWork_view),
    path('allWorks', views.allWorks_view),
    path('staff/<int:id>', views.staff_view),
    path('work/<int:id>', views.singleWork_view),
    path('submit', views.submit),
    path('finish/<int:id>', views.finish),
]