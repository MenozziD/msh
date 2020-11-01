function generateString(struct_tabella, mex_tipe, indice){
    let mex = struct_tabella[mex_tipe]['static'];
    for (let i=0; i < struct_tabella[mex_tipe]['param'].length; i++)
        mex = mex.replace("%" + (i+1), eval(struct_tabella[mex_tipe]['param'][i]));
    return mex;
}

function abilButton(struct_tabella){
    if (JSON.stringify(struct_tabella['table'][struct_tabella['table_key']]) !== JSON.stringify(struct_tabella['new_list']))
        $('#' + struct_tabella['id'] + '-alert').removeClass("d-none");
    else
        $('#' + struct_tabella['id'] + '-alert').addClass("d-none");
}

function createTable(struttura, struct_tabella){
    let template = Handlebars.compile($('#table-' + struct_tabella['id'] + '-template')[0].innerHTML);
    $('#table-' + struct_tabella['id']).html(template(struttura));
    $('[data-toggle="tooltip"]').tooltip({html: true});
    let colonna_tabella = $("#colonna-table-" + struct_tabella['id']);
    if ( ! (typeof colonna_tabella === "undefined")) {
        let h_col = ((colonna_tabella[0].rows[1].offsetHeight + 3) * struct_tabella['record_per_pagina']) + colonna_tabella[0].rows[0].offsetHeight + 2;
        colonna_tabella.css({'height': h_col});
        if (struct_tabella['id'] === "user") {
            let cw = parseInt($(".custom-control-input").height()) + 3;
            let button = $('.button-del-add');
            button.css('width', cw + 'px');
            button.css('height', cw + 'px');
        }
    }
     abilButton(struct_tabella);
}

function sortTable(attribute, struct_tabella){
    // a.data.localeCompare(b.data); crescente
    // b.data.localeCompare(a.data); decrescente
    if (struct_tabella['last_sort']) {
        struct_tabella['new_list'].sort(function(a, b){
            return a[attribute].localeCompare(b[attribute], undefined, {'numeric': true});
        });
    } else {
       struct_tabella['new_list'].sort(function(a, b){
            return b[attribute].localeCompare(a[attribute], undefined, {'numeric': true});
        });
    }
    let tmp = [];
    for (let i=0; i < struct_tabella['new_list'].length; i++){
        for (let j=0; j < struct_tabella['new_list'].length; j++){
            if (struct_tabella['new_list'][i][struct_tabella['primary_key']] === struct_tabella['table'][struct_tabella['table_key']][j][struct_tabella['primary_key']]){
                tmp.push(struct_tabella['table'][struct_tabella['table_key']][j]);
                break;
            }
        }
    }
    struct_tabella['table'][struct_tabella['table_key']] = $.extend(true, [], tmp);
    struct_tabella['table']['current_page'] = 1;
    let tmp_list = Object.assign({}, struct_tabella['table']);
    tmp_list[struct_tabella['table_key']] = $.extend(true, [], struct_tabella['new_list']);
    tmp_list[struct_tabella['table_key']] = tmp_list[struct_tabella['table_key']].slice(0, struct_tabella['record_per_pagina']);
    createTable(tmp_list, struct_tabella);
    struct_tabella['last_sort'] = !struct_tabella['last_sort'];
}

function checkChange(ind, editable_obj, struct_tabella){
    let mex = "";
    if (editable_obj['key'] === 'net_config') {
        if (struct_tabella['new_list'][ind][editable_obj['key']][editable_obj['name']] !== struct_tabella['table'][struct_tabella['table_key']][ind][editable_obj['key']][editable_obj['name']]) {
            mex = "\t# Cambiato il " + editable_obj['name'] + " da " + struct_tabella['table'][struct_tabella['table_key']][ind][editable_obj['key']][editable_obj['name']] + " a " + struct_tabella['new_list'][ind][editable_obj['key']][editable_obj['name']] + "\n";
        }
    } else {
        if (struct_tabella['table'][struct_tabella['table_key']][ind][editable_obj['key']] !== struct_tabella['new_list'][ind][editable_obj['key']])
            mex = "\t# Cambiato il " + editable_obj['name'] + " da " + struct_tabella['table'][struct_tabella['table_key']][ind][editable_obj['key']] + " a " + struct_tabella['new_list'][ind][editable_obj['key']] + "\n";
    }
    return mex;
}

