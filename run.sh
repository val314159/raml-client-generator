#!/bin/bash

#echo Trying javascript...
#./bin/raml-client.js -l javascript -o igjs -e data/instagram-api.raml

#echo Trying python...
#./bin/raml-client.js -l python     -o igpy -e data/instagram-api.raml

echo 'Trying python (box-api.raml)...'
python -mramyam node_modules/raml-parser/box-api.raml >box.py

echo 'Trying python (instagram-api.raml)...'
python -mramyam data/instagram-api.raml >instagram.py

echo 'Trying python (twilio-rest-api.raml)...'
python -mramyam data/twilio-rest-api.raml >twilio.py

echo Complete.
