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
var INDEX_ADD = {
                countRes : 0,
                countEdu : 0,
                countExp : 0
};


function addResidence(id){
    console.log(INDEX_ADD.countRes, id);
    if (id==="residence_yes" && INDEX_ADD.countRes!=0){
        var text = document.getElementById("id_residence");
        text.remove();
        --INDEX_ADD.countRes;
    }else if (id==="residence_not" && INDEX_ADD.countRes===0){
        var text = document.createElement('textarea');
        text.id = "id_residence";
        text.cols = "40";
        text.rows = "10";
        text.name = "residence";
        residence_js.appendChild(text);
        ++INDEX_ADD.countRes;
    }
}

function date_assemble(id){
    var birthDay = document.getElementById('birth_day'),
        birthMonth = document.getElementById('birth_month').value,
        birthYear = document.getElementById('birth_year').value;


    console.log(name);
//    console.log(birthDay);
    console.log('Not cleared date: ' ,birthDay.value, birthMonth, birthYear);

    tempDate = new Date(birthYear, birthMonth, birthDay.value);
    if (birthYear!= tempDate.getFullYear() || birthMonth!= tempDate.getMonth() || birthDay.value!=tempDate.getDate()){
        console.log('Autocorrection: ' ,birthDay.value, birthMonth, birthYear);
        birthDay.classList.add("error");
        error.innerHTML = "Неверная дата!!!";
        this.focus();
    } else{
        birthDay.classList.remove("error");
        error.innerHTML = "";
        console.log('Very good');
    }
}


