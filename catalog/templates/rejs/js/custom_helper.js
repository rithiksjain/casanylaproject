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
var s_d_id = '';

function test_func_text(){
var n =$(".slides .block").length;
++n;
$('.slides .present').append("<div class='block' id='block"+(n)+"' onclick='edit_text(`block"+(n)+"`,1); func(`.block`);' style='border: 2px solid;'>Edit here</div>");
s_d_id="block"+n;
values="Edit here";
};

var values = '';
function GetTextValue() {
  if (s_d_id){
    div_id=s_d_id;
    $('.input').each(function() {
            values=this.value
        });
    edit_text(div_id,0);

  }
    }

function edit_text(div_id,opt){
  console.log($("#"+div_id).text());
  if (opt==1){
    document.getElementById('input').value=$("#"+div_id).text();
    values=$("#"+div_id).text();
  }
  $('#'+div_id).resizable('destroy');
  $("#"+div_id).text(values);
  $('#'+div_id).resizable();
  // document.getElementById(div_id).innerHTML=values;
  s_d_id=div_id;
}

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
    }).done(function(param) {
        console.log(param);
        /*if (param.status==true)
          alert('Slide Saved');
        else
          alert("Error");*/
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

final_array=[];
$.each(array,function(i)
{
dict={};
dict["desc"] = $('#'+array[i]).text();
dict["pos_x"] = $('#'+array[i]).position().left;
dict["pos_y"] = $('#'+array[i]).position().top;
dict["height"] = $('#'+array[i]).height();
dict["width"] = $('#'+array[i]).width();
dict["idcat"] = 1;
final_array.push(dict);
});
console.log(final_array);
$.each(final_array,function(i,j)
{
  console.log(j);
  post_call(j);
});
};

var urls = [{'key':'elements', 'url': '/slide'}];
function success_get(data){
  console.log(data);
}

function init(p_id,s_id){
  var url1=[{}];
  url1[0]["key"]=urls[0].key;
  url1[0]["url"] = urls[0].url+'/'+p_id+'/'+s_id;
  console.log(url1);
  async_call=new async_helper();
async_call.get_call(url1).then(function(result){
                success_get(result);
            },function(error){
      console.log("Network Error")
});
};

init(1,1);
/*
function imageupload(){
async_calls = new async_helper()
var urls = [{'key':'elements', 'url': '/uploadimage'}];
console.log($('form').serialize());
};

$('form').submit(function(e){
console.log(e);
e.preventDefault();
});
*/