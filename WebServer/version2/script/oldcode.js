$document.ready()
{

}
var x = false;
// --------------------------------------------------------------------------------
//              Loading screen
// --------------------------------------------------------------------------------
$("#page").hide()
$("#loading_screen").css("background-color", "black")



$('#skip').click(function() {
$('.progress-circle-outer').removeClass('animate');
$("#loading_screen").fadeOut(4000);
$("#page").fadeIn(8000);
})



function innerText(elm, text, mc)
{

  var len = 0;
  function locking()
  {
      var elm_obj = document.getElementById(elm);

      var timeoutId = setTimeout(locking, mc)

      if(text[len] != undefined) elm_obj.innerHTML += text[len];
      else clearTimeout(timeoutId)

      len++;
  }
  locking();
}
setTimeout(function(){
innerText('loading_screen_date','February 19, 1964', 200);
}, 3000);
setTimeout(function(){
innerText('loading_screen_entry','My sweet, sweet Lily... ', 80);
}, 7300);
setTimeout(function(){
innerText('loading_screen_entry','Oh how I miss you, my innocent child.', 80);
}, 9400);
setTimeout(function(){
innerText('loading_screen_entry',' Its been seven years now, but it still feels as if it was yesterday that  cancer took you away from me. Usually I would be halfway towards your gravestone, as is tradition today, however a letter appeared under my door. A missing girl with your name...', 80);
}, 13000);
setTimeout(function(){
innerText('loading_screen_entry',' Such an unlikely coincidnce for it to happen today...', 80);
}, 34500);
setTimeout(function(){
innerText('loading_screen_entry',' This day...', 80);
}, 40000);
setTimeout(function(){
innerText('loading_screen_entry',' The day I lost you...', 80);
}, 42000);

var $num = $('.number'),
    times = 0;

for(i=0; i<=100; i++) {
    setTimeout(function() {
        $num.html(times + "%");
        times++;
        if (times === 100) {
            $('.progress-circle-outer').removeClass('animate');
            $("#loading_screen").fadeOut(4000);
            $("#page").fadeIn(8000);
        }
    },i*450)
};


// // --------------------------------------------------------------------------------
// //              image hover animations
// // --------------------------------------------------------------------------------
$(".images").hover(function(){
  $(this).clearQueue()
  $(this).animate({
    width: "140%",
    height: "140%",
    marginLeft: "-75px",
    marginTop: "-30px"
  }, 700)
},
function(){
  $(this).clearQueue()
  $(this).animate({
    width: "100%",
    height: "100%",
    marginLeft: "0px",
    marginTop: "0px"
  }, 700)
});

$("#test2").hover(function(){
  $(this).clearQueue()
  $(this).animate({
    width: "140%",
    height: "140%",
    marginLeft: "-75px",
    marginTop: "60px"
  }, 700)
},
function(){
    $(this).clearQueue()
    $(this).animate({
    width: "100%",
    height: "100%",
    marginLeft: "0px",
    marginTop: "110px"
  }, 700)
});


// --------------------------------------------------------------------------------
//              Transition animations
// --------------------------------------------------------------------------------


$(".review").hide();
$("#screenShots").hide();


$("#reviews").click(function(){
$(".review").css("margin", "0");
$("#page").animate({
  marginLeft: "1500px",
  opacity: "hide"
}, 3000)
$(".review").animate({
  opacity: "show"
}, 4000)
})
$("#main_reviews").click(function(){
$("#page").css("margin", "0");
$(".review").animate({
  marginLeft: "-1500px",
  opacity: "hide"
}, 3000)
$("#page").animate({
  opacity: "show"
}, 4000)
})

$("#screen_shots").click(function(){
$("#screenShots").css("margin", "0");
$("#page").animate({
  marginLeft: "-1500px",
  opacity: "hide"
}, 3000)
$("#screenShots").animate({
  opacity: "show"
},
{
  duration: 4000,
  complete: function()
  {
    $(".clipboard_hover").delay(4000).fadeIn(1500);
    $(".classified").delay(4000).fadeIn(1500);
    $(".videos").delay(4000).fadeIn(1500);
  }
})
})
$("#main_screnShots").click(function(){
$("#page").css("margin", "0");
$("#screenShots").animate({
  marginLeft: "1500px",
  opacity: "hide"
}, 3000)
$("#page").animate({
  opacity: "show"
}, 4000)
  $(".clipboard_hover").delay(4000).fadeOut(1500);
  $(".classified").delay(4000).fadeOut(1500);
  $(".videos").delay(4000).fadeOut(1500);
})


