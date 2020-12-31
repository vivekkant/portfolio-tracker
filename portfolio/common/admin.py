from django.contrib import admin

from common.models import Portfolio
from common.models import Investment
from common.models import Account
from common.models import InvestmentPrice
from common.models import Transaction

admin.site.register(Portfolio)
admin.site.register(Investment)
admin.site.register(Account)
admin.site.register(InvestmentPrice)
admin.site.register(Transaction)
