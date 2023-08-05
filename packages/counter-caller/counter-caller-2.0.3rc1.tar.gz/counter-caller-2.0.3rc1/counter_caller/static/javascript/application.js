requirejs.config({
  baseUrl: window.ASSET_BASE_URL,
  paths: {
    app: "../javascript/app",
    socketio: "socket.io-client/socket.io",
    jquery: "jquery/dist/jquery.min",
    howler: "howler.js/howler.min",
    machina: "machina/lib/machina.min",
    lodash: "lodash/lodash.min",
    vue: "vue/dist/vue.min",
    mousetrap: "mousetrap/mousetrap.min",
  }
});
