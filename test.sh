export INDIR=data
mkdir -p gen/languages/js

echo 'Trying python (instagram-api.raml)...'
python -mramyam.gs -y instagram-api.raml -intermediate >gen/languages/js/instagram-api.json
python -mramyam.gs -y instagram-api.raml

#echo 'Trying python (bitly-api.raml)...'
#python -mramyam.gs -y data/bitly-api.raml -intermediate >gen/languages/js/bitly-api.json
#python -mramyam.gs -y data/bitly-api.raml
