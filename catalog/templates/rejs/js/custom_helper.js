$.fn.extend({

    /**
     * Children of the element with the given selector
     * will automatically be made draggable
     * @param {String} selector
     *  The selector of the child / descendant elements
     *  to automatically be made draggable
     * @param {Object} opts
     *  The options that would normally be passed to the
     *  draggable method
     * @returns
     *  The jQuery array for chaining
     */
    draggableChildren: function(selector, opts) {
      console.log("hello");

        // On using event delegation to automatically
        // handle new child events
        $(this).on("mouseover", selector, function() {

           // Check that draggable not already initialized
           console.log(1);
           if(!$(this).is(":ui-draggable")){
            console.log(2);
               // Initialize draggable
               $(this).draggable(opts).resizable(opts);
           }

          console.log(3);
        });

        // Return this for chaining
        return this;
    }

});

$(function() 
{   
    $(".slides").draggableChildren(".block", {
        drag: function() {
            console.log("Dragging");   
        },
        stop: function() {
            console.log("I'm out of place");   
        }
    });
    
});

function test_func_text(){
var n =$(".slides .block").length;
++n;
$(".slides .present").append("<div class='block' id='block"+(n)+"' onclick='func('.block')' style='border: 2px solid;'>Block"+(n)+" </div>");
};

function test_func_img(){
var n = $(".slides .block").length;
++n;
$(".slides .present").append("<div class='block' id='block"+(n)+"' onclick='func('.block')'><img id='block"+(n)+"' src=''></div>");
var imgurl= localStorage.getItem('url');
document.getElementById('block'+(n)+'').src=imgurl;
};

function test_func_slide(){
$(".slides").append("<section class='present' data-markdown><script type='text/template'>ABC</script></section>");
};

function post_call(data)
{
    console.log("Saving")
    $.ajax({
      type: "POST",
      url: "/saveslide",
      data : data
    }).done(function() {
        console.log("Saved")
    });
}

function save_func(){
array=[]
$.each($('#slides').children(),function(i,j)
{
  if($(j).attr('class')=="present")
  {
    $.each($(j).children(),function(k,l)
    {
      array.push($(l).attr('id'))
    });
  };
});

dict={}
dict["desc"] = array[0];
dict["pos_x"] = $('#'+array[0]).offset().left;
dict["pos_y"] = $('#'+array[0]).offset().top;
dict["height"] = $('#'+array[0]).height();
dict["width"] = $('#'+array[0]).width();
dict["idcat"] = 1;
post_call(dict)
};
/*
function test_func_slide(){
console.log("adding1");
var section = $("<section>Welcome</section>");
slides.append(section);
section.attr('data-markdown', '');
var script = $("<script></script>");
section.append(script);
script.attr('type', 'text/template');
};
*/
