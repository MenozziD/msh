var numero_device_pagina = 8;
var page_up = 0;
var page_down = 0;
var table_device = {};
var new_device_net_list = [];
var tipologie = [];
var select_all = false;
var last_sort_device = true;

function view_drop(id){
    var type_template = Handlebars.compile($("#drop_type-template")[0].innerHTML);
    $('#drop_type' + id).html(type_template(tipologie));
    $('#drop_type' + id + ' li').click(function() {
        $('#type' + id).text($(this).text());
        $("#type" + id).val($(this).text());
        cambioVal(id);
    });
}

function createTable(struttura){
    var device_template = Handlebars.compile($("#table-device-template")[0].innerHTML);
    $('#table-device').html(device_template(struttura));
    $('[data-toggle="tooltip"]').tooltip({html: true});
    if ( ! typeof $(".my-table-device") === "undefined"){
        var h_col = ($(".my-table-device")[0].rows[1].offsetHeight * numero_device_pagina) + $(".my-table-device")[0].rows[0].offsetHeight + 2;
        $(".my-table-device").css({'height':h_col});
    }
    abilButton();
}

function sortTable(attribute){
    // a.data.localeCompare(b.data); crescente
    // b.data.localeCompare(a.data); decrescente
    if (last_sort_device) {
        new_device_net_list.sort(function(a, b){
            return a[attribute].localeCompare(b[attribute], undefined, {'numeric': true});
        });
    } else {
       new_device_net_list.sort(function(a, b){
            return b[attribute].localeCompare(a[attribute], undefined, {'numeric': true});
        });
    }
    tmp_dev = []
    for (var i=0; i < new_device_net_list.length; i++){
        for (var j=0; j < new_device_net_list.length; j++){
            if (new_device_net_list[i]['net_mac'] == table_device['devices'][j]['net_mac']){
                tmp_dev.push(table_device['devices'][j]);
                break;
            }
        }
    }
    table_device['devices'] = $.extend(true, [], tmp_dev);
    table_device['current_page'] = 1;
    var tmp_list = Object.assign({}, table_device);
    tmp_list['devices'] = $.extend(true, [], new_device_net_list);
    tmp_list['devices'] = tmp_list['devices'].slice(0, numero_device_pagina);
    createTable(tmp_list);
    last_sort_device = !last_sort_device;
}

function check_change(indice, chiave, nome){
    var mex = "";
    if (table_device['devices'][indice][chiave] != new_device_net_list[indice][chiave])
        mex = "\t# Cambiato il " +  nome + " da " + table_device['devices'][indice][chiave] + " a " + new_device_net_list[indice][chiave] + "\n";
    return mex;
}

function getRiepilogo() {
    var message = "";
    for (var i = 0; i < table_device['devices'].length; i++){
        if (JSON.stringify(table_device['devices'][i]) != JSON.stringify(new_device_net_list[i])){
            if (check_change(i, 'to_delete', "") != ""){
                message = message + "- Il device con MAC address " + table_device['devices'][i]['net_mac'] + " verra eliminato\n";
            } else {
                message = message + "- Modificato device con MAC address " + table_device['devices'][i]['net_mac'] + "\n";
                message = message + check_change(i, 'net_code', "CODICE");
                message = message + check_change(i, 'net_type', "TIPO");
                message = message + check_change(i, 'net_usr', "USER SSH");
                message = message + check_change(i, 'net_psw', "PASSWORD SSH");
            }
            message = message + "\n"
        }
    }
    $('#recap').text(message);
    $('#modal_recap_change').modal();
}

