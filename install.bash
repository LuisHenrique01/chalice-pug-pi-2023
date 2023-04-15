python -m venv venv
source venv/bin/activate
pip install --upgrate pip
pip install chalice
pip install pymongo

export AWS_ACCESS_KEY_ID=my-super-id
export AWS_SECRET_ACCESS_KEY=my-super-key
export AWS_DEFAULT_REGION=us-west-2
export MONGO_URL=my-url

chalice new-project pelandoapi
cd pelandoapi

chalice local
Restarting local dev server.
Serving on http://127.0.0.1:8000

chalice deploy

Creating deployment package.
Reusing existing deployment package.
Updating policy for IAM role: pelandoapi-dev
Updating lambda function: pelandoapi-dev
Creating Rest API
Resources deployed:
  - Lambda ARN: arn:aws:lambda:us-west-2:276418894609:function:pelandoapi-dev
  - Rest API URL: https://87ilpizg4b.execute-api.us-west-2.amazonaws.com/sandbox/


chalice delete
Deleting Rest API: 87ilpizg4b
Deleting function: arn:aws:lambda:us-west-2:276418894609:function:pelandoapi-dev
Deleting IAM role: pelandoapi-dev