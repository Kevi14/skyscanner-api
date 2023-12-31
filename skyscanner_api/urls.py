"""
URL configuration for skyscanner_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from config import API_MOUNT_PATH
from sky_scanner.urls import router as sky_rotuer  # Replace 'your_app_name' with the name of the app containing your viewsets.

urlpatterns = [
    path('admin/', admin.site.urls),
    path(f'{API_MOUNT_PATH}/auth/', include("custom_auth.urls")),
    path(f'{API_MOUNT_PATH}/', include(sky_rotuer.urls)),  # Include the router URLs from your viewsets here.
]
