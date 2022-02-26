
var $prog2 = $('.progress-indicator');
function updateProgress(perc){
    $prog2.css({width : perc*100 + '%'});
}

(function(){
    var $w = $(window);
    var $circ = $('.animated-circle');
    var $prog2 = $('.progress-indicator-2');
    var wh = $w.height();
    var h = $('body').height();
    var sHeight = h - wh;
    $w.on('scroll', function(){
        var perc = Math.max(0, Math.min(1, $w.scrollTop()/sHeight));
        updateProgress(perc);
    });
 
    function updateProgress(perc){
        var circle_offset = 126 * perc;
        $circ.css({
            "stroke-dashoffset" : 126 - circle_offset
        });
 
        $prog2.css({width : perc*100 + '%'});
    }
 
}());
