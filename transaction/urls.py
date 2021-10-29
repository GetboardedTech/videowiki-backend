from django.urls import path, include
from .views import BuyVideoView

urlpatterns = [
    path('oceanbuy', BuyVideoView.as_view()),
]