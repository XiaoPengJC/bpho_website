function change_select_btn(input_planet) {
    var select_btn_class, opposite_btn_class, planet_list;
    
    if(input_planet.className == "checkbox inner") {
        select_btn_class = document.getElementsByClassName("select_btn inner");
        opposite_btn_class = document.getElementsByClassName("select_btn outer");
        planet_list = document.getElementsByClassName("checkbox inner");
    } else if(input_planet.className == "checkbox outer") {
        select_btn_class = document.getElementsByClassName("select_btn outer");
        opposite_btn_class = document.getElementsByClassName("select_btn inner");
        planet_list = document.getElementsByClassName("checkbox outer");
    } else {
        select_btn_class = document.getElementsByClassName("select_btn");
        opposite_btn_class = null;
        planet_list = document.getElementsByClassName("checkbox");
    }

    if (input_planet.checked == true) {
        select_btn_class[0].innerHTML = "Deselect All";
        
        if(opposite_btn_class.length != null) {
            opposite_btn_class[0].innerHTML = "Select All";
        }
    } 
    
    // Check if none of the planets are selected, if true, then change the select/deselect all button to select all
    var none_selected = true;
    for (i = 0; i < planet_list.length; i++) {
        if (planet_list[i].checked == true) {
            none_selected = false;
            break;
        }
    }

    if (none_selected == true) {
        select_btn_class[0].innerHTML = "Select All";
    }
    
}

// Deselect the opposite planet type if one of the planet type is selected
function deselect_opposite_planet_type(input_planet) {
    var planet_type = input_planet.className;
    var opposite_planet_type = input_planet.className == "checkbox inner" ? "checkbox outer" : "checkbox inner";
    var planet_list = document.getElementsByClassName(opposite_planet_type);

    for (i = 0; i < planet_list.length; i++) {
        if (planet_list[i].checked == true) {
            planet_list[i].checked = false;
        }
    }
    change_select_btn(input_planet);
}

function select_deselect_all(select_btn) {
    var select_btn_text = select_btn.innerHTML;

    if (select_btn.className == "select_btn inner") {
        var planet_list_class = document.getElementsByClassName("checkbox inner");
    } else if (select_btn.className == "select_btn outer") {
        var planet_list_class = document.getElementsByClassName("checkbox outer");
    } else {
        var planet_list_class = document.getElementsByClassName("checkbox");
    }
    
    if (select_btn_text == "Select All") {
        select_btn.innerHTML = "Deselect All";

        for (i = 0; i < planet_list_class.length; i++) {
            planet_list_class[i].checked = true;
        }

        if(planet_list_class.className != "checkbox") {
            deselect_opposite_planet_type(planet_list_class[0]);
        }

    } else {
        select_btn.innerHTML = "Select All";
        for (i = 0; i < planet_list_class.length; i++) {
            planet_list_class[i].checked = false;
        }

    }
    
}

function limit_planet_inputs(input_planet, limit) {
    var planet_list = document.getElementsByClassName(input_planet.className);
    var count = 0;

    for (i = 0; i < planet_list.length; i++) {
        if (planet_list[i].checked == true) {
            count++;
        }
    }

    if (count > limit) {
        input_planet.checked = false;
    }
}

