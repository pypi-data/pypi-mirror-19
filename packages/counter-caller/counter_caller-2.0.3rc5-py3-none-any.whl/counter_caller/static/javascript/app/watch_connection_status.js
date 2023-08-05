define(function(requre, exports, module) {
  return function(socket) {
    $(document).ready(function() {
      $body = $('body');

      socket.on('disconnect', function() { $body.removeClass('connected') });
      socket.on('connect', function() { $body.addClass('connected') });
    });
  }
});
