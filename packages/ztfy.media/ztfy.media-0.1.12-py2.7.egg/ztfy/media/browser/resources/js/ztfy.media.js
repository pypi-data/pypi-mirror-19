(function($, globals) {

	"use strict";

	var ZTFY_media = {

		initPlayer: function(player) {

			var callback = function() {
				var _player = $(player);
				var flowplayer = _player.flowplayer({
					swf: '/--static--/ztfy.media/flowplayer/flowplayer.swf',
					swfHls: '/--static--/ztfy.media/flowplayer/flowplayerhls.swf'
				});
				var events = _player.data('ztfy-flowplayer-events');
				if (events) {
					for (var event in events) {
						if (!events.hasOwnProperty(event)) {
							continue;
						}
						flowplayer.on(event, $.ZTFY.getFunctionByName(events[event]));
					}
				}
			};

			if (!$.fn.flowplayer) {
				$.ZTFY.skin.getCSS('/--static--/ztfy.media/flowplayer/skin/functional.css', 'flowplayer');
				$.ZTFY.getScript('/--static--/ztfy.media/flowplayer/flowplayer.js', callback);
			} else {
				callback();
			}
		},

		initPlayerDialog: function() {
			var player = $(this);
			$(player).parents(':first').removeAttr('style');
		},

		shutdownPlayerDialog: function() {
			var dialog = $(this);
			var player = $('.flowplayer', dialog).data('flowplayer');
			player.shutdown();
		}
	};
	$.ZTFY_media = ZTFY_media;

})(jQuery, this);
