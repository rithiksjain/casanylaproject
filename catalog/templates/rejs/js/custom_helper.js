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

$(function() {
   
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
console.log("adding1");
var n =$(".slides .block").length;
++n;
console.log("adding");
$(".slides").append("<div class='block' id='Block"+(n)+"' onclick='func('.block')'>Block"+(n)+" </div>");
};

function test_func_img(){
console.log("adding1");
var n = $(".slides .block").length;
console.log("adding");
++n;
$(".slides").append("<div><img class='block' id='Block"+(n)+"' onclick='func('.block')' src='https://pbs.twimg.com/profile_images/839721704163155970/LI_TRk1z_400x400.jpg'></div>");
};

function test_func_slide(){
console.log("adding1");
var n = $(".slides .block").length;
console.log("adding");
++n;
$(".slides").append("<section class='block' id='Block"+(n)+"' onclick='func('.block')'>Block"+(n)+" </section>");
};