#!/bin/bash

#echo Trying javascript...
#./bin/raml-client.js -l javascript -o igjs -e data/instagram-api.raml

#echo Trying python...
#./bin/raml-client.js -l python     -o igpy -e data/instagram-api.raml

if [ -d .v ]; then
  echo exists
else
  echo not exist.  adding.
  virtualenv .v
fi

source .v/bin/activate
pip install -r requirements.txt

echo 'Trying python (bitly-api.raml)...'
python -mramyam.gen_client -y data/bitly-api.raml >bitly_api.py
python -mramyam.gen_server -y data/bitly-api.raml >bitly_svr.py

echo 'Trying python (box-api.raml)...'
python -mramyam.gen_client -y data/box-api.raml >box_api.py
python -mramyam.gen_server -y data/box-api.raml >box_svr.py

echo 'Trying python (instagram-api.raml)...'
python -mramyam.gen_client -y data/instagram-api.raml >instagram_api.py
python -mramyam.gen_server -y data/instagram-api.raml >instagram_svr.py

echo 'Trying python (twilio-rest-api.raml)...'
python -mramyam.gen_client -y data/twilio-rest-api.raml >twilio_api.py
python -mramyam.gen_server -y data/twilio-rest-api.raml >twilio_svr.py

echo 'Trying python (github-api-v3.raml)...'
python -mramyam.gen_client -y data/github-api-v3.raml >github_api.py
python -mramyam.gen_server -y data/github-api-v3.raml >gibhub_svr.py

echo 'Trying python (stripe-api.raml)...'
python -mramyam.gen_client -y data/stripe-api.raml >stripe_api.py
python -mramyam.gen_server -y data/stripe-api.raml >stripe_svr.py

echo 'Trying python (twitter-rest-api.raml)...'
python -mramyam.gen_client -y data/twitter-rest-api.raml >twitter_rest_api.py
python -mramyam.gen_server -y data/twitter-rest-api.raml >twitter_rest_svr.py

echo 'Trying python (twitter-api.raml)...'
python -mramyam.gen_client -y data/twitter.raml >twitter_api.py
python -mramyam.gen_server -y data/twitter.raml >twitter_svr.py

echo Complete.
