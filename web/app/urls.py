from django.urls import path, include
from app import views

urlpatterns = [
    path('', views.ridrectHome),
    path('doWork', views.doWork_view),
    path('allWorks', views.allWorks_view),
    path('staff/<int:id>', views.staff_view),
    path('work/<int:id>', views.singleWork_view),
    path('work/delete', views.deleteWork),
    path('submit', views.submit),
    path('finish/<int:id>', views.finish),
    path('stop/<int:id>', views.stop),
    path('continue/<int:id>', views.con),
    path('statistics/', include('app.statistics.urls'))
]