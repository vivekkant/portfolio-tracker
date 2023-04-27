from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework import views
from rest_framework import status
from common.models import Portfolio
from common.models import Investment
from common.models import Account
from common.models import InvestmentPrice
from common.models import Transaction
from common.models import AssetClass
from common.models import SymbolType
from common.models import AccountType
from common.models import TransactionType
from apis.serializers import PortfolioSerializer
from apis.serializers import InvestmentSerializer
from apis.serializers import InvestmentPriceSerializers
from apis.serializers import AccountSerializer
from apis.serializers import TransactionSerializer

# Create your views here.
class PortfolioViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, update` and `destroy` actions.
    """
    permission_classes = [IsAuthenticated]
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer

class InvestmentViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, update` and `destroy` actions.
    """
    permission_classes = [IsAuthenticated]
    queryset = Investment.objects.all()
    serializer_class = InvestmentSerializer


class InvestmentPriceViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, update` and `destroy` actions.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = InvestmentPriceSerializers

    def get_queryset(self):
        queryset = InvestmentPrice.objects.filter(investment=self.kwargs['investments_pk'])
        return queryset

class AccountViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, update` and `destroy` actions.
    """
    permission_classes = [IsAuthenticated]
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    """
    This viewset provides `list`, `create`, `retrieve`, update` and `destroy` actions.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer

    def get_queryset(self):
        queryset = Transaction.objects.filter(account=self.kwargs['accounts_pk'])

        return queryset

    def list(self, request, accounts_pk=None):
        queryset = self.get_queryset()
        serializer = TransactionSerializer(queryset, many=True)

        return Response(serializer.data)

    def retrieve(self, request, accounts_pk=None, pk=None):
        instance = self.get_object()
        serializer = TransactionSerializer(instance)

        return Response(serializer.data)

    def create(self, request, accounts_pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data)

    def update(self, request, pk=None, accounts_pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def destroy(self, request, pk=None, accounts_pk=None):
        instance = self.get_object()
        serializer = TransactionSerializer(instance)
        serializer.delete_instance()

        return Response(serializer.data)

class MetaData(views.APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):

        metadata_classes = [AssetClass, SymbolType, AccountType, TransactionType]
        metadata_dict = {}

        for clazz in metadata_classes:
            
            clazz_dict = {}
            
            for name, member in clazz.__members__.items():
                clazz_dict[member.value] = name
            
            metadata_dict[clazz.__name__] = clazz_dict

        return Response(metadata_dict)






    