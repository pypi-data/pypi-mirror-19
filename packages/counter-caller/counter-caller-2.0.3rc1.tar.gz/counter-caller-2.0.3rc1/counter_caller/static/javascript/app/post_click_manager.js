define(function(require, exports, module) {
  $ = require('jquery');

  return function() {
    $(document).on('click', '[data-post]', function(event) {
      $.post(event.target.dataset.post);

      event.preventDefault();
      return false;
    });
  };
});
