# core/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('post-job/', views.post_job, name='post_job'),
    path('jobs/', views.job_list, name='job_list'),
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    # urls.py
    path('employer/job/<int:job_id>/applications/', views.manage_applications, name='manage_applications'),


    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
