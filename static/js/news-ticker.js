/*
 Copyright (C) DevDiv Inc 2022
 Distributed under the MIT License (license terms are at http://opensource.org/licenses/MIT).
 */
(function ($, window, document, undefined) {
  var name = "easyTicker",
    defaults = {
      direction: "up",
      easing: "swing",
      speed: "slow",
      interval: 2000,
      height: "auto",
      visible: 0,
      mousePause: 1,
      controls: {
        up: "",
        down: "",
        toggle: "",
        playText: "Play",
        stopText: "Stop",
      },
    };
  function EasyTicker(el, options) {
    var s = this;
    s.opts = $.extend({}, defaults, options);
    s.elem = $(el);
    s.targ = $(el).children(":first-child");
    s.timer = 0;
    s.mHover = 0;
    s.winFocus = 1;
    init();
    start();
    $([window, document])
      .off("focus.jqet")
      .on("focus.jqet", function () {
        s.winFocus = 1;
      })
      .off("blur.jqet")
      .on("blur.jqet", function () {
        s.winFocus = 0;
      });
    if (s.opts.mousePause == 1) {
      s.elem
        .mouseenter(function () {
          s.timerTemp = s.timer;
          stop();
        })
        .mouseleave(function () {
          if (s.timerTemp !== 0) start();
        });
    }
    $(s.opts.controls.up).on("click", function (e) {
      e.preventDefault();
      moveDir("up");
    });
    $(s.opts.controls.down).on("click", function (e) {
      e.preventDefault();
      moveDir("down");
    });
    $(s.opts.controls.toggle).on("click", function (e) {
      e.preventDefault();
      if (s.timer == 0) start();
      else stop();
    });
    function init() {
      s.elem.children().css("margin", 0).children().css("margin", 0);
      s.elem.css({
        position: "relative",
        height: s.opts.height,
        overflow: "hidden",
      });
      s.targ.css({ position: "absolute", margin: 0 });
      setInterval(function () {
        adjHeight();
      }, 100);
    }
    function start() {
      s.timer = setInterval(function () {
        if (s.winFocus == 1) {
          move(s.opts.direction);
        }
      }, s.opts.interval);
      $(s.opts.controls.toggle)
        .addClass("et-run")
        .html(s.opts.controls.stopText);
    }
    function stop() {
      clearInterval(s.timer);
      s.timer = 0;
      $(s.opts.controls.toggle)
        .removeClass("et-run")
        .html(s.opts.controls.playText);
    }
    function move(dir) {
      var sel, eq, appType;
      if (!s.elem.is(":visible")) return;
      if (dir == "up") {
        sel = ":first-child";
        eq = "-=";
        appType = "appendTo";
      } else {
        sel = ":last-child";
        eq = "+=";
        appType = "prependTo";
      }
      var selChild = s.targ.children(sel);
      var height = selChild.outerHeight();
      s.targ
        .stop(true, true)
        .animate(
          { top: eq + height + "px" },
          s.opts.speed,
          s.opts.easing,
          function () {
            selChild.hide()[appType](s.targ).fadeIn();
            s.targ.css("top", 0);
            adjHeight();
          }
        );
    }
    function moveDir(dir) {
      stop();
      if (dir == "up") move("up");
      else move("down");
    }
    function fullHeight() {
      var height = 0;
      var tempDisp = s.elem.css("display");
      s.elem.css("display", "block");
      s.targ.children().each(function () {
        height += $(this).outerHeight();
      });
      s.elem.css({ display: tempDisp, height: height });
    }
    function visHeight(anim) {
      var wrapHeight = 0;
      s.targ.children(":lt(" + s.opts.visible + ")").each(function () {
        wrapHeight += $(this).outerHeight();
      });
      if (anim == 1) {
        s.elem.stop(true, true).animate({ height: wrapHeight }, s.opts.speed);
      } else {
        s.elem.css("height", wrapHeight);
      }
    }
    function adjHeight() {
      if (s.opts.height == "auto" && s.opts.visible != 0) {
        anim = arguments.callee.caller.name == "init" ? 0 : 1;
        visHeight(anim);
      } else if (s.opts.height == "auto") {
        fullHeight();
      }
    }
    return {
      up: function () {
        moveDir("up");
      },
      down: function () {
        moveDir("down");
      },
      start: start,
      stop: stop,
      options: s.opts,
    };
  }
  $.fn[name] = function (options) {
    return this.each(function () {
      if (!$.data(this, name)) {
        $.data(this, name, new EasyTicker(this, options));
      }
    });
  };
})(jQuery, window, document);
$(".news-ticker").each(function () {
  var domainname = $(this).attr("data-domain");
  var url =
    "https://" +
    domainname +
    "/feeds/posts/summary/?max-results=5&alt=json-in-script";
  var thisc = $(this);
  thisc.append(
    '<div class="tickerwrapper none"><span class="tickhead">Latest News</span><div class="ticker2"><ul></ul></div></div>'
  );
  $.ajax({
    type: "GET",
    url: url,
    async: false,
    contentType: "application/json",
    dataType: "json",
    success: function (json) {
      for (var i = 1; i < json.feed.entry.length; i++) {
        for (var j = 0; j < json.feed.entry[i].link.length; j++) {
          if (json.feed.entry[i].link[j].rel == "alternate") {
            var postUrl = json.feed.entry[i].link[j].href;
            break;
          }
        }
        var postTitle = json.feed.entry[i].title.$t;
        var item = '<li><a href="' + postUrl + '">' + postTitle + "</a></li>";
        $(".ticker2 ul", thisc).append(item);
      }
      $(".ticker2").easyTicker({
        direction: "up",
        easing: "swing",
        speed: "slow",
        interval: 2000,
        height: "auto",
        visible: 0,
        mousePause: 1,
      });
    },
  });
});
