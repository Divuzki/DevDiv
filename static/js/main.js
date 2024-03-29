(function($) {

	"use strict";

	var fullHeight = function() {

		$('.js-fullheight').css('height', $(window).height());
		$(window).resize(function(){
			$('.js-fullheight').css('height', $(window).height());
		});

	};
	fullHeight();

})(jQuery);

// Blog Slider
$(document).ready(function() {
	var config = {
	  infinite: false,
	  slidesToShow: 2,
	  slidesToScroll: 1,
	  autoplay: true,
	  autoplaySpeed: 2000,
	  arrows: false,
	  responsive: [
		{
		  breakpoint: 850,
		  settings: {
			slidesToShow: 1
		  }
		}
	  ]
	};
	
	$('#slick-container-shoutouts').slick(config);
  });