define(function(requre, exports, module) {
  $ = require('jquery');
  Vue = require('vue');
  mousetrap = require('mousetrap');

  Vue.config.delimiters = ['[[', ']]'];

  var ButtonFactory = function(element, triggers, callback) {
    this.initialize(element, triggers, callback);
  }

  ButtonFactory.prototype = {
    callback: null,

    initialize: function(element, triggers, callback) {
      console.info('Creating buttons and connecting shortcuts for ' + triggers.length + ' triggers.');

      this.callback = callback;
      this.connectShortcuts(triggers);
      this.connectButtons(element);

      this.vue = new Vue({
        el: element[0],
        data: { triggers: triggers }
      });
    },

    connectShortcuts: function(triggers) {
      var callback = this.callback;

      triggers.forEach(function(trigger) {
        Mousetrap.bind(trigger.shortcut, function(event) {
          callback(trigger.id);

          console.debug('Trigger ' + trigger.id + ' fired (key: ' + event.key + ')');

          return false;
        })
      });
    },

    connectButtons: function(element) {
      var callback = this.callback;


      $(element).on('click', 'button', function(event) {
        id = event.currentTarget.dataset.triggerId;
        callback(id);

        console.debug('Trigger ' + id + ' fired (button)');
      });
    }

  };

  return ButtonFactory;
})
