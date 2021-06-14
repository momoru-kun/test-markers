from django.urls import path
from .views import PictureView


urlpatterns = [
    path('', PictureView.as_view())
]