function getRiepilogo(struct_tabella) {
    let message = "";
    struct_tabella['to_update'] = [];
    for (let i = 0; i < struct_tabella['table'][struct_tabella['table_key']].length; i++){
        if (JSON.stringify(struct_tabella['table'][struct_tabella['table_key']][i]) !== JSON.stringify(struct_tabella['new_list'][i])){
            let found = false;
            let element = {};
            element[struct_tabella['primary_key']] = struct_tabella["table"][struct_tabella["table_key"]][i][struct_tabella['primary_key']];
            if (checkChange(i, {'key':'to_delete', 'name': ''}, struct_tabella) !== "" && ! found) {
                message = message + generateString(struct_tabella, "mex_del", i);
                element['to_delete'] = true;
                found = true;
            }
            if (checkChange(i, {'key':'to_set', 'name': ''}, struct_tabella) !== "" && ! found){
                message = message + generateString(struct_tabella, "mex_set", i);
                element['to_set'] = true;
                found = true;
            }
            if (checkChange(i, {'key':'to_add', 'name': ''}, struct_tabella) !== "" && ! found){
                message = message + generateString(struct_tabella, "mex_add", i);
                found = true;
                element['to_add'] = true;
            }
            if (! found){
                message = message + generateString(struct_tabella, "mex_up", i);
                let editables = getEditables(i, struct_tabella)
                for (let j=0; j < editables.length; j++) {
                    let mex = checkChange(i, editables[j], struct_tabella)
                    if (mex !== "") {
                        message = message + mex;
                        if (editables[j]['key'] === 'net_config'){
                            if (element[editables[j]['key']] === undefined)
                               element[editables[j]['key']] = {};
                            element[editables[j]['key']][editables[j]['name']] = struct_tabella['new_list'][i][editables[j]['key']][editables[j]['name']];
                        } else
                            element[editables[j]['key']] = struct_tabella['new_list'][i][editables[j]['key']];
                    }
                }
            }
            message = message + "\n"
            struct_tabella['to_update'].push(element);
        }
    }
    $('#recap_' + struct_tabella['id']).text(message);
    $('#modal_recap_change_' + struct_tabella['id']).modal();
}

function getEditables(ind, struct_tabella) {
    let editables = [];
    for (let i=0; i<struct_tabella['new_list'][ind]['net_config_keys'].length; i++) {
        let element = struct_tabella['new_list'][ind]['net_config_keys'][i];
        let editable = {
            'key': 'net_config',
            'name': element,
            'id_frontend': element
        };
        editables.push(editable);
    }
    for (let i=0; i < struct_tabella["editable"].length; i++)
        editables.push(struct_tabella["editable"][i]);
    return editables;
}

function cambioVal(ind, struct_tabella, key){
    let editables = getEditables(ind, struct_tabella);
    let found = false;
    let i, name;
    if (key.includes(":")){
        let params = key.split(":");
        key = params[0];
        name = params[1];
    }
    for (i=0; i < editables.length && !found; i++) {
        if (key === 'net_config'){
            if (editables[i]['key'] === key && editables[i]['name'] === name)
                found = true;
        } else {
            if (editables[i]['key'] === key)
                found = true;
        }
    }
    i = i -1;
    let new_value = $('#' + editables[i]["id_frontend"])[0].value;
    if (key !== 'net_config' && struct_tabella['new_list'][ind][key] !== new_value) {
        struct_tabella['new_list'][ind][key] = new_value;
        if (key === 'net_type') {
            let found = false;
            let j;
            for (j = 0; j < device_types.length && !found; j++) {
                if (device_types[j]['type_code'] === struct_tabella['new_list'][ind][key])
                    found = true;
            }
            j = j - 1;
            let net_config = {};
            let net_config_keys = [];
            for (let key_config in device_types[j]['type_config']) {
                net_config[key_config] = device_types[j]['type_config'][key_config]['desc'];
                net_config_keys.push(key_config);
            }
            struct_tabella['new_list'][ind]['net_config_keys'] = net_config_keys;
            struct_tabella['new_list'][ind]['net_config'] = Object.assign({}, net_config);
            carica_detail(ind);
        }
    } else {
        if (Object.keys(struct_tabella['new_list'][ind][key]).length > 0 && struct_tabella['new_list'][ind][key][editables[i]['name']] !== new_value) {
            console.log(key);
            console.log(ind);
            console.log(editables[i]['name']);
            struct_tabella['new_list'][ind][key][editables[i]['name']] = new_value;
        }
    }
    if (struct_tabella['checkbox_action'] === "to_set"){
        for (let i=0; i < struct_tabella['new_list'].length; i++){
            if (i !== ind)
                struct_tabella['new_list'][i]['to_set'] = false;
        }
        for (let i=0; i < struct_tabella["record_per_pagina"]; i++){
            if (i !== id)
                $("#checkbox_" + struct_tabella['id'] + i).prop("checked", false);
        }
    }
    abilButton(struct_tabella);
}

