from django.urls import path, include
from .views import *

app_name = 'trade'
urlpatterns = [
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('statistics/member', Statistics.as_view(), name='member-statistics'),
    path('trading-plan/update/', UpdatePlan.as_view(), name='update-plan'),
    path('trading-portfolio/update/', UpdatePortfolio.as_view(), name='update-portfolio'),
    path('trading-portfolio/remove/', UpdatePortfolioRemove.as_view(), name='update-portfolio-remove'),
    path('mine/', TradeList.as_view(), name='my-trades'),
    path('strategies/mine/', StrategiesList.as_view(), name='my-strategies'),
    path('place/', PlaceTrade.as_view(), name='place-trade'),
    path('strategy/add/', StrategyCreate.as_view(), name='add-strategy'),
    path('<int:trade_id>/detail', TradeDetail.as_view(), name='trade-detail'),
    path('<int:trade_id>/followup', AddFollowUp.as_view(), name='trade-followup'),
    path('<int:trade_id>/charts/', AddChart.as_view(), name='add-chart'),
]

