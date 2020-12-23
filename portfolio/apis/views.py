from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets
from common.models import Portfolio
from common.models import Investment
from common.models import Account
from common.models import InvestmentPrice
from apis.serializers import PortfolioSerializer
from apis.serializers import InvestmentSerializer
from apis.serializers import InvestmentPriceSerializers
from apis.serializers import AccountSerializer

# Create your views here.
class PortfolioViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, update` and `destroy` actions.
    """
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer

class InvestmentViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, update` and `destroy` actions.
    """
    queryset = Investment.objects.all()
    serializer_class = InvestmentSerializer


class InvestmentPriceViewSet(viewsets.ModelViewSet):
	"""
	This viewset automatically provides `list`, `create`, `retrieve`, update` and `destroy` actions.
	"""
	serializer_class = InvestmentPriceSerializers

	def get_queryset(self):
		queryset = InvestmentPrice.objects.filter(investment=self.kwargs['investments_pk'])
		return queryset

class AccountViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, update` and `destroy` actions.
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    