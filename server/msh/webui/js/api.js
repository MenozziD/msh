function net(type_op){
    let type = null;
    let dispositivo = null;
    let comando = null;
    let list_up_device = [];
    if (type_op === 'update'){
        for (let i = 0; i < device_tabella["table"][device_tabella["table_key"]].length; i++){
            if (JSON.stringify(device_tabella["table"][device_tabella["table_key"]][i]) !== JSON.stringify(device_tabella["new_list"][i])){
                let dev = {
                    'net_mac': device_tabella["table"][device_tabella["table_key"]][i]['net_mac']
                };
                if (checkChange(i, 'to_delete', "", device_tabella) !== ""){
                    dev['to_delete'] = true;
                } else {
                    if (checkChange(i, 'net_code', "CODICE", device_tabella) !== "")
                        dev['net_code'] = device_tabella["new_list"][i]['net_code'];
                    if (checkChange(i, 'net_type', "TIPO", device_tabella) !== "")
                        dev['net_type'] = device_tabella["new_list"][i]['net_type'];
                    if (checkChange(i, 'net_usr', "USER SSH", device_tabella) !== "")
                        dev['net_usr'] = device_tabella["new_list"][i]['net_usr'];
                    if (checkChange(i, 'net_psw', "PASSWORD SSH", device_tabella) !== "")
                        dev['net_psw'] = device_tabella["new_list"][i]['net_psw'];
                }
                list_up_device.push(dev);
            }
        }
    }
    if (type_op === "cmd"){
        dispositivo = $('#device_device')[0].value;
        comando = $('#command_device')[0].value;
    }
    let body = {
        "tipo_operazione": type_op
    };
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
            let json = $.parseJSON(JSON.stringify(response));
            if (['scan', 'update', 'cmd', 'command'].indexOf(type_op) >= 0)
                $.unblockUI();
            if (json["output"].search("OK") === 0){
                if (type_op === 'scan'){
                    $('#found')[0].value = json["find_device"];
                    $('#new')[0].value = json["new_device"];
                    $('#update')[0].value = json["updated_device"];
                    net('list');
                }
                if (type_op === 'type'){
                    device_tabella["tipologie"]["types"] = [];
                    for (let i=0; i<json["types"].length; i++)
                        device_tabella["tipologie"]["types"].push(json["types"][i]["type_code"]);
                }
                if (type_op === 'list'){
                    let funzioni_bar_template = Handlebars.compile($("#funzioni-bar-template")[0].innerHTML);
                    $('#funzioni_bar').html(funzioni_bar_template(json));
                    let page_number = Math.floor(json[device_tabella["table_key"]].length / device_tabella["record_per_pagina"]);
                    let resto = json[device_tabella["table_key"]].length % device_tabella["record_per_pagina"];
                    if (resto > 0)
                        page_number = page_number + 1;
                    json['pages'] = page_number;
                    json['current_page'] = 1;
                    device_tabella["tipologie"]["device"] = [];
                    for (let i = 0; i < json[device_tabella["table_key"]].length; i++){
                        json[device_tabella["table_key"]][i]['to_delete'] = false;
                        device_tabella["tipologie"]["device"].push(json[device_tabella["table_key"]][i]['net_code']);
                    }
                    device_tabella["table"] = Object.assign({}, json);
                    device_tabella["new_list"] = $.extend(true, [], device_tabella["table"][device_tabella["table_key"]]);
                    json[device_tabella["table_key"]] = json[device_tabella["table_key"]].slice(0, device_tabella["record_per_pagina"]);
                    createTable(json, device_tabella);
                }
                if (type_op === 'update'){
                    net('list');
                }
                if (type_op === 'cmd'){
                    $('#cmd_result')[0].value = json["result"];
                }
            } else {
                $("#error_modal").modal();
                $('#errore').text(json["output"]);
                if (type_op === 'cmd'){
                    $('#errore_title').text(json["result"]);
                    $('#cmd_result')[0].value = json["result"];
                }
            }
        },
        error: function(xhr){
        }
    });
}

