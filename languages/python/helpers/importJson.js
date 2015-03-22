var fs = require('fs');

/**
 * Import JSON into the resource
 *
 * @param  {Object} resource
 * @return ""
 */
function importJson(resource, filename, symbol) {
    var data = fs.readFileSync(filename,'ascii');
    data = JSON.parse(data);
    resource[symbol] = data;
    this[symbol] = data;
    return '';
}
module.exports = importJson;