$("#storyLine").click(function(){
$("#page").animate({
  marginTop: "-1500px",
  opacity: "hide"
},
{
  duration: 3000,
  complete: function()
  {
    window.open("storyLine.html", "_self");
  }
})
})

// --------------------------------------------------------------------------------
//              auidio
// --------------------------------------------------------------------------------

$(".mute").click( function (){
  $("audio").prop('muted', !$("audio").prop('muted'));
});
// --------------------------------------------------------------------------------
//              flicker animation on title
// --------------------------------------------------------------------------------

function flicker()
{
$("#lbl").removeClass("illuminated");
setTimeout(function()
{
  $("#lbl").addClass("illuminated");
},50);
}

function triggerFlicker()
{
//var times = Math.floor(Math.random()*4);
//for(var i=0; i<times; i++)
//{
  setTimeout(flicker,/*i**/500);
//}
setTimeout(triggerFlicker,Math.floor(Math.random()*5000)/*+(times*100)+(250)*/);
}1

triggerFlicker();

jQuery.fn.center = function () {
  this.css("position","absolute");
  this.css("top", Math.max(0, (($(window).height() - $(this).outerHeight()) / 2) +
                                              $(window).scrollTop()) + "px");
  this.css("left", Math.max(0, (($(window).width() - $(this).outerWidth()) / 2) +
                                              $(window).scrollLeft()) + "px");
  return this;
}
// For reviews page
$(".shard").click(function(){
  $(this).css({'position': 'absolute', 'z-index':'1000'});
  $(this).clearQueue()
  //$(this).center()
  $(this).animate({

    width: "150%",
    height: "150%",
    margin: "0",
    top: "0",
    marginLeft: "-390px",
    marginTop: "80px"


})



});

      var small={width: "400px",height: "300px"};
      var large={width: "600px",height: "500px", "z-index": "2000", postion: "absolute", align:"center"};
      var count=1;
      $(".rev").css(small).on('click',function () {
          $(this).animate((count==1)?large:small);
          count = 1-count;
      });


 $('.mute').click(function(){
  $(this).find('span').toggleClass('glyphicon-volume-up').toggleClass('glyphicon-volume-off');
});


$(function(){
var front = $('.Front'),
    others = ['Left2', 'Left', 'Right', 'Right2'];

$('.Carousel').on('click', '.Items', function() {
  var $this = $(this);

  $.each(others, function(i, cl) {
    if ($this.hasClass(cl)) {
      front.removeClass('Front').addClass(cl);
      front = $this;
      front.addClass('Front').removeClass(cl);
    }
  });
});
});

$(".images2").hover(function(){
  $(this).clearQueue()
  $(this).animate({
    width: "170%",
    height: "170%",
    marginLeft: "-200px",
    marginTop: "-30px"
  }, 700)
},
function(){
  $(this).clearQueue()
  $(this).animate({
    width: "100%",
    height: "100%",
    marginLeft: "0px",
    marginTop: "0px"
  }, 700)
});


//For scroller
var itemPositions = [];
var numberOfItems = $('#scroller .item').length;

/* Assign each array element a CSS class based on its initial position */
function assignPositions() {
  for (var i = 0; i < numberOfItems; i++) {
      if (i === 0) {
          itemPositions[i] = 'left-hidden';
      } else if (i === 1) {
          itemPositions[i] = 'left';
      } else if (i === 2) {
          itemPositions[i] = 'middle';
      } else if (i === 3) {
          itemPositions[i] = 'right';
      } else {
          itemPositions[i] = 'right-hidden';
      }
  }
  /* Add each class to the corresponding element */
  $('#scroller .item').each(function(index) {
      $(this).addClass(itemPositions[index]);
  });
}

