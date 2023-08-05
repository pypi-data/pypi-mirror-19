requirejs([
  'socketio',
  'jquery',
  'app/button_factory',
  'app/config_loader',
  'app/watch_connection_status',
  'app/post_click_manager'
], function(
  io,
  $,
  ButtonFactory,
  load_config,
  watch_connection_status,
  post_click_manager
) {
  $(document).ready(function() {
    load_config('/config.json').then(function(config) {
      var socket = io.connect();

      var buttons = new ButtonFactory($('#buttons'), config.triggers, function(id) {
        socket.emit('queue', id);
      });

      socket.on('queue', function(trigger_id) {
        console.debug('Trigger ' + trigger_id + ' received (network)');
        $element = $('[data-trigger-id="' + trigger_id + '"]');

        // When any client queues a trigger, simulate a button press.
        // TODO: This isn't exactly efficient...
        $element.addClass('active');
        setTimeout(function() { $('.active[data-trigger-id]').removeClass('active'); }, 10);
      });

      post_click_manager();
      watch_connection_status(socket);
    });
  })
});
