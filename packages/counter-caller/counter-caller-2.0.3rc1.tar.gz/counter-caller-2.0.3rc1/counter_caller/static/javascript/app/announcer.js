define(function(require, exports, module) {
  machina = require('machina');
  howler  = require('howler');
  SoundManager = require('app/sound_manager');

  var queue = [],
      currentTargets = [],
      mode = null,
      progress = 0,
      lastTriggerId = null;

  return machina.Fsm.extend({
    initialize: function() {
      this.sound_manager = new SoundManager();
    },

    initialState: 'idle',
    states: {
      idle: {
        _onEnter: function() {
          setTimeout(function() {
            this.handle('check');
          }.bind(this), 50);

          mode = null;
          progress = 0;
        },

        check: 'checking'
      },

      checking: {
        _onEnter: function() {
          transition = (queue.length > 0) ? 'waiting' : 'idle';
          this.transition(transition);
        }
      },

      waiting: {
        _onEnter: function() {
          setTimeout(function() {
            this.handle('timeout');
          }.bind(this), 200);
        },

        timeout: function() {
          if (queue.length > 0) {
            this.doTakeAll();
            mode = (currentTargets.length > 1) ? 'multiple' : 'singular';
            this.callback('speaking');
            this.transition('preambling');
          } else {
            this.transition('idle');
          }
        }
      },

      preambling: {
        _onEnter: function() {
          filename = (mode === 'multiple') ? 'positions' : 'position';
          this.callback('announcing', currentTargets.slice(0));
          this.play(filename);
        },
        finished: 'announcing'
      },

      announcing: {
        _onEnter: function() {
          triggerId = currentTargets.shift();
          if (currentTargets.length === 0) lastTriggerId = null;
          progress += 1;
          this.play(triggerId);
        },

        finished: function() {
          if (queue.length > 0) {
            this.doTakeAll();
            transition = 'joining';
          } else {
            transition = (currentTargets.length > 0) ? 'joining' : 'afterwording'
          }

          this.transition(transition);
        }
      },

      joining: {
        _onEnter: function() {
          filename = (mode === 'multiple') ? 'and' : 'and-position';
          this.callback('announcing', currentTargets.slice(0));
          this.play(filename);
        },
        finished: 'announcing'
      },

      afterwording: {
        _onEnter: function() {
          this.play('please');
        },
        finished: 'finished'
      },

      finished: {
        _onEnter: function() {
          this.transition('idle');
          this.callback('finishing');
        }
      }
    },

    queue: function(triggerId) {
      if (triggerId === lastTriggerId) return;

      queue.push(triggerId);
      lastTriggerId = triggerId;
    },

    check: function() {
      this.handle('check');
    },

    play: function(filename) {
      stateName = String("            " + this.state).slice(-12);
      console.debug(stateName + ": " + filename);

      this.sound_manager.playTrigger(filename, function() { this.handle('finished'); }.bind(this));
    },

    doTakeAll: function() {
      // Take everything in the queue and move it to currentTargets
      while (queue.length) currentTargets.push(queue.shift());
    },

    getQueue: function() {
      return queue;
    },

    getCurrentTargets: function() {
      return currentTargets;
    },

    emptyQueue: function() {
      // Empty the queue, and remove the correct number of current targets that
      // makes grammatical sense.
      queue = [];

      keep = (mode === 'multiple') ? 2 : 1;

      // If we're announcing multiple items, but have already announced more than one,
      // we only need to announce one more, instead of two.
      if (mode === 'multiple' && progress >= 1)
        keep = 1;

      if (currentTargets.length) {
        console.info('Removing all but ' + keep + ' (of ' + currentTargets.length + ') item(s) from the queue.')
        currentTargets = currentTargets.slice(0, keep);
      } else {
        console.info('Request to empty the queue, but no items left.');
      }
    },

    getMode: function() {
      return mode;
    },

    setCallback: function(callback) {
      this.callback = callback;
    }
  });
});