function net(type_op){
    var type = null;
    var dispositivo = null;
    var comando = null;
    var list_up_device = [];
    if (type_op == 'update'){
        for (var i = 0; i < table_device['devices'].length; i++){
            if (JSON.stringify(table_device['devices'][i]) != JSON.stringify(new_device_net_list[i])){
                var dev = {
                    'net_mac': table_device['devices'][i]['net_mac']
                }
                if (check_change(i, 'to_delete', "") != ""){
                    dev['to_delete'] = true;
                } else {
                    if (check_change(i, 'net_code', "CODICE") != "")
                        dev['net_code'] = new_device_net_list[i]['net_code']
                    if (check_change(i, 'net_type', "TIPO") != "")
                        dev['net_type'] = new_device_net_list[i]['net_type']
                    if (check_change(i, 'net_usr', "USER SSH") != "")
                        dev['net_usr'] = new_device_net_list[i]['net_usr']
                    if (check_change(i, 'net_psw', "PASSWORD SSH") != "")
                        dev['net_psw'] = new_device_net_list[i]['net_psw']
                }
                list_up_device.push(dev);
            }
        }
    }
    if (type_op == 'command'){
        for(var l = 0; l < table_device['devices'].length; l++) {
            if (table_device['devices'][l]['net_code'] == $('#device')[0].value){
                type = table_device['devices'][l]['net_type'];
                break;
            }
        }
    }
    if (type_op == "cmd"){
        dispositivo = $('#device')[0].value;
        comando = $('#command')[0].value;
    }
    var body = {
        "tipo_operazione": type_op
    };
    if (type != null)
        body['net_type'] = type;
    if (dispositivo != null)
        body['dispositivo'] = dispositivo;
    if (comando != null)
        body['comando'] = comando;
    if (list_up_device.length > 0)
        body['list_up_device'] = list_up_device;
    if (['scan', 'update', 'cmd', 'command'].indexOf(type_op) >= 0)
        $.blockUI();
    $.ajax({
        url: "/api/net",
        type: 'POST',
        contentType: "application/json",
        data : JSON.stringify(body),
        success: function(response){
            var json = $.parseJSON(JSON.stringify(response));
            if (['scan', 'update', 'cmd', 'command'].indexOf(type_op) >= 0)
                $.unblockUI();
            if (json["output"].search("OK") == 0){
                if (type_op == 'scan'){
                    $('#found')[0].value = json["find_device"];
                    $('#new')[0].value = json["new_device"];
                    $('#update')[0].value = json["updated_device"];
                    net('list');
                }
                if (type_op == 'type'){
                    tipologie = json["types"]
                }
                if (type_op == 'list'){
                    var funzioni_bar_template = Handlebars.compile($("#funzioni-bar-template")[0].innerHTML);
                    $('#funzioni_bar').html(funzioni_bar_template(json));
                    var page_number = Math.floor(json['devices'].length / numero_device_pagina);
                    var resto = json['devices'].length % numero_device_pagina;
                    if (resto > 0)
                        page_number = page_number + 1;
                    json['pages'] = page_number;
                    json['current_page'] = 1;
                    for (i = 0; i < json['devices'].length; i++){
                        json['devices'][i]['to_delete'] = false;
                    }
                    table_device = Object.assign({}, json);
                    new_device_net_list = $.extend(true, [], table_device["devices"]);
                    json['devices'] = json['devices'].slice(0, numero_device_pagina);
                    createTable(json);
                }
                if (type_op == 'command'){
                    console.log("dfsfsd");
                    var commands = json["commands"]
                    var command_template = Handlebars.compile($("#drop_command-template")[0].innerHTML);
                    $('#drop_command').html(command_template(commands));
                    for(var k = 0; k < commands.length; k++) {
                        $("#drop_command li").click(function(){
                          $('#command').text($(this).text());
                          $("#command").val($(this).text());
                          abilButtonTooltip("invia");
                       });
                    }
                }
                if (type_op == 'update'){
                    net('list');
                }
                if (type_op == 'cmd'){
                    $('#cmd_result')[0].value = json["result"];
                }
            } else {
                $("#error_modal").modal();
                $('#errore').text(json["output"]);
                if (type_op == 'cmd'){
                    $('#errore_title').text(json["result"]);
                    $('#cmd_result')[0].value = json["result"];
                }
            }
        },
        error: function(xhr){
        }
    });
}

