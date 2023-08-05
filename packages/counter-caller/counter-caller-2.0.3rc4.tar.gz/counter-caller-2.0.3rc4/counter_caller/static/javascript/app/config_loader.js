define(function(require, exports, module) {
  $ = require('jquery');

  return function(config_path) {
    return $.ajax({
      url: config_path,
      dataType: 'json',
      success: function(config) { window.config = config; },
    });

  }
})
