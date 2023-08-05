define(function(require, exports, module) {
  howler = require('howler');

  var SoundManager = function() {
    this.preloadAllTriggers();
  }

  SoundManager.prototype = {
    builtInSounds: ['and-position', 'and', 'please', 'position', 'positions'],
    sounds: {},

    preloadAllTriggers: function() {
      var triggers = window.config.triggers.slice();
      var promises = [];

      this.builtInSounds.forEach(function(item) {
        triggers.push({ id: item})
      });

      triggers.forEach(function(trigger) {
        var def = $.Deferred();

        this.sounds[trigger.id] = trigger;
        this.sounds[trigger.id].howl = new Howl({
          urls: [
            "/static/" + trigger.id + ".mp3",
          ],
          onload: function() { def.resolve(); },
          onloaderror: function() { def.fail(); },
        });

        promises.push(def);
      }.bind(this));

      $.when.apply(undefined, promises).then(function() {
        console.info('All sounds have been loaded.');
      });
    },

    playTrigger: function(triggerId, callback) {
      var howl = this.sounds[triggerId].howl;

      howl.on('end', function(foo) {
        callback();
        howl.off('end');
      })

      howl.play();
    }
  };

  return SoundManager;
});
