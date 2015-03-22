var YAML = require('js-yaml');
var fs = require('fs');

/**
 * Import Yaml into the resource
 *
 * @param  {Object} resource
 * @return ""
 */
function importYaml(resource, filename, symbol) {
    var data = fs.readFileSync(filename,'ascii');
    data = YAML.load(data);
    resource[symbol] = data;
    this[symbol] = data;
    return '';
}
module.exports = importJson;
