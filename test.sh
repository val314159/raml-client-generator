echo ==============================================
rm -fr igpy
echo ==============================================
./bin/raml-client.js -l python -o igpy -e instagram-api.raml
echo ==============================================
. .venv/bin/activate
echo ==============================================
nosetests igpy/rpc_requests.py
echo ==============================================
