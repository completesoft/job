
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

function add_quant_children(id){
    var div = document.getElementById('div_quant_children');
    var hid_child = document.getElementById('id_quant_children');
    if (id=='children_yes'){
        div.hidden = false;
    }
    if (id=='children_not'){
        div.hidden = true;
        hid_child.value = '0';
    }
    console.log(hid_child.value)
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
        INDEX_ADD.countEdu+=1;
        var elements = divChild.querySelectorAll('input, textarea, select');
        for (var i = 0; i < elements.length; i++) {
            var input = elements[i];
//            console.log(input.tagName);
            input.name+=INDEX_ADD.countEdu;
            input.id+=INDEX_ADD.countEdu;
            if (input.tagName == 'SELECT'){continue;}
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
        INDEX_ADD.countExp+=1;
//        console.log(INDEX_ADD.countExp);
        var elements = divChild.querySelectorAll('input, textarea, select');
        for (var i = 0; i < elements.length; i++) {
            var input = elements[i];
            input.name+=INDEX_ADD.countExp;
            input.id+=INDEX_ADD.countExp;
            if (input.tagName == 'SELECT'){continue;}
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


function populatedYear(){
    var date = new Date (Date.now())
    var min = 1930,
        max = date.getFullYear(),
        inHTML = "<option value='"+min+"' disabled selected>Год</option>";

    option_birth = document.getElementById('birth_year');
    option_passp = document.getElementById('passp_year');
    option_edu_start_year = document.getElementById('edu_start_year');
    option_edu_end_year = document.getElementById('edu_end_year');
    option_exp_start_year = document.getElementById('exp_start_year');
    option_exp_end_year = document.getElementById('exp_end_year');
    option_start_year = document.getElementById('start_year');


    for (var i = min; i<=max; i++){
            inHTML+="<option value='";
            inHTML+=i;
            inHTML+="'>";
            inHTML+=i;
            inHTML+="</option>";
    }
    option_birth.insertAdjacentHTML('beforeEnd', inHTML);
    option_passp.insertAdjacentHTML('beforeEnd', inHTML);
    option_edu_start_year.insertAdjacentHTML('beforeEnd', inHTML);
    option_edu_end_year.insertAdjacentHTML('beforeEnd', inHTML);
    option_exp_start_year.insertAdjacentHTML('beforeEnd', inHTML);
    option_exp_end_year.insertAdjacentHTML('beforeEnd', inHTML);
    var inHTML_s = "<option value='"+max+"' disabled selected>Год</option>"+"<option value='"+max+"'>"+max+"</option>"+"<option value='"+(max+1)+"'>"+(max+1)+"</option>";
    option_start_year.insertAdjacentHTML('beforeEnd', inHTML_s);
}


document.addEventListener("DOMContentLoaded", ready);
function ready(){
    populatedYear();
   var fMain = document.getElementById('mainForm');
    fMain.addEventListener('keydown', function(event) {
            if(event.keyCode == 13) {
                event.preventDefault();
            }
    });
    var salary_main = document.getElementById('id_salary');
    var salary_exp = document.getElementById('id_exp_salary');
    salary_main.setAttribute("oninput", "valid_salary(this.id)");
    salary_exp.setAttribute("oninput", "valid_salary(this.id)");

}

function valid_salary(id){
    var input = document.getElementById(id);
    var value = input.value;
    var re = /[^0-9]/gi;
    if (re.test(value)){
        value = value.replace(re, '');
        input.value = value;
    }
}