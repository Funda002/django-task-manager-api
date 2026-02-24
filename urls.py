from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views # Import Django's built-in login views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tasks.urls')),
    
    # Add these built-in paths
    path('login/', auth_views.LoginView.as_view(template_name='tasks/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]