Current implementation of AMSC data movement API allows to transfer
datasets between globus end-points using globus access tokens. Having 
accounts on both globus end-points is currently prerequisite.

# AMSC data movement API

LBNL runs prototype implementation of AMSC data movement API server
at https://amsc-data-api.nersc.gov. There is swagger UI with RES APIs 
documenation https://amsc-data-api.nersc.gov/docs

# How to transfer data between FDP and Nersc globus end point using AMSC data movement API

First, one has to obtain account at Nersc. 

Then on the client machine / desktop:

* install python, e.g.:
  ```
  dnf install python3.13
  ```
* install `uv`
  ```
  pip install uv
  ```
* install a couple of modules
  ```
  uv pip install  typer
  uv pip install  globus_sdk
  ```
* download a handy client script that generates globus access token
  ```
  curl https://gist.githubusercontent.com/tylern4/924b19e58d75046e593e0db2d87f6c5c/raw/3e008fb6c0c9d21d429e5a779d2866c8f74e5072/generate_token.py \
     -o generate_token.py
  ```
* run the script like so:
  ```
  uv run generate_token.py login --mapped-collections <UUID1> --mapped-collections <UUID2> --domain nersc.gov
  ```
  Where UUIDs are UUIDs of globus source and collections. Specifically, using FDP and my account at Nersc:
  ```
  uv run generate_token.py login \
      --mapped-collections b35955d3-14d1-4aab-a1c9-189989f7d8d0 \
      --mapped-collections 9d6d994a-6d04-11e5-ba46-22000b92c6ec \
      --domain nersc.gov
  ```
  `b35955d3-14d1-4aab-a1c9-189989f7d8d0` is UUID of FDP globus collection and `9d6d994a-6d04-11e5-ba46-22000b92c6ec`
  is UUID of Nersc globus collection. Invocaton of the script will result in something like:
  ```
  Please authenticate with Globus here:
  -------------------------------------
  https://auth.globus.org/v2/oauth2/authorize?client_id=57554043-6dd8-410b-8ece-cd54e9c003bb&redirect_uri=https%3A%2F%2Fauth.globus.org... 
  -------------------------------------

  Enter the resulting Authorization Code here: 
  ```
  Cut&paste the URL into your browser and perform authentication. Eventually you will be redirected to a page with the secret. Cut&paste the secret into:
  ```
  Enter the resulting Authorization Code here:
  ```
  prompt. You will get your globus access token in return. You can use environmen
  variable, say GLOBUS_ACCESS_TOKEN, to store the access token.
  This globus access token can be used to initiate transfers.
  Example:
  ```
  export GLOBUS_ACCESS_TOKEN="Ag...." # (your globus access token)

  curl -X 'POST' \
  'https://amsc-data-api.nersc.gov/transfer/globus' \
  -H 'accept: application/json' \
  -H "Authorization: $GLOBUS_ACCESS_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{ \
  "source_url": "globus://b35955d3-14d1-4aab-a1c9-189989f7d8d0/amsc/cms/aoj/", \
  "destination_url": "globus://9d6d994a-6d04-11e5-ba46-22000b92c6ec/pscratch/sd/d/dimlit/", \
  "label": "Test transfer of AOJ dataset." \
  }'
  ```
  It should return json containing `transfer_uuid`:
  ```
  [
  {
    "name": "Test transfer of AOJ dataset.",
    "source_url": "globus://b35955d3-14d1-4aab-a1c9-189989f7d8d0/amsc/cms/aoj/",
    "destination_url": "globus://9d6d994a-6d04-11e5-ba46-22000b92c6ec/pscratch/sd/d/dimlit/",
    "transfer_uuid": "6ec65387-2322-11f1-927c-02ea150f82e1"
  }
  ]
  ```
  that can be used to query request status:
  ```
  curl  -s  -H "Authorization: $GLOBUS_ACCESS_TOKEN" \
   -H 'Content-Type: application/json' \
   "https://amsc-data-api.nersc.gov/transfer/globus/6ec65387-2322-11f1-927c-02ea150f82e1"
  ```
  which would return something like:
  ```
  {
    "transfer_uuid": "6ec65387-2322-11f1-927c-02ea150f82e1",
    "status": "SUCCEEDED",
    "completion_time": "2026-03-18T23:33:25Z",
    "destination_url": "globus://9d6d994a-6d04-11e5-ba46-22000b92c6ecNone",
    "reason": "",
    "bytes_transferred": 207292621489,
    "effective_bytes_per_second": 1150306465
  }
  ```
  