function setDelete(ind, struct_tabella){
    struct_tabella['new_list'][ind]['to_delete'] = true;
    abilButton(struct_tabella);
}

function reset(struct_tabella){
    for (let i = struct_tabella['new_list'].length; i--;){
        if (struct_tabella['new_list'][i]['to_add'] === true){
            struct_tabella['table'][struct_tabella['table_key']].splice(i, 1);
        }
    }
    let page_number = Math.floor(struct_tabella['table'][struct_tabella['table_key']].length / struct_tabella["record_per_pagina"]);
    let resto = struct_tabella['table'][struct_tabella['table_key']].length % struct_tabella["record_per_pagina"];
    if (resto > 0)
        page_number = page_number + 1;
    struct_tabella['table']['current_page'] = 1;
    struct_tabella['table']['pages'] = page_number;
    struct_tabella["new_list"] = $.extend(true, [], struct_tabella['table'][struct_tabella['table_key']]);
    let tmp_list = Object.assign({}, struct_tabella['table']);
    tmp_list[struct_tabella['table_key']] = tmp_list[struct_tabella['table_key']].slice((struct_tabella['table']['current_page']-1)*struct_tabella["record_per_pagina"], struct_tabella['table']['current_page']*struct_tabella["record_per_pagina"]);
    struct_tabella['to_update'] = [];
    createTable(tmp_list, struct_tabella);
    $('#detail-device').addClass('d-none');
}

function changePage(pagina, struct_tabella){
    if (pagina >= 1 && pagina <= struct_tabella['table']['pages']) {
        struct_tabella['page_up'] = 0;
        struct_tabella['page_down'] = 0;
        struct_tabella['table']['current_page'] = pagina;
        let tmp_list = Object.assign({}, struct_tabella['table']);
        tmp_list[struct_tabella['table_key']] = $.extend(true, [], struct_tabella["new_list"]);
        tmp_list[struct_tabella['table_key']] = tmp_list[struct_tabella['table_key']].slice((pagina-1)*struct_tabella["record_per_pagina"], pagina*struct_tabella["record_per_pagina"]);
        createTable(tmp_list, struct_tabella);
        struct_tabella['select_all'] = false;
        if (struct_tabella['page_down']+struct_tabella['page_up'] > 4){
            if (struct_tabella['page_up']+struct_tabella['page_down'] === 6 || struct_tabella['page_up']+struct_tabella['page_down'] === 7 || struct_tabella['page_up']+struct_tabella['page_down'] === 8){
                for (let i=struct_tabella['page_up']; i > 2; i--){
                    $("#" + struct_tabella['id_char'] + (pagina+i))[0].classList.add("d-none");
                }
                for (let i=struct_tabella['page_down']; i > 2; i--){
                    $("#" + struct_tabella['id_char'] + (pagina-i))[0].classList.add("d-none");
                }
            }
            if (struct_tabella['page_up']+struct_tabella['page_down'] === 5){
                if (struct_tabella['page_up'] === 4){
                   $("#" + struct_tabella['id_char'] + (pagina+struct_tabella['page_up']))[0].classList.add("d-none");
                }
                if (struct_tabella['page_down'] === 4){
                   $("#" + struct_tabella['id_char'] + (pagina-struct_tabella['page_down']))[0].classList.add("d-none");
                }
            }
        }
    }
}


function selectAll(struct_tabella){
    let ind = ((struct_tabella['table']['current_page']-1)*struct_tabella['record_per_pagina']);
    let ind_final;
    let value;
    if (struct_tabella['table']['current_page'] === struct_tabella['table']['pages'])
        ind_final = struct_tabella['table'][struct_tabella['table_key']].length;
    else
        ind_final = ind + struct_tabella['record_per_pagina'];
    value = !struct_tabella["select_all"];
    for (let i = 0; i < ind_final - ind; i++) {
        if (! struct_tabella['new_list'][ind + i]['to_add'])
            $("#checkbox_" + struct_tabella["id"] + i).prop("checked", value);
        cambioVal(i, struct_tabella);
    }
    struct_tabella["select_all"] = value;
}

