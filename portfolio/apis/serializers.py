from rest_framework import serializers
from common.models import Portfolio
from common.models import Investment
from common.models import InvestmentPrice
from common.models import Account


class PortfolioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Portfolio
        fields = ['id', 'name', 'notes', 'created_date', 'updated_date',
        ]

class InvestmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Investment
        fields = ['id', 'name', 'symbol', 'symbol_type', 'asset_class', 'notes', 'created_date', 'updated_date',
        ]

class InvestmentPriceSerializers(serializers.ModelSerializer):

	class Meta:
		model = InvestmentPrice
		fields = ['id', 'investment', 'price', 'price_date', 'created_date', 'updated_date',
		]

class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['id', 'name', 'account_number', 'account_type', 'intial_balance', 'closed', 'notes', 'created_date', 'updated_date',
        ]

