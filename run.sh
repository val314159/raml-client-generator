#!/bin/bash

echo Trying javascript...

./bin/raml-client.js -l javascript -o igjs -e data/instagram-api.raml 

echo Trying python...

./bin/raml-client.js -l python     -o igpy -e data/instagram-api.raml 

echo Complete.
