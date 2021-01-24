"""mining_monitor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import include, path
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', include('monitor.urls'), name='home'),
    path('admin/', admin.site.urls),    
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('add-device/', include('monitor.urls'), name='add device'),
    path('my-devices/', include('monitor.urls'), name='my devices'),
    path('devices/', include('monitor.urls'), name='my devices'),
    path('add-transaction/', include('monitor.urls'), name='add transaction'),
    path('maintenance/', include('monitor.urls'), name='maintenance'),
    path('manage-devices/', include('monitor.urls'), name='manage devices'),
    path('work-archive/', include('monitor.urls'), name='work archive'),
    path('archive-devices/', include('monitor.urls'), name='archive devices'),
    path('payback/', include('monitor.urls'), name='payback'),
    path('transactions/', include('monitor.urls'), name='transactions'),
]