function selectAllD(){
    var ind = ((table_device['current_page']-1)*numero_device_pagina);
    var ind_final = null;
    var value = null;
    if (table_device['current_page'] == table_device['pages'])
        ind_final = table_device['devices'].length;
    else
        ind_final = ind + numero_device_pagina;
    if (! select_all)
        value = true;
    else
        value = false;
    for (var i = 0; i < ind_final - ind; i++) {
        $("#checkbox_device" + i).prop("checked", value);
        cambioVal(i);
    }
    select_all = value;
}

function abilButton(){
    var mex = "È necessario modificare almeno un valore per attivare questa funzione";
    if (JSON.stringify(table_device['devices']) != JSON.stringify(new_device_net_list)){
        abilButtonTooltip("reset");
        abilButtonTooltip("salva");
    } else {
        disabilButtonTooltip("reset", mex);
        disabilButtonTooltip("salva", mex);
    }
}

function change_page(pagina){
    if (pagina >= 1 && pagina <= table_device['pages']) {
        page_up = 0;
        page_down = 0;
        table_device['current_page'] = pagina;
        var tmp_list = Object.assign({}, table_device);
        tmp_list['devices'] = $.extend(true, [], new_device_net_list);
        tmp_list['devices'] = tmp_list['devices'].slice((pagina-1)*numero_device_pagina, pagina*numero_device_pagina);
        createTable(tmp_list);
        select_all = false;
        if (page_down+page_up > 4){
            if (page_up+page_down == 6 || page_up+page_down == 7 || page_up+page_down == 8){
                for (var i=page_up; i > 2; i--){
                    $("#" + (pagina+i))[0].classList.add("d-none");
                }
                for (var i=page_down; i > 2; i--){
                    $("#" + (pagina-i))[0].classList.add("d-none");
                }
            }
            if (page_up+page_down == 5){
                if (page_up == 4){
                   $("#" + (pagina+page_up))[0].classList.add("d-none");
                }
                if (page_down == 4){
                   $("#" + (pagina-page_down))[0].classList.add("d-none");
                }
            }
        }
    }
}

function cambioVal(id){
    var ind = ((table_device['current_page']-1)*numero_device_pagina) + parseInt(id);
    var type = $("#type" + id)[0].value;
    var code = $("#code" + id)[0].value;
    var user = $("#usr" + id)[0].value;
    var password = $("#psw" + id)[0].value;
    var to_del = $("#checkbox_device" + id).prop("checked");
    new_device_net_list[ind]['net_code'] = code;
    new_device_net_list[ind]['net_usr'] = user;
    new_device_net_list[ind]['net_psw'] = password;
    new_device_net_list[ind]['net_type'] = type;
    new_device_net_list[ind]['to_delete'] = to_del;
    abilButton();
}

function device_net_code(){
    var template = Handlebars.compile($("#drop_device-template")[0].innerHTML);
    $('#drop_device').html(template(table_device['devices']));
    for(var i = 0; i < table_device['devices'].length;i++) {
        $("#drop_device li").click(function(){
          $('#device').text($(this).text());
          $("#device").val($(this).text());
          abilCommand();
       });
    }
}

function abilCommand(){
    var mex = "Campi mancanti: <ul><li>COMANDO</li></ul>";
    disabilButtonTooltip("invia", mex);
    $("#command").val("");
    $("#command").text("");
    abilButtonTooltip("command");
}

function net_reset(){
    new_device_net_list = $.extend(true, [], table_device["devices"]);
    var tmp_list = Object.assign({}, table_device);
    tmp_list['devices'] = tmp_list['devices'].slice((table_device['current_page']-1)*numero_device_pagina, table_device['current_page']*numero_device_pagina);
    createTable(tmp_list);
}

function view_password(i){
    var input_text = $("#psw" + i)[0];
    var icon = $("#psw_icon" + i)[0];
    if (input_text.type == 'text'){
        input_text.type = 'password';
        icon.classList.remove("fa-eye");
        icon.classList.add("fa-eye-slash");
    } else {
        input_text.type = 'text';
        icon.classList.remove("fa-eye-slash");
        icon.classList.add("fa-eye");
    }
}
