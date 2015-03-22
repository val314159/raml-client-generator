fullPath = require('fullPath')

module.exports = function (resource) {
    var uri = lalala(resource);
    uri=uri.replace(/\//g,'_');
    uri=uri.replace(/-/g,'_');
    uri=uri.replace(/{/g,'_');
    uri=uri.replace(/}/g,'_');
    return uri;
};
