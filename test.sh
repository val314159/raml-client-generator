echo 'Trying python (instagram-api.raml)...'
#python -mramyam.gs -y data/instagram-api.raml -intermediate >outf/instagram-api.json
#python -mramyam.gs -y data/instagram-api.raml

export INDIR=data

python -mramyam.gs -y instagram-api.raml

#echo 'Trying python (bitly-api.raml)...'
#python -mramyam.gs -y data/bitly-api.raml -intermediate >outf/bitly-api.json
#python -mramyam.gs -y data/bitly-api.raml
