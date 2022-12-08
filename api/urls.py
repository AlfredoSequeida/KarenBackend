from django.urls import path
from .views import KarenView

urlpatterns = [
    path("karen/", KarenView.as_view(), name="karen"),
]
