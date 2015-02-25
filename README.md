# RAML Client Generator

[![NPM version][npm-image]][npm-url]
[![NPM downloads][downloads-image]][downloads-url]
[![Build status][travis-image]][travis-url]

Template-driven generator of clients for APIs described by RAML.

## Installation

For ramyam, type the following:

```sh
virtualenv .v
source .v/bin/activate
```

First, make sure [node](http://nodejs.org) has been installed. Then, we can install it using `npm`:

```sh
npm install raml-client-generator -g
```

## Usage

For ramyam, type the following:

```sh
sh run.sh
```

To generate an API client, point the command to your base RAML file and specify the output directory and language.

```sh
raml-to-client api.raml -o api-client -l javascript
```

## Supported Languages

* [JavaScript](languages/javascript) (`javascript`)
  * Node and browser support
  * Promises
  * Complete OAuth 2.0 Support
  * Multiple instances
  * Automatic `README.md` and `package.json` generation
  * Multi-part form data

* [Python](languages/javascript) (`python`)
  * Client code using requests
  * Server code using WSGI
  * High performance gevent WSGI server
  * OAuth 2.0 Support **NO**

We're excited to see new languages soon! If you have a language you'd like to implement, check out the [implementation guide](IMPLEMENTATION.md).

## Testing

For ramyam, type the following:

```sh
sh run.sh
```

```sh
npm install
npm test # This *will* test every language.
```

## License

Apache 2.0

[npm-image]: https://img.shields.io/npm/v/raml-client-generator.svg?style=flat
[npm-url]: https://npmjs.org/package/raml-client-generator
[downloads-image]: https://img.shields.io/npm/dm/raml-client-generator.svg?style=flat
[downloads-url]: https://npmjs.org/package/raml-client-generator
[travis-image]: https://img.shields.io/travis/mulesoft/raml-client-generator.svg?style=flat
[travis-url]: https://travis-ci.org/mulesoft/raml-client-generator
