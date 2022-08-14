import os

AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
ALGORITHMS = ['RS256']
CLIENT_ID = os.getenv('CLIENT_ID')
API_AUDIENCE = os.getenv('API_AUDIENCE')
REDIRECT_URI = os.getenv('REDIRECT_URI')

AUTH0_LOGIN_URL = f'''https://{AUTH0_DOMAIN}/authorize?audience={API_AUDIENCE}&response_type=token&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}'''
