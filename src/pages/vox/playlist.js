// @license  magnet:?xt=urn:btih:0b31508aeb0634b347b8270c7bee4d411b5d4109&dn=agpl-3.0.txt AGPL-v3.0

// Loads an external JS file and append it to the head, from:
// http://zcourts.com/2011/10/06/dynamically-requireinclude-a-javascript-file-into-a-page-and-be-notified-when-its-loaded

/* eslint-disable */

function require(file, callback) {
  var head = document.getElementsByTagName("head")[0];
  var script = document.createElement("script");
  script.src = file;
  script.type = "text/javascript";
  // real browsers:
  script.onload = callback;
  // MSIE:
  script.onreadystatechange = function () {
    if (this.readyState === "complete") callback();
  };
  head.appendChild(script);
}

require("https://archive.org/includes/jquery-1.10.2.min.js", function () {
  var $ = jQuery; // allows us to use jQuery as $ w/o collision

  // encrapsulate all our functions and variables.  no globals!
  var Player = {
    playlist: [],
    starts: [],
    ends: [],
  };

  Player.setupPlaylist = function () {
    // Parse document as a text file, line by line.
    // Also remove any body logical borders/padding.
    var bod = $("body").css({ padding: 0, margin: 0, border: 0 }).html();
    if (navigator.userAgent.indexOf("IE") >= 0)
      bod = bod.replace(/(archive.org\/download\/\S+)/g, "$1\n"); // IE SUX
    var lines = bod.split("\n");

    for (var i = 0; i < lines.length; i++) {
      if (lines[i][0] === "#") continue;
      var mat = lines[i].match(/:\/\/archive.org\/download\/([^\/]+)/);
      if (!mat) continue;

      var id = mat[1];
      var url = lines[i].trim();

      var file = {
        file: url,
        image: "https://archive.org/services/img/" + id,
      };

      // mp4 uses serverside lossless cutting -- our 3 other formats dont have that, so use JS..
      // look for start and end first (2 variants); then just start (2 variants)
      var start = (url.match(/\.(mp3|ogg|ogv)\?t=([\d.]+)\/([\d.]+)/) ||
        url.match(/\.(mp3|ogg|ogv)\?start=([\d.]+)&end=([\d.]+)/) ||
        url.match(/\.(mp3|ogg|ogv)\?t=([\d.]+)/) ||
        url.match(/\.(mp3|ogg|ogv)\?start=([\d.]+)/) || [0, 0, 0])[2];

      // look for start and end first (2 variants); then just end (2 variants)
      var end = (url.match(/\.(mp3|ogg|ogv)\?t=[\d.]+\/([\d.]+)/) ||
        url.match(/\.(mp3|ogg|ogv)\?start=[\d.]+&end=([\d.]+)/) ||
        url.match(/\.(mp3|ogg|ogv)\?t=\/([\d.]+)/) ||
        url.match(/\.(mp3|ogg|ogv)\?end=([\d.]+)/) || [0, 0, 0])[2];

      if (start) file.starttime = parseFloat(start);

      Player.starts.push(start);
      Player.ends.push(end);

      Player.playlist.push(file);
    }
  };

  Player.addButtons = function (jwp) {
    // make a (upper left) button that shows IA logo, and links to source (archive.org)
    // of each audio/video file in playlist (updating as they play).
    jwp.addButton(
      "https://archive.org/images/glogo20x20.png",
      "this item, formats, and more at Internet Archive",
      function () {
        var url = "https://archive.org";
        var fi = jwp.getPlaylistItem()["file"]; // file currently playing
        var mat = fi.match(/\/download\/([^\/\?&]+)/);
        if (mat) url += "/details/" + mat[1];
        window.location.href = url;
      },
      "origin" //unique ID of this button
    );

    // add 'previous' and 'next' playlist buttons
    var prv =
      '<svg xmlns="http://www.w3.org/2000/svg" class="jw-svg-icon jw-svg-icon-next" style="transform: rotate(180deg)" viewBox="0 0 240 240"><path d="M165,60v53.3L59.2,42.8C56.9,41.3,55,42.3,55,45v150c0,2.7,1.9,3.8,4.2,2.2L165,126.6v53.3h20v-120L165,60L165,60z"></path></svg>';
    var nxt =
      '<svg xmlns="http://www.w3.org/2000/svg" class="jw-svg-icon jw-svg-icon-next" viewBox="0 0 240 240"><path d="M165,60v53.3L59.2,42.8C56.9,41.3,55,42.3,55,45v150c0,2.7,1.9,3.8,4.2,2.2L165,126.6v53.3h20v-120L165,60L165,60z"></path></svg>';

    jwp.addButton(
      nxt,
      "next",
      function () {
        jwp.playlistNext();
      },
      "btn-nxt"
    );
    jwp.addButton(
      prv,
      "previous",
      function () {
        jwp.playlistPrev();
      },
      "btn-prv"
    );
  };

  // Load jwplayer JS.  When loaded, replace the page contents
  // with a single div, and then insert jwplayer into the div
  // with the wanted playlist.
  Player.setup = function () {
    $.getScript("https://archive.org/jw/8/jwplayer.js", function () {
      Player.setupPlaylist();
      $("body").html('<div id="player"></div>');
      var jwp = jwplayer("player").setup({
        base: "https://archive.org/jw/8",
        playlist: Player.playlist,
        startparam: "start",
        width: "100%",
        height: "100%",
      });

      Player.addButtons(jwp);

      jwp.on("ready", function () {
        // console.log('ready', Player)

        jwp.on("time", function (evt) {
          var idx = jwp.getPlaylistIndex();
          if (!Player.ends[idx]) return;

          var diff = evt.position - Player.ends[idx];
          // console.log(evt.position, diff)
          if (diff >= 0 && diff < 1) {
            // we've passed the stop point!
            // NOTE: we require to be w/i 1s of stop point (should be 0 to .1s after _normally_)
            // so if a user starts manually seeking or moving around, we dont annoyingly robo-advance
            jwp.playlistItem(idx + 1);
          }
        });
      });
    });
  };

  Player.setup();
}); // end require(..)
// @license-end
