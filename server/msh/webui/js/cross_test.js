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
    Handlebars.registerHelper('if_object', function(a, opts) {
        if (typeof a == "object") {
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
    /*user('list');
    upload_arduino('core');
    upload_arduino('tipo');
    settings('list');*/
    carica_pag('device');
}

function carica_pag(lnk_pag){
    //Disattivo Colorazione Selezionato
    let lista_lnk=['home','set','dev','user','device'];

    for (let i=0;i<lista_lnk.length;i++)
        $('#lnk_'.concat(lista_lnk[i])).attr('class', 'nav-link');

    //Attivo Colorazione Selezionato su Target
    $('#lnk_'.concat(lnk_pag)).attr('class', 'nav-link active');
    if(lnk_pag==='device') {
        net('list');
        $('#table-device').removeClass("d-none");
    }

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

function viewDropCommand() {
    device_tabella["tipologie"]["command"] = [];
    for (let i = 0; i < device_tabella['table'][device_tabella['table_key']].length; i++) {
        if (device_tabella["table"][device_tabella["table_key"]][i]['net_code'] === $('#device_device')[0].value)
            device_tabella["tipologie"]["command"] = device_tabella["table"][device_tabella["table_key"]][i]['commands'];
    }
    viewDrop("", "command", device_tabella, "abilButtonTooltip('invia')");
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

function cambioValSettings(key){
    if (key.search("__") > 0){
        let keys = key.split("__");
        if (keys.length === 2){
            settings_data['new_settings'][keys[0]][keys[1]] = $('#' + settings_data['id'] + "_" + keys[0] + "__" + keys[1])[0].value;
        }
        if (keys.length === 3){
            settings_data['new_settings'][keys[0]][keys[1]][keys[2]] = $('#' + settings_data['id'] + "_" + keys[0] + "__" + keys[1] + "__" + keys[2])[0].value;
        }
    } else {
        settings_data['new_settings'][key] = $('#' + settings_data['id'] + "_" + key)[0].value;
    }
    abilButtonSettings();
}

function abilButtonSettings(){
    let mex = "È necessario modificare almeno un valore per attivare questa funzione";
    if (JSON.stringify(settings_data['settings']) !== JSON.stringify(settings_data['new_settings'])) {
        abilButtonTooltip("reset_" + settings_data['id']);
        abilButtonTooltip("salva_" + settings_data['id']);
    } else {
        disabilButtonTooltip("reset_" + settings_data['id'], mex);
        disabilButtonTooltip("salva_" + settings_data['id'], mex);
    }
}

function resetSettings(){
    settings_data["new_settings"] = $.extend(true, {}, settings_data['settings']);
    createSettings();
}

function createSettings(){
    let template = Handlebars.compile($('#setting-element-template')[0].innerHTML);
    $('#settings-element').html(template(settings_data));
    $('[data-toggle="tooltip"]').tooltip({html: true});
    abilButtonSettings();
}

function checkChangeSettings(key){
    let mex = "";
    if (key.search("__") > 0) {
        let keys = key.split("__");
        if (keys.length === 2) {
            if (settings_data['settings'][keys[0]][keys[1]] !== settings_data['new_settings'][keys[0]][keys[1]]) {
                mex = "\t# Cambiata impostazione " + keys[0] + "." + keys[1] + " da " + settings_data['settings'][keys[0]][keys[1]] + " a " + settings_data['new_settings'][keys[0]][keys[1]] + "\n";
                if (typeof settings_data['diff_settings'][keys[0]] === 'undefined')
                    settings_data['diff_settings'][keys[0]] = {};
                settings_data['diff_settings'][keys[0]][keys[1]] = settings_data['new_settings'][keys[0]][keys[1]];
            }
        }
        if (keys.length === 3) {
            if (settings_data['settings'][keys[0]][keys[1]][keys[2]] !== settings_data['new_settings'][keys[0]][keys[1]][keys[2]]) {
                mex = "\t# Cambiata impostazione " + keys[0] + "." + keys[1] + "." + keys[2] + " da " + settings_data['settings'][keys[0]][keys[1]][keys[2]] + " a " + settings_data['new_settings'][keys[0]][keys[1]][keys[2]] + "\n";
                if (typeof settings_data['diff_settings'][keys[0]] === 'undefined')
                    settings_data['diff_settings'][keys[0]] = {};
                if (typeof settings_data['diff_settings'][keys[0]][keys[1]] === 'undefined')
                    settings_data['diff_settings'][keys[0]][keys[1]] = {};
                settings_data['diff_settings'][keys[0]][keys[1]][keys[2]] = settings_data['new_settings'][keys[0]][keys[1]][keys[2]];
            }
        }
    } else {
        if (settings_data['settings'][key] !== settings_data['new_settings'][key]) {
            mex = "\t# Cambiata impostazione " + key + " da " + settings_data['settings'][key] + " a " + settings_data['new_settings'][key] + "\n";
            settings_data['diff_settings'][key] = settings_data['new_settings'][key];
        }
    }
    return mex;
}

function getRiepilogoSettings(){
    let message = "Modificate impostazioni: \n";
    settings_data['diff_settings'] = {};
    if (JSON.stringify(settings_data['settings']) !== JSON.stringify(settings_data['new_settings'])){
        let keys = Object.keys(settings_data['settings']);
        for (let i=0; i < keys.length; i++) {
            if (typeof settings_data['settings'][keys[i]] == "object"){
                let keys1 = Object.keys(settings_data['settings'][keys[i]]);
                for (let j=0; j < keys1.length; j++) {
                    if (typeof settings_data['settings'][keys[i]][keys1[j]] == "object"){
                        let keys2 = Object.keys(settings_data['settings'][keys[i]][keys1[j]]);
                        for (let k=0; k < keys2.length; k++) {
                            message = message + checkChangeSettings(keys[i] + "__" + keys1[j] + "__" + keys2[k]);
                        }
                    } else {
                        message = message + checkChangeSettings(keys[i] + "__" + keys1[j]);
                    }
                }
            } else {
                message = message + checkChangeSettings(keys[i]);
            }
        }
        message = message + "\n"
    }
    $('#recap_' + settings_data['id']).text(message);
    $('#modal_recap_change_' + settings_data['id']).modal();
}