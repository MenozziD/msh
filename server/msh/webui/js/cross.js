function carica(){
    $.blockUI.defaults.css.width = '0%';
    $.blockUI.defaults.css.height = '0%';
    $.blockUI.defaults.css.left = '50%';
    $.blockUI.defaults.css.border = '';
    $.blockUI.defaults.baseZ = 2000;
    $.blockUI.defaults.message = '<div class="spinner-border text-light" role="status" style=""><span class="sr-only">Loading...</span></div>';
    $.blockUI();
    Handlebars.registerHelper('if_eq', function(a, b, opts) {
        if (a === b) {
            return opts.fn(this);
        } else {
            return opts.inverse(this);
        }
    });
    Handlebars.registerHelper('if_not_eq', function(a, b, opts) {
        if (a === b) {
            return opts.inverse(this);
        } else {
            return opts.fn(this);
        }
    });
    Handlebars.registerHelper('if_min', function(a, b, c, d, opts) {
        if (a+b <= c) {
            eval(d)["page_up"] = eval(d)["page_up"] + 1;
            return opts.fn(this);
        } else {
            return opts.inverse(this);
        }
    });
    Handlebars.registerHelper('if_mag', function(a, b, c, d, opts) {
        if (a-b > 0) {
            eval(d)["page_down"] = eval(d)["page_down"] + 1;
            return opts.fn(this);
        } else {
            return opts.inverse(this);
        }
    });
    Handlebars.registerHelper('sum', function(a, b) {
        return a+b;
    });
    Handlebars.registerHelper('dif', function(a, b) {
        return a-b;
    });
    net('list');
    net('type');
    user('list');
    upload_arduino('core');
    upload_arduino('tipo');
    wifi('list');
    let modal_user = $('#modal_user');
    let modal_wifi = $('#modal_wifi');
    modal_user.on('shown.bs.modal', function () {
        let colonna_table_user = $("#colonna-table-user");
        let tooltip_plus_user = $("#tooltip_plus_user");
        let cw = tooltip_plus_user.height();
        tooltip_plus_user.css({'width':cw+'px'});
        if ( ! (typeof colonna_table_user === "undefined")){
            let h_col = (colonna_table_user[0].rows[1].offsetHeight * user_tabella["record_per_pagina"]) + colonna_table_user[0].rows[0].offsetHeight + 2;
            colonna_table_user.css({'height': h_col});
        }
    });
    modal_user.on('hide.bs.modal', function () {
        reset(user_tabella);
    });
    modal_wifi.on('shown.bs.modal', function () {
        let colonna_table_wifi = $("#colonna-table-wifi");
        if ( ! (typeof colonna_table_wifi === "undefined")){
            let h_col = (colonna_table_wifi[0].rows[1].offsetHeight * wifi_tabella["record_per_pagina"]) + colonna_table_wifi[0].rows[0].offsetHeight + 2;
            colonna_table_wifi.css({'height':h_col});
        }
    });
    modal_wifi.on('hide.bs.modal', function () {
        reset(wifi_tabella);
    });
    $('#modal_add_user').on('hide.bs.modal', function () {
        clearAdd(user_tabella);
    });
    $('#modal_search').on('hide.bs.modal', function () {
        let field_list = ['found', 'new', 'update'];
        cleanFields(field_list);
    });
    $('#modal_exec_cmd').on('hide.bs.modal', function () {
        let field_list = ['device_device', 'command_device', 'cmd_result'];
        cleanFields(field_list);
        let mex = "Campi mancanti: <ul><li>DISPOSITIVO</li><li>COMANDO</li></ul>";
        disabilButtonTooltip("invia", mex);
        mex = "Scegliere il DISPOSITIVO";
        disabilButtonTooltip("command_device", mex);
    });
    $('#modal_compile').on('hide.bs.modal', function () {
        let field_list = ['device_arduino', 'tipo_arduino', 'esito_upload', 'program_bytes_used', 'program_percentual_used',
        'program_bytes_total', 'memory_bytes_used', 'memory_percentual_used', 'memory_bytes_free', 'memory_bytes_total',
        'porta_seriale', 'chip', 'mac_addres', 'byte_write', 'byte_write_compressed', 'time'];
        cleanFields(field_list);
        checkActionExecutable();
    });
}

function cleanFields(field_list){
    for (let i=0; i<field_list.length; i++) {
        let element = $("#" + field_list[i]);
        element.val("");
        element.text("");
    }
}

function abilButtonTooltip(name){
    let element = $("#" + name);
    element.prop("disabled", false);
    element.removeAttr("style");
    $("#tooltip_" + name).removeAttr("data-original-title");
}

function disabilButtonTooltip(name, mex){
    let element = $("#" + name);
    element.prop("disabled", true);
    element.attr("style", "pointer-events: none;");
    $("#tooltip_" + name).attr("data-original-title", mex);
}

function viewDrop(id, key, struct_tabella, funzione){
    let template = Handlebars.compile($("#drop-template")[0].innerHTML);
    $('#drop_' + key + "_" + struct_tabella['id'] + id).html(template(struct_tabella["tipologie"][key]));
    $('#drop_' + key + "_" + struct_tabella['id'] + id + ' li').click(function() {
        $('#' + key + "_" + struct_tabella['id'] + id).text($(this).text());
        $("#" + key + "_" + struct_tabella['id'] + id).val($(this).text());
        eval(funzione);
    });
}

function checkCommandExecutable(){
    let mex = "Campi mancanti: <ul><li>COMANDO</li></ul>";
    cleanFields(['command_device', 'cmd_result']);
    disabilButtonTooltip("invia", mex);
    abilButtonTooltip("command_device");
}

function checkUserAdd(){
    let user_set = false;
    let pass_set = false;
    let role_set = false;
    let username = $("#username_add")[0].value;
    let password = $("#password_add")[0].value;
    let ruolo = $("#role_useradd")[0].value;
    let mex = "Campi mancanti: <ul>";
    if (username !== ""){
        if (!checkExists(username, user_tabella))
            user_set = true;
        else
           mex = mex + "<li>USERNAME GIA ESISTENTE</li>";
    } else
        mex = mex + "<li>USERNAME</li>";
    if (password !== ""){
        if (password.length >= 4)
            pass_set = true;
        else
            mex = mex + "<li>PASSWORD MINORE DI 4 CARATTERI</li>";
    } else
        mex = mex + "<li>PASSWORD</li>";
    if (ruolo !== "")
        role_set = true;
    else
        mex = mex + "<li>TIPOLOGIA</li>";
    mex = mex + "</ul>";
    if (user_set && pass_set && role_set)
        abilButtonTooltip("add_user");
    else
        disabilButtonTooltip("add_user", mex);
}

function checkActionExecutable(){
    let core_set = false;
    let script_set = false;
    let core = $("#device_arduino")[0].value;
    let script = $("#tipo_arduino")[0].value;
    let mex = "Campi mancanti: <ul>";
    if (core !== "")
        core_set = true;
    else
        mex = mex + "<li>DISPOSITIVO</li>";
    if (script !== "")
        script_set = true;
    else
        mex = mex + "<li>TIPOLOGIA</li>";
    mex = mex + "</ul>";
    if (core_set && script_set){
        abilButtonTooltip("compila");
        abilButtonTooltip("upload");
        abilButtonTooltip("compila_upload");
    } else {
        disabilButtonTooltip("compila", mex);
        disabilButtonTooltip("upload", mex);
        disabilButtonTooltip("compila_upload", mex);

    }
}