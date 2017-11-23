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
$('#splbtn').effect( "transfer", { to: "#main", className: "ui-effects-transfer" }, 1000 );
// edit_text(s_d_id,1);
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

function StorageEvent(e){
  console.log("i am active");
  var value=0;
  if(localStorage.getItem('upload_img_added')!=null){
    value = localStorage.getItem('upload_img_added');
  }
  else if(localStorage.getItem('catalog_img_added')!=null){
    value = localStorage.getItem('catalog_img_added');    
  }
    else{
      return 0;
  }
  console.log(value);
if (value==1){
  test_func_img();
  localStorage.clear();
  }

}
  
function upload(){
  console.log("upload");
  $('#uploaddiv').hide(500);
 localStorage.setItem('upload_img_added',0);
 window.addEventListener('storage', StorageEvent);
} 

function add_from_catalog(){
  localStorage.setItem( 'from_catalog', 1 );
  localStorage.setItem( 'catalog_img_added', 0 );
  window.open("/itemfetch?id=1",'_blank');
  window.addEventListener('storage', StorageEvent);
}


function test_func_img(){
var n = $(".slides .block").length;
++n;
$(".slides .present").append("<div class='block' id='block"+(n)+"' onclick='func('.block')'><img src=''></div>");
var imgurl= localStorage.getItem('url');
$($('#block'+(n)).children()).attr("src",imgurl );
};

// function test_func_slide(slide_id){
// $(".slides").append("<section class='present' class='slide_el' id='"+slide_id+"'' data-markdown><script type='text/template'></script></section>");    
// };
function test_func_slide(){  
  // Reveal.add('<h3>Slide title</h3>') 
$(".slides").append("<section class='present' data-markdown><script type='text/template'></script><div></div></section>");
};

// function add_slide(){
//   console.log("adding slide");
//   url='/addslide?id='+pr_id;
//   async_call.get_call(url1).then(function(result)
//     {
//       console.log(result.default);
//       // test_func_slide()
//     },
//     function(error){
//     console.log("Network Error")
// });
// }

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
arr=[]
$.each($('#slides').children(),function(i,j)
{
  // console.log(j);
  if($(j).hasClass('present'))
  {
    // console.log(j);
    $.each($(j).children(),function(k,l)
    {
      // console.log("property");
      // console.log(l);
      arr.push($(l).attr('id'))
    });
  };
});

console.log(arr);

final_array=[];
$.each(arr,function(i)
{
dict={};
dict["desc"] = $('#'+arr[i]).text();
dict["pos_x"] = parseInt($('#'+arr[i]).position().left);
dict["pos_y"] = parseInt($('#'+arr[i]).position().top);
dict["height"] = parseInt($('#'+arr[i]).height());
dict["width"] = parseInt($('#'+arr[i]).width());
dict["idcat"] = 1;
//extra code here revert back if required
dict["s_id"]=c_slide;
// till this point
final_array.push(dict);
});

// console.log(final_array);
$.each(final_array,function(i,j)
{
  console.log(j);
  post_call(j);
});
};

function post_init(result){
  console.log(result);
  if (result.elements.status){
    // call successful
    var data = result.elements.data;
    console.log(data);
    slide_data();
  }
  else{
    //call failed
  }
}

function slide_data(result){
  // this is for each slide rearrange slide elements here
  console.log("hellabbo");
  $.each(result,function(i){
  var a=result.elements.data.text[i]['id'];
  var posx=result.elements.data.text[i]['position_x'];
  var posy=result.elements.data.text[i]['position_y'];
  var wid=result.elements.data.text[i]['object_breadth'];
  var len=result.elements.data.text[i]['object_length'];
  $("blockdb"+(a)+"").css({"width":"wid","height":"len", "position.top":"posy","position.left":"posx"});
  });
}


var urls = [{'key':'elements', 'url': '/slide'}];

function init(p_id,s_id){
  c_slide=s_id;
  var url1=[{}];
  url1[0]["key"]=urls[0].key;
  url1[0]["url"] = urls[0].url+'/'+p_id+'/'+s_id;
  // console.log(url1);

  async_call=new async_helper();    
  async_call.get_call(url1).then(function(result){
  // console.log(result);
  if (s_id==0){
    result={"data": {"text": [{"object_breadth": 100, "temp_url": null, "p_id": 0, "URL": null, "id": 1, "position_x": 21, "object_length": 156, "position_y": 265, "s_id": 1}, {"object_breadth": 100, "temp_url": null, "p_id": 0, "URL": null, "id": 2, "position_x": -1, "object_length": 156, "position_y": 432, "s_id": 1}, {"object_breadth": 100, "temp_url": null, "p_id": 0, "URL": null, "id": 3, "position_x": -36, "object_length": 156, "position_y": 661, "s_id": 1}, {"object_breadth": 64, "temp_url": null, "p_id": 0, "URL": null, "id": 4, "position_x": -150, "object_length": 10, "position_y": 616, "s_id": 1}, {"object_breadth": 44, "temp_url": null, "p_id": 0, "URL": null, "id": 5, "position_x": -114, "object_length": 143, "position_y": 239, "s_id": 1}, {"object_breadth": 282, "temp_url": null, "p_id": 0, "URL": null, "id": 6, "position_x": 47, "object_length": 57, "position_y": 382, "s_id": 1}, {"object_breadth": 100, "temp_url": null, "p_id": 0, "URL": null, "id": 7, "position_x": -56, "object_length": 52, "position_y": 502, "s_id": 1}, {"object_breadth": 100, "temp_url": null, "p_id": 0, "URL": null, "id": 8, "position_x": 20, "object_length": 154, "position_y": 0, "s_id": 1}, {"object_breadth": 100, "temp_url": null, "p_id": 0, "URL": null, "id": 9, "position_x": -89, "object_length": 52, "position_y": 313, "s_id": 1}, {"object_breadth": 100, "temp_url": null, "p_id": 0, "URL": null, "id": 10, "position_x": -114, "object_length": 154, "position_y": 66, "s_id": 1}, {"object_breadth": 100, "temp_url": null, "p_id": 0, "URL": null, "id": 11, "position_x": -122, "object_length": 52, "position_y": 372, "s_id": 1}, {"object_breadth": 100, "temp_url": null, "p_id": 0, "URL": null, "id": 12, "position_x": 20, "object_length": 144, "position_y": 0, "s_id": 1}, {"object_breadth": 100, "temp_url": null, "p_id": 0, "URL": null, "id": 13, "position_x": 54, "object_length": 52, "position_y": 336, "s_id": 1}], "url": [], "slides": [1]}, "status": true};
    post_init(result);
    }
  else{
    slide_specific(result);
  }
    },function(error){
      console.log("Network Error")
});
};

//init(1,1);
/*
=======
// init(1,1);

>>>>>>> 10f9de4b6552fb4df8c7cc5d8ce6319c26a2fc11
var doc = new jsPDF();
var specialElementHandlers = {
    '#editor': function (element, renderer) {
        return true;
    }
};
*/
function download() {
    var doc = new jsPDF();
    var specialElementHandlers = {
    '#editor': function (element, renderer) {
        return true;
    }
    };
    
    doc.fromHTML($('.reveal').html(), 15, 15, {
        'width': 170,
            'elementHandlers': specialElementHandlers
    });
    doc.save('sample_file.pdf');
};
 // init(1,1,1);