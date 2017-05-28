//var items=1;
//        function AddItem() {
//        if (items<2){
//            div=document.getElementById("items");
//            button=document.getElementById("add");
//            items++;
//            newitem="<textarea name=\"item" + items;
//            newitem+="\" rows=\"2\" cols=\"50\" ></textarea><br>";
//            newnode=document.createElement("span");
//            newnode.innerHTML=newitem;
//            div.insertBefore(newnode, button);
//            }
//        }

//function timer() {
//  var text = document.getElementById('text');
//  text.hidden = false;
//  var obj = document.getElementById('timer_input');
//  obj.innerHTML--;
//
//  if (obj.innerHTML == 0) {
//
//    document.getElementById('timer_inp').style.display = 'none';
//
////    setTimeout(function() {}, 1000); //данная строка для данного примера не играет никакой роли
//  } else {
//    setTimeout(timer, 1000);
//  }
//}




var count=0
function addResidence(id){
//    var count=0
    console.log(count, id)
    if (id==="residence_yes" && count!=0){
        var text = document.getElementById("id_residence")
        text.remove()
        --count
    }else if (id==="residence_not" && count===0){
        var text = document.createElement('textarea');
        text.id = "id_residence";
        text.cols = "40";
        text.rows = "10"
        text.name = "residence";
        residence_js.appendChild(text);
        ++count;
    }
}

