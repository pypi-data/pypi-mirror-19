requirejs([
  'jquery',
  'socketio',
  'app/config_loader',
  'app/announcer',
  'app/screen',
  'app/watch_connection_status',
  'app/vue.extras'
],
function(
  $,
  io,
  load_config,
  Announcer,
  Screen,
  watch_connection_status
) {
  load_config('/config.json').then(function(config) {
    var triggers = [];
    config.triggers.forEach(function(trigger) {
      triggers[trigger.id] = trigger;
    });

    config.triggers = triggers;

    var socket = io.connect();

    var screen = new Screen($('#screen'), config);
    var announcer = new Announcer();

    announcer.setCallback(function(messageType, triggerId) {
      screen.update(messageType, triggerId);
    });

    socket.on('queue', function(triggerId) {
      announcer.queue(triggerId);
    });

    socket.on('refresh', function() {
      location.reload(true);
    });

    socket.on('clear', function() {
      announcer.emptyQueue();
    });

    watch_connection_status(socket);
  });
});