/* To scroll, we shift the array values by one place and reapply the classes to the images */
function scroll(direction) {
  if (direction === 'prev') {
      itemPositions.push(itemPositions.shift());
  } else if (direction === 'next') {
      itemPositions.unshift(itemPositions.pop());
  }
  $('#scroller .item').removeClass('left-hidden left middle right right-hidden').each(function(index) {
      $(this).addClass(itemPositions[index]);
  });
}

/* Do all this when the DOMs ready */
$(document).ready(function() {

  assignPositions();
  var autoScroll = window.setInterval("scroll('next')", 4000);

  /* Hover behaviours */
  $('#scroller').hover(function() {
      window.clearInterval(autoScroll);
      $('.nav').stop(true, true).fadeIn(200);
  }, function() {
      autoScroll = window.setInterval("scroll('next')", 4000);
      $('.nav').stop(true, true).fadeIn(200);
  });

  /* Click behaviours */
  $('.prev').click(function() {
      scroll('prev');
  });
  $('.next').click(function() {
      scroll('next');
  });

});
// --------------------------------------------------------------------------------
//             screenshots
// --------------------------------------------------------------------------------

$(".clipboard_hover").hide();


var index = 1;
$('.clipboard_hover').hover(function() {
index++;
$(this).css("zIndex", index)
$(this).animate({
  width: "18%",
  marginLeft: "-6%",
}, 1000)
$("img",this).animate({
  marginLeft: "0%",
  width: "100%"
}, 1000)
}, function() {
var elem = $(this).attr('class').split(' ')[1];
// console.log(elem);
if($(this).attr('id') == "overlay1")
{
  $(this).animate({
    width: "6.3%",
    marginLeft: "0",
  }, 1000)
  $("img",this).animate({
    marginLeft: "-100%",
    width: "280%"
  }, 1000)
}
else if(elem == "2")
{

  $(this).animate({
    width: "4.6%",
    marginLeft: "0",
  }, 1000)
  $("img",this).animate({
    marginLeft: "-100%",
    width: "250%"
  }, 1000)
}
else if(elem == "3")
{

  $(this).animate({
    width: "4.6%",
    marginLeft: "0",
  }, 1000)
  $("img",this).animate({
    marginLeft: "-100%",
    width: "280%"
  }, 1000)
}
else if(elem == "4")
{

  $(this).animate({
    width: "2.8%",
    marginLeft: "0",
  }, 1000)
  $("img",this).animate({
    marginLeft: "-100%",
    width: "280%"
  }, 1000)
}
})

// --------------------------------------------------------------------------------
//             modals
// --------------------------------------------------------------------------------

$('.M_image').click(function() {
var src = $(this).attr("src");

$("#myModal").css("display","block")
$("#img01").attr("src",src)
})
$(".close").click(function(){
$("#myModal").css("display","none")
})


$('.videos').click(function() {
var src = $(this).attr("data");
var mute = false;
console.log(src);
$("audio").prop('muted',true);


$("#myModal2").css("display","block")
$("iframe").css("borderRadius", "0%")
$("#vid01").attr("src",src)
})
$(".close").click(function(){
$("#myModal2").css("display","none")
$("iframe").css("borderRadius", "50%")
$("audio").prop('muted',false);
})

var demo = (function (window) {

  'use strict';

  var SELECTORS = {
          textRows: '.row'
      },

      CLASSES = {
          drawingWord: 'drawing'
      },

      textRows = document.querySelectorAll(SELECTORS.textRows);



  function applyDrawEffect (rowSVG) {
    rowSVG.classList.add(CLASSES.drawingWord);
  }


  function drawWords () {
      [].forEach.call(textRows, applyDrawEffect);
  }


  function init () {
      drawWords();
  }


  return {
      init: init
  };

}(window));




window.addEventListener('DOMContentLoaded', demo.init, false);


$("#hiddenStory").hide();

$("#readMore").click(function(){

  $("#hiddenStory").show();
   $("#hiddenStory2").hide();

})

$("#readBook").click(function(){

  $("#hiddenStory").hide();
   $("#hiddenStory2").show();

})
