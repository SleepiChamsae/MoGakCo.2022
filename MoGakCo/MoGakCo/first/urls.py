from django.urls import path
from . import views


urlpatterns = [
    path('', views.waiting.as_view()),
    path('RankingInput/', views.RankingInput.as_view(), name="RankingInput"),
    path('RankingList/', views.RankingList.as_view())
]
