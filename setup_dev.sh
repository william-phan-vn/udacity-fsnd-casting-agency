#~/bin/bash

# Authentication
export AUTH0_DOMAIN='william.jp.auth0.com'
export CLIENT_ID='meB9SnRgCYGsJIQV97xClgq1lFfD7vOx'
export API_AUDIENCE='http://localhost:5000'
export REDIRECT_URI='http://localhost:5000'

# Database
export DATABASE_URL='postgresql://vietplh1:123@localhost:5432/udacity-casting-agency'

echo 'setup.sh script executed successfully!'
