define(function(require, exports, module) {
  machina = require('machina');
  $ = require('jquery');
  Vue = require('vue');

  Vue.config.delimiters = ['[[', ']]'];

  return machina.Fsm.extend({
    initialize: function(element, config) {
      this.triggers = config.triggers;
      this.vue = new Vue({
        el: element[0],
        data: { recents: [], current: null, idle: true, connected: false, please_wait: config.please_wait },
      });
    },

    initialState: 'idle',

    states: {
      idle: {
        _onEnter: function() {
          console.info('Switching to idle state.');

          // TODO: This is a little nasty as it messes with the state of the DOM globally.
          // It would be better to move #display into the Vue template known to this FSM,
          // and add/remove the class inside the Vue.js template.
          $('#display').removeClass('announcing');

          this.vue.idle = true;
          this.vue.current = null;
          this.vue.recents = [];
        },

        _onExit: function() {
          console.info('Leaving idle state.');

          $('#display').addClass('announcing');

          this.vue.idle = false;
        },

        speaking: 'displaying',
      },

      displaying: {
        announcing: 'updating',
        finishing: 'waiting'
      },

      updating: {
        _onEnter: function() {
          trigger = this.triggers[this.currentTriggerId];

          this.vue.current = trigger.label || trigger.id;
          this.vue.recents.push(this.currentTriggerId);

          this.transition('displaying');
        }
      },

      waiting: {
        _onEnter: function() {
          this.timer = setTimeout(function() {
            this.transition('idle');
          }.bind(this), 2500);
        },

        speaking: function() {
          clearTimeout(this.timer);
          this.transition('displaying');
        }
      }
    },

    update: function(messageType, extra) {
      if (messageType === 'announcing') this.currentTriggerId = extra[0];
      this.handle(messageType, extra);
    },

    connected: function(connected) {
      this.vue.connected = connected;
    },
  });
})
