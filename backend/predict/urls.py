# urls.py 

from django.urls import path
from . import views


urlpatterns = [
    path("<str:params>/", views.predict)
]