function user(type_op){
    let list_up_user = [];
    if (type_op === 'update'){
        for (let i = 0; i < user_tabella["new_list"].length; i++){
            if (JSON.stringify(user_tabella["table"][user_tabella["table_key"]][i]) !== JSON.stringify(user_tabella["new_list"][i])){
                let usr= {
                    'username': user_tabella["table"][user_tabella["table_key"]][i]['username']
                };
                if (checkChange(i, 'to_delete', "", user_tabella) !== ""){
                    usr['to_delete'] = true;
                } else {
                    if (checkChange(i, 'to_add', "", user_tabella) !== ""){
                        usr['to_add'] = true;
                        usr['password'] = user_tabella["new_list"][i]['password'];
                        usr['role'] = user_tabella["new_list"][i]['role'];
                    } else {
                        if (checkChange(i, 'password', "PASSWORD", user_tabella) !== "")
                            usr['password'] = user_tabella["new_list"][i]['password'];
                        if (checkChange(i, 'role', "RUOLO", user_tabella) !== "")
                            usr['role'] = user_tabella["new_list"][i]['role'];
                    }
                }
                list_up_user.push(usr);
            }
        }
    }
    let body = {
        "tipo_operazione": type_op
    };
    if (list_up_user.length > 0)
        body['list_up_user'] = list_up_user;
    if (['update'].indexOf(type_op) >= 0)
        $.blockUI();
    $.ajax({
        url: "/api/user",
        type: 'POST',
        contentType: "application/json",
        data : JSON.stringify(body),
        success: function(response){
            let json = $.parseJSON(JSON.stringify(response));
            if (['update'].indexOf(type_op) >= 0)
                $.unblockUI();
            if (json["output"].search("OK") === 0){
                if (type_op === 'list'){
                    let page_number = Math.floor(json['users'].length / user_tabella["record_per_pagina"]);
                    let resto = json['users'].length % user_tabella["record_per_pagina"];
                    if (resto > 0)
                        page_number = page_number + 1;
                    json['pages'] = page_number;
                    json['current_page'] = 1;
                    for (let i = 0; i < json[user_tabella["table_key"]].length; i++){
                        json[user_tabella["table_key"]][i]['to_delete'] = false;
                        json[user_tabella["table_key"]][i]['to_add'] = false;
                    }
                    user_tabella["table"] = Object.assign({}, json);
                    user_tabella["new_list"] = $.extend(true, [], user_tabella["table"][user_tabella["table_key"]]);
                    json[user_tabella["table_key"]] = json[user_tabella["table_key"]].slice(0, user_tabella["record_per_pagina"]);
                    createTable(json, user_tabella);
                }
                if (type_op === 'update'){
                    user('list');
                }
            } else {
                $("#error_modal").modal();
                $('#errore').text(json["output"]);
            }
        },
        error: function(xhr){
        }
    });
}

function wifi(type_op){
    let wifi_set = null;
    if (type_op === 'update'){
        for (let i = 0; i < wifi_tabella["new_list"].length; i++){
            if (JSON.stringify(wifi_tabella['table'][wifi_tabella['table_key']][i]) !== JSON.stringify(wifi_tabella["new_list"][i])){
                wifi_set = {
                    'ssid': wifi_tabella['table'][wifi_tabella['table_key']][i]['ssid'],
                    'psw': wifi_tabella['table'][wifi_tabella['table_key']][i]['wpa_psk_key']
                }
            }
        }
    }
    let body = {
        "tipo_operazione": type_op
    };
    if (wifi_set != null)
        body['wifi'] = wifi_set;
    $.blockUI();
    $.ajax({
        url: "/api/wifi",
        type: 'POST',
        contentType: "application/json",
        data : JSON.stringify(body),
        success: function(response){
            let json = $.parseJSON(JSON.stringify(response));
            $.unblockUI();
            if (json["output"].search("OK") === 0){
                if (type_op === 'list'){
                    let page_number = Math.floor(json[wifi_tabella['table_key']].length / wifi_tabella["record_per_pagina"]);
                    let resto = json[wifi_tabella['table_key']].length % wifi_tabella["record_per_pagina"];
                    if (resto > 0)
                        page_number = page_number + 1;
                    json['pages'] = page_number;
                    json['current_page'] = 1;
                    for (let i = 0; i < json[wifi_tabella['table_key']].length; i++){
                        json[wifi_tabella['table_key']][i]['to_set'] = false;
                    }
                    wifi_tabella['table'] = Object.assign({}, json);
                    wifi_tabella["new_list"] = $.extend(true, [], wifi_tabella['table'][wifi_tabella['table_key']]);
                    json[wifi_tabella['table_key']] = json[wifi_tabella['table_key']].slice(0,  wifi_tabella["record_per_pagina"]);
                    createTable(json, wifi_tabella);
                }
                if (type_op === 'update'){
                    wifi('list');
                }
            } else {
                if (json["output"].indexOf("essere eseguita solo da un ADMIN") === -1){
                    $("#error_modal").modal();
                    $('#errore').text(json["output"]);
                }
            }
        },
        error: function(xhr){
        }
    });
}

