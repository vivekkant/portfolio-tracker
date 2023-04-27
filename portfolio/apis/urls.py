from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from rest_framework.authtoken.views import obtain_auth_token
from apis import views

router = DefaultRouter(trailing_slash=False)
router.register(r'portfolios', views.PortfolioViewSet)
router.register(r'investments', views.InvestmentViewSet)
router.register(r'accounts', views.AccountViewSet)

investments_router = routers.NestedSimpleRouter(router, r'investments', lookup='investments')
investments_router.register(r'prices', views.InvestmentPriceViewSet, basename='investments-prices')

accounts_router = routers.NestedSimpleRouter(router, r'accounts', lookup='accounts')
accounts_router.register(r'transactions', views.TransactionViewSet, basename='accounts-transactions')

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(investments_router.urls)),
    path(r'', include(accounts_router.urls)),
    path(r'metadata', views.MetaData().as_view()),
    path(r'authenticate', obtain_auth_token),
]
