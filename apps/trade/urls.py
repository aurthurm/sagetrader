from django.urls import path, include
from .views import *

app_name = 'trade'
urlpatterns = [
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('mine/', TradeList.as_view(), name='my-trades'),
    path('<int:trade_id>/detail', TradeDetail.as_view(), name='trade-detail'),
]