function upload_arduino(tipo_op){
    let core = null;
    let tipologia = null;
    if (['upload', 'compile', 'compile_upload'].indexOf(tipo_op) >= 0){
        core = $("#device_arduino")[0].value;
        tipologia = $("#tipo_arduino")[0].value;
    }
    let toUpload = false;
    if (tipo_op === 'compile_upload'){
        tipo_op = 'compile';
        toUpload = true;
    }
    let body = {
        "tipo_operazione": tipo_op
    };
    if (core != null)
        body['core'] = core;
    if (tipologia != null)
        body['tipologia'] = tipologia;
    if (['upload', 'compile'].indexOf(tipo_op) >= 0)
        $.blockUI();
    $.ajax({
        url: "/api/upload_arduino",
        type: 'POST',
        contentType: "application/json",
        data : JSON.stringify(body),
        success: function(response){
            let json = $.parseJSON(JSON.stringify(response));
            if (['upload', 'compile'].indexOf(tipo_op) >= 0)
                $.unblockUI();
            if (json["output"].search("OK") === 0){
                if (tipo_op === 'core'){
                    arduino_tabella['tipologie']['device'] = json["cores"]
                }
                if (tipo_op === 'tipo'){
                    arduino_tabella['tipologie']['tipo']  = json["types"]
                }
                if (tipo_op === 'compile'){
                    $('#esito_upload')[0].value = json["result"];
                    $('#program_bytes_used')[0].value = json["compile_output"]["program_bytes_used"];
                    $('#program_percentual_used')[0].value = json["compile_output"]["program_percentual_used"];
                    $('#program_bytes_total')[0].value = json["compile_output"]["program_bytes_total"];
                    $('#memory_bytes_used')[0].value = json["compile_output"]["memory_bytes_used"];
                    $('#memory_percentual_used')[0].value = json["compile_output"]["memory_percentual_used"];
                    $('#memory_bytes_free')[0].value = json["compile_output"]["memory_bytes_free"];
                    $('#memory_bytes_total')[0].value = json["compile_output"]["memory_bytes_total"];
                    if (toUpload)
                        upload_arduino('upload');
                }
                if (tipo_op === 'upload'){
                    $('#esito_upload')[0].value = json["result"];
                    $('#porta_seriale')[0].value = json["upload_output"]["porta_seriale"];
                    $('#chip')[0].value = json["upload_output"]["chip"];
                    $('#mac_addres')[0].value = json["upload_output"]["mac_addres"];
                    $('#byte_write')[0].value = json["upload_output"]["byte_write"];
                    $('#byte_write_compressed')[0].value = json["upload_output"]["byte_write_compressed"];
                    $('#time')[0].value = json["upload_output"]["time"];
                }
            } else {
                $("#error_modal").modal();
                $('#errore').text(json["output"]);
                if (tipo_op === 'upload' || tipo_op === 'compile') {
                    $('#errore_title').text(json["result"]);
                    $('#esito_upload')[0].value = json["result"];
                }
            }
        },
        error: function(xhr){
        }
    });
}

function update(){
    $.blockUI();
    $.ajax({
        url: "/api/update_last_version",
        type: 'GET',
        success: function(response){
            let json = $.parseJSON(JSON.stringify(response));
            if (json["output"].search("OK") === 0){
                setTimeout(function () {
                    $.unblockUI();
                    $(window.location).attr('href', '/');
                }, 15000);
            } else {
                $.unblockUI();
            }
        },
        error: function(xhr){
        }
    });
}

function logout(){
    $.ajax({
        url: "/logout",
        type: 'GET',
        success: function(){
            $(window.location).attr('href', '/');
        },
        error: function(xhr){
        }
    });
}