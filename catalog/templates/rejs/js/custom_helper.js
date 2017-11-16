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
$(".slides .present").append("<div class='block' onclick='func('.block')'><img id='block"+(n)+"' src='/images/3seatersofa.jpg'></div>");
var imgurl= localStorage.getItem('url');
document.getElementById('block'+(n)+'').src=imgurl;
};

function test_func_slide(){
$(".slides").append("<section class='present' data-markdown><script type='text/template'>ABC</script></section>");
};
