"""geoln_test_markers URL Configuration

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
from django.urls import path
from django.urls.conf import include
from django.views.generic import TemplateView

from markers.urls import urlpatterns as picture_urls
from comments.urls import urlpatterns as comment_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('picture/', include(picture_urls)),
    path('comment/', include(comment_urls)),
    path('', TemplateView.as_view(template_name="index.html")) 
]
