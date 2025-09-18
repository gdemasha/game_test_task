from django.urls import path

from task_2.prize import views

app_name = 'prize'

urlpatterns = [
    path('<int:prize_id>/', views.user_prize),
]
