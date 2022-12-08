from django.urls import path
from .views import index, docs

urlpatterns = [
    path("", index, name="karen_index"),
    path("docs/<str:version>", docs, name="karen_docs"),
]