from rest_framework import serializers

def null_validator(data, fields):
	for item in fields:
		if item in data:
			value = data[item]
			if (value != None):
				raise serializers.ValidationError("The field " + item + " should be null")

def not_null_validator(data, fields):
	for item in fields:
		if item in data:
			value = data[item]
			if (value == None or value < 0):
				raise serializers.ValidationError("The field " + item + " should be not null and positve")

def validate_transaction(serializer, data):

	if data["transaction_type"] == "INCOME":
		account = data["account"]
		if (account.account_type == "_INTERNAL"):
			raise serializers.ValidationError("Transactions can not be made on internal accounts")
		
		counter_account = data["counter_account"]
		if (counter_account.account_type != "_INTERNAL" or counter_account.id != 1):
			raise serializers.ValidationError("Counter account has to be CASHBOOK for INCOME Transaction Type")
		
		debit = data["debit"]
		if (debit != None and debit != 0.0):
			raise serializers.ValidationError("for INCOME debit amount should be null or zero")
		
		credit = data["credit"]
		if (credit == None or credit < 0.0):
			raise serializers.ValidationError("for INCOME credit amount should be zero or positive")
		
		null_fields = ["investment", "price", "quantity", "fee"]
		null_validator(data, null_fields)

		data["debit"] = 0.0
	
	elif data["transaction_type"] == "EXPENSE":
		account = data["account"]
		if (account.account_type == "_INTERNAL"):
			raise serializers.ValidationError("Transactions can not be made on internal accounts")
		
		counter_account = data["counter_account"]
		if (counter_account.account_type != "_INTERNAL" or counter_account.id != 1):
			raise serializers.ValidationError("Counter account has to be CASHBOOK for EXPENSE Transaction Type")
		
		debit = data["debit"]
		if (debit == None or debit < 0.0):
			raise serializers.ValidationError("for EXPENSE debit amount should be zero or positive")
		
		credit = data["credit"]
		if (credit != None and credit != 0.0):
			raise serializers.ValidationError("for EXPENSE credit amount should be null or zero")
		
		null_fields = ["investment", "price", "quantity", "fee"]
		null_validator(data, null_fields)

		data["credit"] = 0.0

	elif data["transaction_type"] == "TRANSFER":
		account = data["account"]
		if (account.account_type == "_INTERNAL"):
			raise serializers.ValidationError("Transfer transactions can not be made on internal accounts")
		
		counter_account = data["counter_account"]
		if (counter_account.account_type == "_INTERNAL"):
			raise serializers.ValidationError("Trasfer transactions can not be made on internal accounts")

		if account == counter_account:
			raise serializers.ValidationError("Transfer transaction can not be to same account")

		debit = data.get("debit", 0.0) if data.get("debit", 0.0) is not None else 0.0
		credit = data.get("credit", 0.0) if data.get("credit", 0.0) is not None else 0.0
		if (debit > 0 and credit > 0):
			raise serializers.ValidationError("Trasfer transactions can either have debit or credit")
		
		null_fields = ["investment", "price", "quantity", "fee"]
		null_validator(data, null_fields)

		data["debit"] = debit
		data["credit"] = credit

	elif data["transaction_type"] == "BUY":
		account = data["account"]
		if (account.account_type != "INVEST"):
			raise serializers.ValidationError("Asset buy can only be done on Investment Accounts")
		
		counter_account = data["counter_account"]
		if (counter_account.account_type != "_INTERNAL" or counter_account.id != 2):
			raise serializers.ValidationError("Counter account has to be ASSETBOOK for BUY Transaction Type")

		investment = data["investment"]
		if (investment is None):
			raise serializers.ValidationError("Investment is mandatory for BUY Transaction Type")
		
		not_null_fields = ["price", "quantity", "fee"]
		not_null_validator(data, not_null_fields)

		debit = (data["price"] * data["quantity"]) + data["fee"]
		data["debit"] = debit
		data["credit"] = 0

	elif data["transaction_type"] == "SELL":
		account = data["account"]
		if (account.account_type != "INVEST"):
			raise serializers.ValidationError("Asset buy can only be done on Investment Accounts")
		
		counter_account = data["counter_account"]
		if (counter_account.account_type != "_INTERNAL" or counter_account.id != 2):
			raise serializers.ValidationError("Counter account has to be ASSETBOOK for BUY Transaction Type")

		investment = data["investment"]
		if (investment is None):
			raise serializers.ValidationError("Investment is mandatory for BUY Transaction Type")
		
		not_null_fields = ["price", "quantity", "fee"]
		not_null_validator(data, not_null_fields)

		credit = (data["price"] * data["quantity"]) - data["fee"]
		data["credit"] = credit
		data["debit"] = 0

	else:
		raise serializers.ValidationError("Invalid transaction type")

	return data

