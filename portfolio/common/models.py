from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import date

class AssetClass(models.TextChoices):
	STOCKS = 'STK', _('Stocks')
	MF_EQUITY = 'MFE', _('Mutual Fund - Equity')
	MF_DEBT = 'MFD', _('Mutual Fund - Debt')
	MF_LIQUID = 'MFL', _('Mutudl Fund - Liquid')
	COMMODITY = 'COM', _('Commodity')
	OTHERS = 'OTR', _('Others')

class SymbolType(models.TextChoices):
	YAHOO = 'YAHOO', _('Yahoo Finance')
	AMFI = 'AMFI', _('AMFI MF File')
	NONE = 'NONE', _('None')

class AccountType(models.TextChoices):
	BANK = 'BANK', _('Bank')
	CC = 'CC', _('Credit Card')
	CASH = 'CASH', _('Cash')
	ASSET = 'ASSET', _('Assets')
	LIBLTY = 'LIBLTY', _('Liability')
	INVEST = 'INVEST', _('Investment')
	_INTERNAL = '_INTERNAL', _('Internal Counter Party Accounts')

class TransactionType(models.TextChoices):
	INCOME = 'INCOME', _('Income')
	EXPENSE = 'EXPENSE', _('Expense')
	TRANSFER = 'TRANSFER', _('Transfer')
	BUY = 'BUY', _('Buy')
	SELL = 'SELL', _('Sell')

class Investment(models.Model):
	name = models.CharField(max_length=100, blank=True, default='')
	symbol = models.CharField(max_length=100, blank=True, default='')
	symbol_type = models.CharField(max_length=10, choices=SymbolType.choices, default=SymbolType.NONE)
	asset_class = models.CharField(max_length=10, choices=AssetClass.choices, default=AssetClass.OTHERS)
	notes = models.TextField(blank=True)
	created_date = models.DateTimeField(auto_now_add=True)
	updated_date = models.DateTimeField(auto_now=True)

class InvestmentPrice(models.Model):
	investment =  models.ForeignKey(Investment, on_delete=models.CASCADE, related_name='prices')
	price = models.DecimalField(max_digits=13, decimal_places=4, blank=False, default=0.0)
	price_date = models.DateField(default=date.today)
	created_date = models.DateTimeField(auto_now_add=True)
	updated_date = models.DateTimeField(auto_now=True)

class Portfolio(models.Model):
	name = models.CharField(max_length=100, blank=True, default='')
	notes = models.TextField(blank=True)
	created_date = models.DateTimeField(auto_now_add=True)
	updated_date = models.DateTimeField(auto_now=True)

class Account(models.Model):
	name = models.CharField(max_length=100, blank=True, default='')
	account_number = models.CharField(max_length=100, blank=True, default='')
	account_type = models.CharField(max_length=10, choices=AccountType.choices, default=AccountType.BANK)
	intial_balance = models.DecimalField(max_digits=13, decimal_places=4, blank=False, default=0.0)
	notes = models.TextField(blank=True)
	closed = models.BooleanField(default=False)
	created_date = models.DateTimeField(auto_now_add=True)
	updated_date = models.DateTimeField(auto_now=True)


class Transaction(models.Model):
	transaction_id = models.CharField(max_length=100, blank=False)
	transaction_date = models.DateField(default=date.today)
	transaction_type = models.CharField(max_length=10, choices=TransactionType.choices, default=TransactionType.EXPENSE)
	reference_no = models.CharField(max_length=100, blank=True, default='', null=True)
	account =  models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions_account')
	counter_account =  models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions_counter_account')
	investment =  models.ForeignKey(Investment, blank=True, on_delete=models.CASCADE, null=True)
	price = models.DecimalField(max_digits=13, decimal_places=4, blank=False, default=0.0, null=True)
	quantity = models.DecimalField(max_digits=13, decimal_places=4, blank=False, default=0.0, null=True)
	fee = models.DecimalField(max_digits=13, decimal_places=4, blank=False, default=0.0, null=True)
	payee = models.CharField(max_length=100, blank=True, default='', null=True)
	category = models.CharField(max_length=100, blank=True, default='', null=True)
	debit = models.DecimalField(max_digits=13, decimal_places=4, blank=False, default=0.0, null=True)
	credit = models.DecimalField(max_digits=13, decimal_places=4, blank=False, default=0.0, null=True)
	notes = models.TextField(blank=True, null=True)
	created_date = models.DateTimeField(auto_now_add=True)
	updated_date = models.DateTimeField(auto_now=True)

