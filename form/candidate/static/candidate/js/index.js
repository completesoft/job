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
    var res = document.getElementById('residenceBool');
    if (id==="residence_yes" && INDEX_ADD.countRes!=0){
        var text = document.getElementById("id_residence");
        text.remove();
        res.checked = true;
        --INDEX_ADD.countRes;
    }else if (id==="residence_not" && INDEX_ADD.countRes===0){
        var text = document.createElement('textarea');
        text.id = "id_residence";
        text.cols = "40";
        text.rows = "10";
        text.name = "residence";
        residence_js.appendChild(text);
        res.checked = false;
        ++INDEX_ADD.countRes;
    }
    console.log(res.checked);
}

function dateEduExp(id){
    rootEl = document.getElementById(id);
    elemEdu = rootEl.parentNode.querySelectorAll('select');
    inpEdu = rootEl.parentNode.querySelector('input');
    tempDate = new Date(elemEdu[2].value, elemEdu[1].value);
    var formatter = new Intl.DateTimeFormat("ru");
    inpEdu.value = formatter.format(tempDate);
}



function addEdu(id){
    if (id==="edu_add"){
        var divParent = document.getElementById("app_edu");
        var sourceNode = document.getElementById("edu_div");
        var divChild = sourceNode.cloneNode(true);
        ++INDEX_ADD.countEdu;
        var elements = divChild.querySelectorAll('input, textarea, select');
        for (var i = 0; i < elements.length; i++) {
            var input = elements[i];
            console.log(input.name);
            input.name+=INDEX_ADD.countEdu;
            input.id+=INDEX_ADD.countEdu;
            if (input.tag == 'select'){continue;}
            input.value = '';
        }
        sourceNode.parentNode.insertBefore(divChild, document.getElementById('edu_js'));
    }
    document.getElementById(id).checked = false;
}

function addExp(id){
    if (id==="exp_add"){
        var divParent = document.getElementById("app_exp");
        var sourceNode = document.getElementById("exp_div");
        var divChild = sourceNode.cloneNode(true);
        ++INDEX_ADD.countExp;
        var elements = divChild.querySelectorAll('input, textarea, select');
        for (var i = 0; i < elements.length; i++) {
            var input = elements[i];
            console.log(input.name);
            input.name+=INDEX_ADD.countEdu;
            input.id+=INDEX_ADD.countEdu;
            if (input.tag == 'select'){continue;}
            input.value = '';
        }
        sourceNode.parentNode.insertBefore(divChild, document.getElementById('exp_js'));
    }
    document.getElementById(id).checked = false;
}



function date_assemble(id){
    var elem = document.getElementById(id);

    switch(elem.name){
        case 'birth':
            var Day = document.getElementById('birth_day');
            var Month = document.getElementById('birth_month');
            var Year = document.getElementById('birth_year');
            var inp = document.getElementById('id_birthday');
            var error = document.getElementById('error_birth');
            break;
        case 'passp':
            var Day = document.getElementById('passp_day');
            var Month = document.getElementById('passp_month');
            var Year = document.getElementById('passp_year');
            var inp = document.getElementById('id_passp_date');
            var error = document.getElementById('error_passp');
            break;
        case 'start_s':
            var Day = document.getElementById('start_day');
            var Month = document.getElementById('start_month');
            var Year = document.getElementById('start_year');
            var inp = document.getElementById('id_start');
            var error = document.getElementById('error_start');
            break;
    }
    tempDate = new Date(Year.value, Month.value, Day.value);
    if (Year.value!= tempDate.getFullYear() || Month.value!= tempDate.getMonth() || Day.value!=tempDate.getDate()){
        console.log('Autocorrection: ' ,Day.value, Month.value, Year.value);
        Day.classList.add("error");
        error.innerHTML = "Неверная дата!!!";
    } else{
        Day.classList.remove("error");
        error.innerHTML = "";
        console.log('Very good');
        var formatter = new Intl.DateTimeFormat("ru");
        inp.value = formatter.format(tempDate);
        console.log(inp.value);
    }
}

function finalyze(){
    document.getElementById('countRes').value = INDEX_ADD.countRes;
    document.getElementById('countEdu').value = INDEX_ADD.countEdu;
    document.getElementById('countExp').value = INDEX_ADD.countExp;
}