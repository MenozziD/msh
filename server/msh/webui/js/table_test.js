function generateString(struct_tabella, mex_tipe, indice){
    let mex = struct_tabella[mex_tipe]['static'];
    for (let i=0; i < struct_tabella[mex_tipe]['param'].length; i++)
        mex = mex.replace("%" + (i+1), eval(struct_tabella[mex_tipe]['param'][i]));
    return mex;
}

function abilButton(struct_tabella){
    let mex = "È necessario modificare almeno un valore per attivare questa funzione";
    if (JSON.stringify(struct_tabella['table'][struct_tabella['table_key']]) !== JSON.stringify(struct_tabella['new_list'])) {
        abilButtonTooltip("reset_" + struct_tabella['id']);
        abilButtonTooltip("salva_" + struct_tabella['id']);
    } else {
        disabilButtonTooltip("reset_" + struct_tabella['id'], mex);
        disabilButtonTooltip("salva_" + struct_tabella['id'], mex);
    }
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

function checkChange(indice, chiave, nome, struct_tabella){
    let mex = "";
    if (struct_tabella['table'][struct_tabella['table_key']][indice][chiave] !== struct_tabella['new_list'][indice][chiave])
        mex = "\t# Cambiato il " +  nome + " da " + struct_tabella['table'][struct_tabella['table_key']][indice][chiave] + " a " + struct_tabella['new_list'][indice][chiave] + "\n";
    return mex;
}

function getRiepilogo(struct_tabella) {
    let message = "";
    for (let i = 0; i < struct_tabella['table'][struct_tabella['table_key']].length; i++){
        if (JSON.stringify(struct_tabella['table'][struct_tabella['table_key']][i]) !== JSON.stringify(struct_tabella['new_list'][i])){
            let found = false;
            if (checkChange(i, 'to_delete', "", struct_tabella) !== "" && ! found) {
                message = message + generateString(struct_tabella, "mex_del", i);
                found = true;
            }
            if (checkChange(i, 'to_set', "", struct_tabella) !== "" && ! found){
                message = message + generateString(struct_tabella, "mex_set", i);
                found = true;
            }
            if (checkChange(i, 'to_add', "", struct_tabella) !== "" && ! found){
                message = message + generateString(struct_tabella, "mex_add", i);
                found = true;
            }
            if (! found){
                message = message + generateString(struct_tabella, "mex_up", i);
                for (let j=0; j < struct_tabella["editable"].length; j++)
                    message = message + checkChange(i, struct_tabella["editable"][j]['key'], struct_tabella["editable"][j]['name'], struct_tabella);
            }
            message = message + "\n"
        }
    }
    $('#recap_' + struct_tabella['id']).text(message);
    $('#modal_recap_change_' + struct_tabella['id']).modal();
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

function cambioVal(id, struct_tabella){
    let ind = ((struct_tabella['table']['current_page']-1)*struct_tabella["record_per_pagina"]) + parseInt(id);
    for (let i=0; i < struct_tabella["editable"].length; i++) {
        let element = struct_tabella["editable"][i];
        struct_tabella['new_list'][ind][element['key']] = $('#' + element["id_frontend"] + id)[0].value;
    }
    struct_tabella['new_list'][ind][struct_tabella['checkbox_action']] = $("#checkbox_" + struct_tabella['id'] + id).prop("checked");
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

function reset(struct_tabella){

/*
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
    createTable(tmp_list, struct_tabella);
 */
    $('#types_device').css('color', 'white');
    $('#detail-device input').each(function() {
        if ( !$(this).is('[readonly]') )
        {
            $(this).css('background-color', 'white');
        }
    });

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