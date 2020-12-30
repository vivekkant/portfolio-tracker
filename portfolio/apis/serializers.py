from rest_framework import serializers
from common.models import Portfolio
from common.models import Investment
from common.models import InvestmentPrice
from common.models import Account
from common.models import Transaction
from apis.validators import validate_transaction
from copy import copy
from uuid import uuid4

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

class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ['id', 'transaction_id', 'transaction_date', 'transaction_type', 'reference_no', 
                  'account', 'counter_account' , 'investment', 'price', 'quantity',
                  'fee', 'debit', 'credit', 'notes', 'created_date', 'updated_date',
        ]

    def validate(self, data):
        return validate_transaction(self, data)

    def create(self, validated_data):

        validated_data["transaction_id"] = uuid4().hex
        instance = Transaction(**validated_data)
        instance.save()

        counter_validated_data = copy(validated_data)
        counter_validated_data["account"] = validated_data["counter_account"]
        counter_validated_data["counter_account"] = validated_data["account"]
        counter_validated_data["debit"] = validated_data["credit"]
        counter_validated_data["credit"] = validated_data["debit"]
        counter_instance = Transaction(**counter_validated_data)
        counter_instance.save()

        return instance

    def update(self, instance, validated_data):
        
        instance = self.update_instance(instance, validated_data)
        instance.save()

        counter_instance = Transaction.objects.filter(account=instance.counter_account, transaction_id=instance.transaction_id)[0];
        counter_validated_data = copy(validated_data)
        counter_validated_data["account"] = validated_data["counter_account"]
        counter_validated_data["counter_account"] = validated_data["account"]
        counter_validated_data["debit"] = validated_data["credit"]
        counter_validated_data["credit"] = validated_data["debit"]

        counter_instance = self.update_instance(counter_instance, counter_validated_data)
        counter_instance.save()  

        return instance

    def update_instance(self, instance, validated_data):

        instance.transaction_date   = validated_data.get('transaction_date', instance.transaction_date)
        instance.transaction_type   = validated_data.get('transaction_type', instance.transaction_type)
        instance.reference_no       = validated_data.get('reference_no', instance.reference_no)
        instance.account            = validated_data.get('account', instance.account)
        instance.counter_account    = validated_data.get('counter_account', instance.counter_account)
        instance.investment         = validated_data.get('investment', instance.investment)
        instance.price              = validated_data.get('price', instance.price)
        instance.quantity           = validated_data.get('quantity', instance.quantity)
        instance.fee                = validated_data.get('fee', instance.fee)
        instance.debit              = validated_data.get('debit', instance.debit)
        instance.credit             = validated_data.get('credit', instance.credit)
        instance.notes              = validated_data.get('notes', instance.notes)

        return instance






