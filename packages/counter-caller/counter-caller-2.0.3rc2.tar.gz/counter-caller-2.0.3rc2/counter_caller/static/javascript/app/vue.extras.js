define(function(require, exports, module) {
  var Vue = require('vue');

  Vue.filter('slice', function(value, start, end) {
    if (value == undefined) return;
    return (end == undefined) ? value.slice(start) : value.slice(start, end);
  });

  Vue.filter('reverse', function(value) {
    return value.reverse();
  });
});