function viewPassword(i, struct_tabella){
    let input_text = $("#psw_" + struct_tabella["id"] + i)[0];
    let icon = $("#psw_icon_" + struct_tabella["id"] + i)[0];
    if (input_text.type === 'text'){
        input_text.type = 'password';
        icon.classList.remove("fa-eye");
        icon.classList.add("fa-eye-slash");
    } else {
        input_text.type = 'text';
        icon.classList.remove("fa-eye-slash");
        icon.classList.add("fa-eye");
    }
}

function checkExists(valore, struct_tabella){
    let trovato = false;
    for (let i = 0; i < struct_tabella["new_list"].length; i++){
        if (struct_tabella["new_list"][i][struct_tabella['primary_key']] === valore){
            trovato = true;
            break;
        }
    }
    return trovato;
}

function clearAdd(struct_tabella){
    for (let i=0; i<struct_tabella['field_add'].length; i++) {
        let element = $("#" + struct_tabella['field_add'][i]['id_frontend']);
        element.val("");
        element.text("");
    }
    eval(struct_tabella["method_add"]);
}

function addElement(struct_tabella){
    let add = {
        'to_delete': false,
        'to_add': true
    };
    for (let i=0; i<struct_tabella['field_add'].length; i++)
        add[struct_tabella['field_add'][i]['key']] = $("#" + struct_tabella['field_add'][i]['id_frontend'])[0].value;
    struct_tabella["new_list"].push(add);
    let add_new = $.extend(true, {}, add);
    add_new['to_add'] = false;
    struct_tabella['table'][struct_tabella['table_key']].push(add_new);
    $('#modal_add_' + struct_tabella['id']).modal('toggle');
    clearAdd(struct_tabella);
    let page_number = Math.floor(struct_tabella['table'][struct_tabella['table_key']].length / struct_tabella['record_per_pagina']);
    let resto = struct_tabella['table'][struct_tabella['table_key']].length % struct_tabella['record_per_pagina'];
    if (resto > 0)
        page_number = page_number + 1;
    if (struct_tabella['table']['pages'] < page_number)
        struct_tabella['table']['current_page'] = page_number;
    struct_tabella['table']['pages'] = page_number;
    let tmp_list = Object.assign({}, struct_tabella['table']);
    tmp_list[struct_tabella['table_key']] = $.extend(true, [], struct_tabella['new_list']);
    tmp_list[struct_tabella['table_key']] = tmp_list[struct_tabella['table_key']].slice((struct_tabella['table']['current_page']-1)*struct_tabella['record_per_pagina'], struct_tabella['table']['current_page']*struct_tabella['record_per_pagina']);
    createTable(tmp_list, struct_tabella);
}

function removeElement(ind, struct_tabella){
    struct_tabella['new_list'].splice(((struct_tabella['table']['current_page']-1)*struct_tabella['record_per_pagina']) + ind, 1);
    struct_tabella['table'][struct_tabella['table_key']].splice(((struct_tabella['table']['current_page']-1)*struct_tabella['record_per_pagina']) + ind, 1);
    let page_number = Math.floor(struct_tabella['table'][struct_tabella['table_key']].length / struct_tabella['record_per_pagina']);
    let resto = struct_tabella['table'][struct_tabella['table_key']].length % struct_tabella['record_per_pagina'];
    if (resto > 0)
        page_number = page_number + 1;
    struct_tabella['table']['pages'] = page_number;
    if (struct_tabella['table']['current_page'] > page_number)
        struct_tabella['table']['current_page'] = page_number;
    let tmp_list = Object.assign({}, struct_tabella['table']);
    tmp_list[struct_tabella['table_key']] = $.extend(true, [], struct_tabella['new_list']);
    tmp_list[struct_tabella['table_key']] = tmp_list[struct_tabella['table_key']].slice((struct_tabella['table']['current_page']-1)*struct_tabella['record_per_pagina'], struct_tabella['table']['current_page']*struct_tabella['record_per_pagina']);
    createTable(tmp_list, struct_tabella);
}