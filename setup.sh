#~/bin/bash

# Authentication
export AUTH0_DOMAIN='william.jp.auth0.com'
export CLIENT_ID='UhoeJD0USTjd1cpwEAA3sZr2GtagsjQQ'
export API_AUDIENCE='http://localhost:5000'
export REDIRECT_URI='https://william-casting-agency.herokuapp.com/'

# Database
export DATABASE_URL='postgres://octfpywkxydatf:6b0eb3c7da70ff5c73700f4e6add9fe2ffe5b78164f1329aab3215775ac3a255@ec2-44-193-178-122.compute-1.amazonaws.com:5432/ddlp23fcjqmms7'

echo 'setup.sh script executed successfully!'
