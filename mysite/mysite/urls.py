"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from users import views as user_views
from activities import views as activity_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$', activity_views.training_log_view, name='training_log'),
    path('Register/', user_views.register_view, name='register'),
    path('Login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('Logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('About/', activity_views.about_view, name='about'),
    path('Training-Log/', activity_views.training_log_view, name='training_log'),
    path('Create-Activity/', activity_views.create_activity_view, name='create_activity'),
    re_path(r'Edit-Activity/(?P<aid>\d+)/$', activity_views.edit_activity_view, name='edit_activity'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
