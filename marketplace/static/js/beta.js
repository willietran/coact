/**
 * Created by WillieTran on 7/27/14.
 */
$(document).ready(function () {

    $(".player").mb_YTPlayer();

    var classes = function() {
        $.ajax({
            url:'/class_list/',
            type: 'GET',
            datatype: 'html',
            success: function(response) {
                console.log(response);
                console.log("Totally got it");
                $('.class-list').html(response);
                $('.class-list').toggle();
            },
            error: function(response) {
                console.log(response);
                console.log("Nope");
            }
        })
    };

    classes();


    $(".moreClassButton").on('click', function() {
        $('.class-list').slideToggle("slow");
    });


//    $(".teacher-one").hover(function() {
////        $(".teacher-one").css('background-color', 'rgba(0, 0, 0, .5)');
//        $('.teacher-one').html('<p>stuff</p>');
////        $(".teacher-one").slideToggle("slow");
//    })

    $(function() {
      $('a[href*=#]:not([href=#])').click(function() {
        if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
          var target = $(this.hash);
          target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
          if (target.length) {
            $('html,body').animate({
              scrollTop: target.offset().top
            }, 1000);
            return false;
          }
        }
      });
    });
});