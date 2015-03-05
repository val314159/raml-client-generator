#!/bin/bash

#echo Trying javascript...
#./bin/raml-client.js -l javascript -o igjs -e data/instagram-api.raml

#echo Trying python...
#./bin/raml-client.js -l python     -o igpy -e data/instagram-api.raml

if [ "$3" == "-noinstall" ]; then
  echo no install
else
  if [ -d .v ]; then
    echo exists
  else
    echo not exist.  adding.
    virtualenv .v
  fi

  source .v/bin/activate
  pip install -r requirements.txt
fi

source .v/bin/activate

export INDIR=data
mkdir -p gen/languages/js

all=
if [ "$1" == "" ]; then
  all=yes
fi
if [ "$1" == "all" ]; then
  all=yes
fi

if [ "$2" == "ig" ]; then
  echo 'Trying python (instagram-api.raml)...'
  #python -mramyam.gs -y instagram-api.raml -intermediate >gen/languages/js/instagram-api.json
  echo ...
  python -mramyam.gs -y instagram-api.raml
  #python -mramyam.gen_server -y data/instagram-api.raml >instagram_svr.py
fi

if [ "$1" == "twilio" ]; then
  echo 'Trying python (twilio-rest-api.raml)...'
  python -mramyam.gs -y twilio-rest-api.raml -intermediate >gen/languages/js/twilio.json
  echo ...
  python -mramyam.gs -y twilio-rest-api.raml
  #python -mramyam.gen_server -y data/twilio-rest-api.raml >twilio_svr.py
fi

if [ "$all" == "yes" ]; then
  echo 'Trying python (bitly-api.raml)...'
  python -mramyam.gs -y bitly-api.raml -intermediate >gen/languages/js/bitly-api.json
  echo ...
  python -mramyam.gs -y bitly-api.raml
  #python -mramyam.gen_server -y data/bitly-api.raml >bitly_svr.py

  echo 'Trying python (box-api.raml)...'
  python -mramyam.gs -y box-api.raml -intermediate >gen/languages/js/box-api.json
  echo ...
  python -mramyam.gs -y box-api.raml
  #python -mramyam.gen_server -y data/box-api.raml >box_svr.py

  echo 'Trying python (instagram-api.raml)...'
  python -mramyam.gs -y instagram-api.raml -intermediate >gen/languages/js/instagram-api.json
  echo ...
  python -mramyam.gs -y instagram-api.raml
  #python -mramyam.gen_server -y data/instagram-api.raml >instagram_svr.py

  echo 'Trying python (twilio-rest-api.raml)...'
  python -mramyam.gs -y twilio-rest-api.raml -intermediate >gen/languages/js/twilio.json
  echo ...
  python -mramyam.gs -y twilio-rest-api.raml
  #python -mramyam.gen_server -y data/twilio-rest-api.raml >twilio_svr.py

  echo 'Trying python (github-api-v3.raml)...'
  python -mramyam.gs -y github-api-v3.raml -intermediate >gen/languages/js/github-v3.json
  echo ...
  python -mramyam.gs -y github-api-v3.raml
  #python -mramyam.gen_server -y data/github-api-v3.raml >gibhub_svr.py

  echo 'Trying python (stripe-api.raml)...'
  python -mramyam.gs -y stripe-api.raml -intermediate >gen/languages/js/stripe-api.json
  echo ...
  python -mramyam.gs -y stripe-api.raml
  #python -mramyam.gen_server -y data/stripe-api.raml >stripe_svr.py

  echo 'Trying python (twitter-rest-api.raml)...'
  python -mramyam.gs -y twitter-rest-api.raml -intermediate >gen/languages/js/twitter-rest.json
  echo ...
  python -mramyam.gs -y twitter-rest-api.raml
  #python -mramyam.gen_server -y data/twitter-rest-api.raml >twitter_rest_svr.py

  echo 'Trying python (twitter-api.raml)...'
  python -mramyam.gs -y twitter.raml -intermediate >gen/languages/js/twitter.json
  echo ...
  python -mramyam.gs -y twitter.raml
  #python -mramyam.gen_server -y data/twitter.raml >twitter_svr.py

  echo Complete.
fi

if [ "$1" == "run" ]; then
  echo 'Running instagram server... (ports 9080 & 9443)'
  PORT_OFFSET=9000 python instagram_svr.py
fi
