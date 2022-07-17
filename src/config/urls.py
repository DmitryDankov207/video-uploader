"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from ninja import NinjaAPI

from common.ninja.parser import ORJSONParser
from common.ninja.renderers import ORJSONRenderer
from common.ninja.security import ApiKey
from main import views

api = NinjaAPI(
    auth=ApiKey(),
    csrf=False,
    parser=ORJSONParser(),
    renderer=ORJSONRenderer(),
)

api.add_router('/videos/', views.video_router)
api.add_router('/', views.main_router)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
]
