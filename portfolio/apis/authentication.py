from rest_framework.authentication import TokenAuthentication


class PortfolioTokenAuthentication(TokenAuthentication):
	keyword = 'Bearer'