[![npm-image]][npm-url]
[![ramyam-awesome]][xxx-url]

Template-driven generator of clients for APIs described by RAML.

## Installation

For ramyam, just type the following:

```sh
source run.sh
```

or, if you like to do all the steps:

```sh
virtualenv .v
source .v/bin/activate
pip install -r requirements.txt
```

## Usage

For ramyam, just type the following:

```sh
source run.sh
```

or, initialize your environment thusly:

```sh
source .v/bin/activate
```

then (using *raml/yaml* file):

```sh
# generate client code
python -mramyam.gen_client -y [datafile.raml] >datafile_api.py
# generate server code
python -mramyam.gen_server -y [datafile.raml] >datafile_svr.py
```

or (using *json/javascript* file):

```sh
# generate client code
python -mramyam.gen_client -js [datafile.js] >datafile_api.py
# generate server code
python -mramyam.gen_server -js [datafile.js] >datafile_svr.py
```

To run the webserver ([gevent](http://gevent.org) based):

```sh
python -mramyam.wsgi_svr # runs both HTTP/HTTPS
```

## Supported Languages

* [Python](languages/python) (`python`)
  * Client code using [requests](http://python-requests.org)
  * Server code using [WSGI](http://wsgi.readthedocs.org)
  * High performance gevent WSGI server
  * SSL (HTTPS) Support
  * <s>OAuth 1.0 Support (looking at you, twitter)</s>
  * <s>OAuth 2.0 Support</s>

We're excited to see new languages soon! If you have a language you'd like to implement, check out the [implementation guide](IMPLEMENTATION.md).

## Testing

For ramyam, type the following:

```sh
sh run.sh
```

### Results:

- ![](https://img.shields.io/badge/bitly--api.raml-compiles-lightgrey.svg)
- ![](https://img.shields.io/badge/box--api.raml-compiles-lightgrey.svg)
- ![](https://img.shields.io/badge/instagram--api.raml-compiles-lightgrey.svg)
- ![](https://img.shields.io/badge/twilio--rest--api.raml-compiles-lightgrey.svg)
- ![](https://img.shields.io/badge/github--api--v3.raml-compiles-lightgrey.svg)
- ![](https://img.shields.io/badge/stripe--api.raml-compiles-lightgrey.svg)
- ![](https://img.shields.io/badge/twitter--rest--api.raml-compiles-lightgrey.svg)
- ![](https://img.shields.io/badge/twitter--api.raml-compiles-lightgrey.svg)


## License

Apache 2.0

[ramyam-awesome]: https://img.shields.io/badge/ramyam-awesome-brightgreen.svg
[npm-image]: https://img.shields.io/badge/version-0.11-orange.svg?style=flat
[npm-url]: https://npmjs.org/package/raml-client-generator
[xxx-url]: https://github.com/val314159/raml-client-generator
[downloads-image]: https://img.shields.io/npm/dm/raml-client-generator.svg?style=flat
[downloads-url]: https://npmjs.org/package/raml-client-generator
[travis-image]: https://img.shields.io/travis/mulesoft/raml-client-generator.svg?style=flat
[travis-url]: https://travis-ci.org/mulesoft/raml-client-generator
