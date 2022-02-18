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
	  infinite: true,
	  slidesToShow: 2,
	  slidesToScroll: 1,
	  autoplay: true,
	  autoplaySpeed: 2000,
	  arrows: true,
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

var loaderEl = document.getElementsByClassName('fullpage-loader')[0];
document.addEventListener('readystatechange', () => {
	// const readyState = "interactive";
	var readyState = "complete";
    
	if(document.readyState == readyState) {
		// when document ready add lass to fadeout loader
		loaderEl.classList.add('fullpage-loader--invisible');
		
		// when loader is invisible remove it from the DOM
			setTimeout(()=>{
				loaderEl.parentNode.removeChild(loaderEl);
			}, 2000);
	}
});

window.addEventListener("load", function() {
    setTimeout(()=>{
      loaderEl.parentNode.removeChild(loaderEl);
    }, 2000);
});