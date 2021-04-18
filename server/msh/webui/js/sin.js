//Make the DIV element draggagle:
//dragElement(document.getElementById("mydiv"));

//var nodeIndex=0;
let nodes = []

function getRandomInt(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min)) + min; //Il max è escluso e il min è incluso
}

function dragElement(elmnt) {
  let pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
  if (document.getElementById(elmnt.id + "header")) {
    /* if present, the header is where you move the DIV from:*/
    document.getElementById(elmnt.id + "header").onmousedown = dragMouseDown;
  } else {
    /* otherwise, move the DIV from anywhere inside the DIV:*/
    elmnt.onmousedown = dragMouseDown;
  }

  function dragMouseDown(e) {
    e = e || window.event;
    e.preventDefault();
    // get the mouse cursor position at startup:
    pos3 = e.clientX;
    pos4 = e.clientY;
    document.onmouseup = closeDragElement;
    // call a function whenever the cursor moves:
    document.onmousemove = elementDrag;
  }

  function elementDrag(e) {
    e = e || window.event;
    e.preventDefault();
    // calculate the new cursor position:
    pos1 = pos3 - e.clientX;
    pos2 = pos4 - e.clientY;
    pos3 = e.clientX;
    pos4 = e.clientY;
    let new_x = elmnt.offsetLeft - pos1;
    let new_y = elmnt.offsetTop - pos2;
    let element = $("#" + elmnt.id);
    if ( new_x <= (parseInt($("#sinottico").css("width")) - parseFloat(element.css("width"))) && new_x > 0 && new_y >= 0 && new_y <= (screen.height / 2.5) - parseFloat(element.css("height")))  {
      // set the element's new position:
        elmnt.style.left = new_x + "px";
        elmnt.style.top = new_y + "px";
    }
  }

  function closeDragElement() {
    /* stop moving when mouse button is released:*/
    document.onmouseup = null;
    document.onmousemove = null;
  }
}

function allDraggable(){
    for (let i = 0; i < nodes.length; i++){
        if (nodes[i]['draggable'])
            dragElement(document.getElementById("mydiv" + nodes[i]["id"]));
    }
}

function setDrag(index)
{
    if (nodes[index]['draggable'] == false)
        enableDraggable(index);
    else
        disabilDraggable(index);
}

function disabilDraggable(index){
    nodes[index]['draggable'] = false;
    $("#mydiv" + nodes[index]['id'] + "header").prop('onmousedown', null);
    $("#mydiv" + nodes[index]['id'] + "header").css("cursor", "auto");
    $("#icon" + nodes[index]['id']).replaceWith(feather.icons['anchor'].toSvg().replace("2000/svg\"", "2000/svg\" id=\"icon" + nodes[index]['id'] + "\""));
}

function enableDraggable(index){
    nodes[index]['draggable'] = true;
    $("#mydiv" + nodes[index]['id'] + "header").css("cursor", "move");
    $("#icon" + nodes[index]['id']).replaceWith(feather.icons['move'].toSvg().replace("2000/svg\"", "2000/svg\" id=\"icon" + nodes[index]['id'] + "\""));
    dragElement(document.getElementById("mydiv" + nodes[index]['id']));
}

function addNode(){
    let template = Handlebars.compile($('#div-node')[0].innerHTML);
    let nodeIndex=getRandomInt(0, 5000);
    let node = {
        'id': String(nodeIndex),
        'indice': nodes.length,
        'draggable': true
    };
    nodes.push(node);
    $('#sinottico').html($('#sinottico')[0].innerHTML+template(node));
    allDraggable();
    feather.replace();
}