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

function func(element){
      console.log("hola");
      s_d_id=$($(element)[0]).attr('id');
  }

function test_func_text(){
var n =$(".slides .block").length;
++n;
$('.slides .present').append("<div class='block' id='blocktemp_"+(n)+"' onclick='edit_text($(this),1);' style='border: 2px solid; position:absolute; top:50px; left:50px;color:black;'>Edit here</div>");
s_d_id="blocktemp_"+n;
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

function edit_text(element,opt){
  if (opt==0){
  div_id = element;  
  }
  else{
  div_id = $($(element)[0]).attr('id');
  }
  // console.log($("#"+div_id).text());
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



function RemoveValue() {
  if (s_d_id){
    div_id=s_d_id;
    delete_element(div_id);
  }
}

function delete_element(div_id){
  var div = document.getElementById(div_id);
  div.remove();
  console.log(div_id);
  del={}
  block_id_prep_text=div_id.slice(0,div_id.indexOf('_'))
  if (block_id_prep_text=="blocktemp"){
    return 0;
  }
  del["id"]=parseInt(div_id.slice(div_id.indexOf('_')+1,div_id.length));
  console.log(del["id"]);
  delete_ele(del);
}

function delete_ele(data)
{
  console.log("Deleting")
  $.ajax({
    type: "POST",
    url: "/delete",
    data : data
  }).done(function(d){
    console.log(d);
  });
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

// $(".slides .block").on( "click", function() {
//   console.log("^^^^^^^^^");
//   console.log(this);
// });

function test_func_img(){
var n = $(".slides .block").length;
++n;
$(".slides .present").append("<div class='block' id='blocktemp_"+(n)+"' onclick='func($(this))' style='position:absolute; top:70px; left:70px;'><img src=''></div>");
var imgurl= localStorage.getItem('url');
$($('#blocktemp_'+(n)).children()).attr("src",imgurl );
};

// function test_func_slide(slide_id){
// $(".slides").append("<section class='present' class='slide_el' id='"+slide_id+"'' data-markdown><script type='text/template'></script></section>");    
// };
function test_func_slide(){  
  // Reveal.add('<h3>Slide title</h3>')
  temp={}
  temp["id"]=pr_id;
  addslide(temp);
};

function addSlideFrontend(id,na_present){
  if(na_present==0){
    $($(".slides").children()[0]).attr("id","slide_"+id);
  }
  else{
    $(".slides").prepend("<section id='slide_"+id+"' data-markdown data-state=intro> </section>");  
  }
}


function addslide(data)
{
  console.log("Adding")
  $.ajax({
    type: "POST",
    url: "/addslide",
    data : data
  }).done(function(p){
    console.log(p);
    if (p.status){
      addSlideFrontend(p.slide_id);
    }
  });
}


function change_div_id(present_id,changed_id){
  $("#"+present_id).attr("id",changed_id);
}



function post_call(data)
{
    console.log("Saving")
    $.ajax({
      type: "POST",
      url: "/saveslide",
      data : data
    }).done(function(param) {
        if (param.status==true)
        {
          if (data["temp_id"])
          {
            console.log(data["temp_id"]);
            changed_id = "blockdb_"+param.block_id;
            console.log(changed_id);
            change_div_id(data["temp_id"],changed_id);
          }
          else{
                      console.log(data["id"]);
          }

        }
        else{

        }
    });
}

function save_func(){
arr=[];
$.each($('#slides').children(),function(i,j)
{
  if($(j).hasClass('present'))
  { 
    c_slide=parseInt(j.id.slice(j.id.indexOf('_')+1,j.id.length));
    // return 0;
    $.each($(j).children(),function(k,l)
    {
      console.log(l);
       arr.push($(l).attr('id'))
    });
  };
});

console.log(arr);
// var cat_id = localStorage.getItem('id_cat');
final_array=[];
$.each(arr,function(i)
{
  dict={};

    block_id=arr[i].slice(arr[i].indexOf('_')+1,arr[i].length)
    block_id_prep_text=arr[i].slice(0,arr[i].indexOf('_'))

    if (block_id_prep_text=="blocktemp")
    {
    dict["temp_id"]=arr;
    dict["id"]=0;
        }
    else
    {
    dict["id"]=block_id;
    dict["temp_id"]="";
      }

    dict["desc"] = $('#'+arr[i]).text();
    dict["pos_x"] = parseInt($('#'+arr[i]).position().left);
    dict["pos_y"] = parseInt($('#'+arr[i]).position().top);
    dict["height"] = parseInt($('#'+arr[i]).height());
    dict["width"] = parseInt($('#'+arr[i]).width());
    
    if(dict["desc"]=="")
      dict["url"] = $($('#'+arr[i]).children()).attr('src');
    else
      dict["url"]="";

    if(dict["url"]=="")
        dict["idcat"] = 1;
    else
      dict["idcat"] = "";
    dict["s_id"]=c_slide;

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
    //create slides
    $.each(data.slides,function(i,j){
      console.log(j);
      addSlideFrontend(j,na_present=i);
    });
    slide_data(result);
  }
  else{
    //call failed
  }
}

function slide_data(result){
  // this is for each slide rearrange slide elements here
  css_data = result.elements.data.text;
  css_url = result.elements.data.url;
  // console.log(result);
  for (i= 0; i < css_data.length; ++i) {
  a = css_data[i]['id'];
  posx=css_data[i]['position_x'];
  posy=css_data[i]['position_y'];
  wid=css_data[i]['object_breadth'];
  len=css_data[i]['object_length'];
  text=css_data[i]['e_desc'];
  $('#slide_'+css_data[i]['s_id']).append("<div class='block' id='blockdb_"+(a)+"' onclick='edit_text($(this),1);' style='border: 2px solid;'></div>");
  //$("#blockdb_"+(a)+"").css({"width":"wid","height":"len","position":"relative","top":"posy","left":"posx"});
  document.getElementById("blockdb_"+(a)+"").innerHTML=text;
  $("#blockdb_"+(a)+"").css('width', wid);
  $("#blockdb_"+(a)+"").css('height', len);
  $("#blockdb_"+(a)+"").css('top', posx);
  $("#blockdb_"+(a)+"").css('left', posy);
  $("#blockdb_"+(a)+"").css('position', 'relative');
  $("#blockdb_"+(a)+"").css('color', 'black');
  }

  for (j= 0; j < css_url.length; ++j) {
  b = css_url[j]['id'];
  posx=css_url[j]['position_x'];
  posy=css_url[j]['position_y'];
  wid=css_url[j]['object_breadth'];
  len=css_url[j]['object_length'];
  url=css_url[j]['temp_url']
  $('#slide_'+css_url[j]['s_id']).append("<div class='block' id='blockdb_"+(b)+"' onclick='func($(this));' style='position:absolute;'><img src=''></div>");
  $($('#blockdb_'+(b)).children()).attr("src",url);
  $("#blockdb_"+(b)+"").css('width', wid);
  $("#blockdb_"+(b)+"").css('height', len);
  $("#blockdb_"+(b)+"").css('top', posx);
  $("#blockdb_"+(b)+"").css('left', posy);
  $("#blockdb_"+(b)+"").css('position', 'relative');
  }
  if(project_init==1){
    project_init=0;
    Reveal.slide(0);
  }
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
    project_init=1;
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


var doc = new jsPDF();
var specialElementHandlers = {
    '.reveal': function (element, renderer) {
        return true;
    }
};

function download() {    
    doc.fromHTML($('.reveal').html(), 15, 15, {
        'width': 170,
            'elementHandlers': specialElementHandlers
    });
    doc.save('sample_file.pdf');
};

/*
$(document).ready(function() {

        $("#down").click(function() {

    var pdf = new jsPDF();
    var specialElementHandlers = {
    '.reveal': function (element, renderer) {
        return true;
        }
    };

    pdf.addHTML($('.reveal').first(), function() {
        pdf.save("pre.pdf");
    });
    });
});
*/

function generateImagesForPDF(imagesToCapture, originalPresentationState) {
    // Use the lodash defer method to help with timing issues.
    _.defer(function () {
        var clone = $('.reveal').clone();
        $('.ui.snapshot').html(clone);

        // Grab the HTML from the cloned container.
        var snapshotContainer = $('.ui.snapshot .ui.slides');

        // Grab the canvas that contains the slide.
        html2canvas(snapshotContainer[0]).then(function (canvas) {
            // Convert the canvas to an image and push into the array.
            imagesToCapture.push(canvas.toDataURL('image/jpeg'));

            // Empty out the contents of the container.
            $('.ui.snapshot').empty();

            if (Reveal.isLastSlide()) {
                // If we are done, then send imagesToCapture off to PDF generation and cleanup.
                var exportedPresentation = new jsPDF();
                for (var i = 0; i < imagesToCapture.length; i++) {
                    exportedPresentation.addImage(imagesToCapture[i], 'JPEG', 15, 40, 180, 160);

                    if (i < (imagesToCapture.length - 1)) {
                        exportedPresentation.addPage();
                    }
                }

                exportedPresentation.save('presentation.pdf');
                Reveal.setState(originalPresentationState);
               $("#headerblock").css("display","block");
                $('body').addClass('dimmable');
            }
            else {
                Reveal.next();
                generateImagesForPDF(imagesToCapture, originalPresentationState);
            }
        });
    });
}


function rewindAndBegin() {
    $("#headerblock").css("display","none");
    var originalPresentationState,
        imagesToCapture = [];

    // Save off the original state of the presentation so that we can return there when we are finished.
    originalPresentationState = Reveal.getState();

    // Rewind the presentation back to the start.
    var beginningPresentationState = _.clone(originalPresentationState);
    beginningPresentationState.indexv = 0;
    beginningPresentationState.indexh = 0;
    Reveal.setState(beginningPresentationState);

    $('body').removeClass('dimmable');
    generateImagesForPDF(imagesToCapture, originalPresentationState);
}


