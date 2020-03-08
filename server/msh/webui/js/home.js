var table_device = {};
var new_device_net_list = [];
var tipologie = [];
var user_list = {};
var last_sort = true;
var page_up = 0;
var page_down = 0;
var page_up_u = 0;
var page_down_u = 0;
var select_all = false;

function carica(){
    Handlebars.registerHelper('if_eq', function(a, b, opts) {
        if (a == b) {
            return opts.fn(this);
        } else {
            return opts.inverse(this);
        }
    });
    Handlebars.registerHelper('if_not_eq', function(a, b, opts) {
        if (a == b) {
            return opts.inverse(this);
        } else {
            return opts.fn(this);
        }
    });
    Handlebars.registerHelper('if_min', function(a, b, c, d, opts) {
        if (a+b <= c) {
            if (d == 'device')
                page_up = page_up + 1;
            else
                page_up_u = page_up_u + 1;
            return opts.fn(this);
        } else {
            return opts.inverse(this);
        }
    });
    Handlebars.registerHelper('if_mag', function(a, b, c, d, opts) {
        if (a-b > 0) {
            if (d == 'device')
                page_down = page_down + 1;
            else
                page_down_u = page_down_u + 1;
            return opts.fn(this);
        } else {
            return opts.inverse(this);
        }
    });
    Handlebars.registerHelper('sum', function(a, b, opts) {
        return a+b;
    });
    Handlebars.registerHelper('dif', function(a, b, opts) {
        return a-b;
    });
    net('list');
    setTimeout(net, 250, 'type');
    setTimeout(user_function, 500, 'list');
    $.blockUI.defaults.css.width = '0%';
    $.blockUI.defaults.css.height = '0%';
    $.blockUI.defaults.css.left = '50%';
    $.blockUI.defaults.css.border = '';
    $.blockUI.defaults.baseZ = 2000;
    $.blockUI.defaults.message = '<div class="spinner-border text-light" role="status" style=""><span class="sr-only">Loading...</span></div>';
 }

function view_drop(id){
    var type_template = Handlebars.compile($("#drop_type-template")[0].innerHTML);
    $('#drop_type' + id).html(type_template(tipologie));
    $('#drop_type' + id + ' li').click(function() {
        $('#type' + id).text($(this).text());
        $("#type" + id).val($(this).text());
        cambioVal(id);
    });
}

function sortTable(attribute){
    // a.data.localeCompare(b.data); crescente
    // b.data.localeCompare(a.data); decrescente
    if (last_sort) {
        table_device['devices'].sort(function(a, b){
            return a[attribute].localeCompare(b[attribute], undefined, {'numeric': true});
        });
    } else {
       table_device['devices'].sort(function(a, b){
            return b[attribute].localeCompare(a[attribute], undefined, {'numeric': true});
        });
    }
    table_device['current_page'] = 1;
    var tmp_list = Object.assign({}, table_device);
    tmp_list['devices'] = tmp_list['devices'].slice(0,8);
    var device_template = Handlebars.compile($("#table-device-template")[0].innerHTML);
    $('#table-device').html(device_template(tmp_list));
    last_sort = !last_sort;
}

function net(type_op){
    var code = null;
    var type = null;
    var mac = null;
    var user = null;
    var password = null;
    var id = null;
    var dispositivo = null;
    var comando = null;
    /*if (type_op.search('update') >=0){
        id = type_op.replace('update','');
        mac = $("#mac" + id).text();
        type_op = 'update';
        for (var i = 0; i < table_device.length; i++){
            if (table_device[i]['net_mac'] == mac){
                if ($("#type" + id)[0].value != table_device[i]['net_type'])
                    type = $("#type" + id)[0].value;
                if ($("#code" + id)[0].value != table_device[i]['net_code'])
                    code = $("#code" + id)[0].value;
                if ($("#usr" + id)[0].value != table_device[i]['net_usr'])
                    user = $("#usr" + id)[0].value;
                if ($("#psw" + id)[0].value != table_device[i]['net_psw'])
                    password = $("#psw" + id)[0].value;
            }
        }
    }*/
    if (type_op.search('type') >=0){
        id = type_op.replace('type','');
        type_op = 'type';
    }
    if (type_op == 'command'){
        for(var l = 0; l < table_device['devices'].length; l++) {
            if (table_device['devices'][l]['net_code'] == $('#device')[0].value){
                type = table_device['devices'][l]['net_type'];
                break;
            }
        }
    }
    if (type_op.search('cmd') >= 0){
        dispositivo = $('#device')[0].value;
        comando = $('#command')[0].value;
    }
    if ( (type_op == 'cmd' && dispositivo != "" && comando != "") || (type_op == 'type' && tipologie.length == 0) || (type_op != 'cmd' && type_op != 'type')){
        var body = {
            "tipo_operazione": type_op
        };
        if (code != null)
            body['codice'] = code
        if (type != null)
            body['tipo'] = type
        if (mac != null)
            body['mac'] = mac
        if (password != null)
            body['password'] = password
        if (user != null)
            body['user'] = user
        if (dispositivo != null)
            body['dispositivo'] = dispositivo
        if (comando != null)
            body['comando'] = comando
        if (type_op.search('scan') >= 0 || type_op.search('cmd') >= 0)
            $.blockUI();
        $.ajax({
            url: "/api/net",
            type: 'POST',
            contentType: "application/json",
            data : JSON.stringify(body),
            success: function(response){
                var json = $.parseJSON(JSON.stringify(response));
                if (type_op == 'scan' || type_op == 'cmd')
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
                        var page_number = Math.floor(json['devices'].length / 8);
                        var resto = json['devices'].length % 8;
                        if (resto > 0)
                            page_number = page_number + 1;
                        json['pages'] = page_number;
                        json['current_page'] = 1;
                        for (i = 0; i < json['devices'].length; i++){
                            json['devices'][i]['to_delete'] = false;
                        }
                        table_device = Object.assign({}, json);
                        new_device_net_list = $.extend(true, [], table_device["devices"]);
                        json['devices'] = json['devices'].slice(0,8);
                        var device_template = Handlebars.compile($("#table-device-template")[0].innerHTML);
                        $('#table-device').html(device_template(json));
                        /*for(var j = 0; j < new_device_net_list.length; j++) {
                            new_device_net_list[j]['to_delete'] = false;
                            $('#code' + j).on('input',function(e){must_save(this.id.replace("code", ""))});
                            $('#usr' + j).on('input',function(e){must_save(this.id.replace("usr", ""))});
                            $('#psw' + j).on('input',function(e){must_save(this.id.replace("psw", ""))});
                            if (json['user_role'] != 'ADMIN'){
                                $('#code' + j).prop('readonly', true);
                                $('#type' + j).prop('disabled', true);
                            }
                        }*/
                    }
                    if (type_op == 'command'){
                        var commands = json["commands"]
                        var command_template = Handlebars.compile($("#drop_command-template")[0].innerHTML);
                        $('#drop_command').html(command_template(commands));
                        for(var k = 0; k < commands.length; k++) {
                            $("#drop_command li").click(function(){
                              $('#command').text($(this).text());
                              $("#command").val($(this).text());
                           });
                        }
                    }
                    if (type_op == 'update' || type_op == 'delete'){
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
}

function selectAllD(){
    var ind = ((table_device['current_page']-1)*8);
    var ind_final = null;
    var value = null;
    if (table_device['current_page'] == table_device['pages'])
        ind_final = table_device['devices'].length;
    else
        ind_final = ind + 8;
    if (! select_all)
        value = true;
    else
        value = false;
    for(var j = ind; j < ind_final; j++)
        new_device_net_list[j]['to_delete'] = value;
    for (var i = 0; i < ind_final - ind; i++)
        $("#checkbox_device" + i).prop("checked", value);
    select_all = value;
}

function change_page(pagina){
    if (pagina >= 1 && pagina <= table_device['pages']) {
        page_up = 0;
        page_down = 0;
        table_device['current_page'] = pagina;
        var tmp_list = Object.assign({}, table_device);
        tmp_list['devices'] = $.extend(true, [], new_device_net_list);
        tmp_list['devices'] = tmp_list['devices'].slice((pagina-1)*8,pagina*8);
        var device_template = Handlebars.compile($("#table-device-template")[0].innerHTML);
        $('#table-device').html(device_template(tmp_list));
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
    console.log(id);
    var ind = ((table_device['current_page']-1)*8) + parseInt(id);
    console.log(ind);
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
}

function device_net_code(){
    var template = Handlebars.compile($("#drop_device-template")[0].innerHTML);
    $('#drop_device').html(template(table_device['devices']));
    for(var i = 0; i < table_device['devices'].length;i++) {
        $("#drop_device li").click(function(){
          $('#device').text($(this).text());
          $("#device").val($(this).text());
       });
    }
}

/*function must_save(id){
    var type = $("#type" + id)[0].value;
    var code = $("#code" + id)[0].value;
    var mac = $("#mac" + id).text();
    var user = $("#usr" + id)[0].value;
    var password = $("#psw" + id)[0].value;
    for (var i = 0; i < table_device.length; i++){
        if (table_device[i]['net_mac'] == mac){
            if (type != table_device[i]['net_type'] || code != table_device[i]['net_code'] || user != table_device[i]['net_usr'] || password != table_device[i]['net_psw']){
                $("#salva" + i).attr("disabled", false);
                $("#reset" + i).attr("disabled", false);
            } else {
                $("#salva" + i).attr("disabled", true);
                $("#reset" + i).attr("disabled", true);
            }
        }
    }
}*/

function net_reset(){
    new_device_net_list = $.extend(true, [], table_device["devices"]);
    var tmp_list = Object.assign({}, table_device);
    tmp_list['devices'] = tmp_list['devices'].slice((table_device['current_page']-1)*8,table_device['current_page']*8);
    var device_template = Handlebars.compile($("#table-device-template")[0].innerHTML);
    $('#table-device').html(device_template(tmp_list));
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

function user_function(type_op){
    var user = null;
    var password = null;
    var role = null;
    var id = null;
    if (type_op.search('update') >= 0){
        id = type_op.replace('update','');
        type_op = 'update';
        user = $("#username" + id).text();
        for (var i = 0; i < user_list.length; i++){
            if (user_list[i]['username'] == user){
                if ($("#psw_user" + id)[0].value != user_list[i]['password'])
                    password = $("#psw_user" + id)[0].value;
                if ($("#role_user" + id)[0].value != user_list[i]['role'])
                    role = $("#role_user" + id)[0].value;
            }
        }
    }
    if (type_op.search('delete') >= 0){
        id = type_op.replace('delete','');
        type_op = 'delete';
        user = $("#username" + id).text();
    }
    if (type_op == 'add'){
        user = $("#username_add")[0].value;
        password = $("#password_add")[0].value;
        role = $("#role_user_add")[0].value;
    }
    if (type_op != 'add' || (user != "" && password != "" && role != "")){
        var body = {
            "tipo_operazione": type_op
        };
        if (role != null)
            body['role'] = role
        if (user != null)
            body['username'] = user
        if (password != null)
            body['password'] = password
        $.ajax({
            url: "/api/user",
            type: 'POST',
            contentType: "application/json",
            data : JSON.stringify(body),
            success: function(response){
                var json = $.parseJSON(JSON.stringify(response));
                if (json["output"].search("OK") == 0){
                    if (type_op == 'list'){
                        var users = json["users"];
                        var user_template = Handlebars.compile($("#table-user-template")[0].innerHTML);
                        $('#table-user').html(user_template(json));
                        user_list = [];
                        for(var i = 0; i < users.length;i++) {
                            user_list.push(users[i]);
                            $('#psw_user' + i).on('input',function(e){must_save_user(this.id.replace("psw_user", ""))});
                            if (json['user_username'] != users[i].username)
                                $('#psw_user' + i).prop('readonly', true);
                            if (json['user_role'] != 'ADMIN'){
                                $('#role_user' + i).prop('disabled', true);
                            }
                        }
                    }
                    if (type_op == 'update' || type_op == 'delete' || type_op == 'add'){
                        user_function('list');
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
}

function must_save_user(id){
    var user = $("#username" + id).text();
    var password = $("#psw_user" + id)[0].value;
    var role = $("#role_user" + id)[0].value;
    for (var i = 0; i < user_list.length; i++){
        if (user_list[i]['username'] == user){
            if (password != user_list[i]['password'] || role != user_list[i]['role']){
                $("#salva_user" + i).attr("disabled", false);
                $("#reset_user" + i).attr("disabled", false);
            } else {
                $("#salva_user" + i).attr("disabled", true);
                $("#reset_user" + i).attr("disabled", true);
            }
        }
    }
}

function view_password_user(i){
    var input_text = $("#psw_user" + i)[0];
    var icon = $("#psw_icon_user" + i)[0];
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

function user_reset(id){
    var username = $("#username" + id).text();
    for (var i = 0; i < user_list.length; i++){
        if (user_list[i]['username'] == username){
            $("#salva_user" + i).attr("disabled", true);
            $("#reset_user" + i).attr("disabled", true);
            $("#psw_user" + id)[0].value = user_list[i]['password'];
            $("#role_user" + id)[0].value = user_list[i]['role'];
            $("#role_user" + id).text(user_list[i]['role']);
            console.log(user_list[i]['role']);
        }
    }
}

function user_role(id, text){
    if (id != "add"){
        $('#role_user' + id).text(text);
        $("#role_user" + id).val(text);
        must_save_user(id);
    } else {
        $('#role_user_add').text(text);
        $("#role_user_add").val(text);
    }
}

function logout(){
    $.ajax({
        url: "/logout",
        type: 'GET',
        success: function(response){
            $(window.location).attr('href', '/');
        },
        error: function(xhr){
        }
    });
}

function upload_arduino(tipo_op){
    var core = null;
    var tipologia = null;
    if (['upload', 'compile', 'compile_upload'].indexOf(tipo_op) >= 0){
        core = $("#device_arduino")[0].value;
        tipologia = $("#tipo_arduino")[0].value;
    }
    if (['upload', 'compile', 'compile_upload'].indexOf(tipo_op) < 0 || (core != "" && tipologia != "")){
        var toUpload = false;
        if (tipo_op == 'compile_upload'){
            tipo_op = 'compile';
            toUpload = true;
        }
        var body = {
            "tipo_operazione": tipo_op
        };
        if (core != null)
            body['core'] = core
        if (tipologia != null)
            body['tipologia'] = tipologia
        if (['upload', 'compile'].indexOf(tipo_op) >= 0)
            $.blockUI();
        $.ajax({
            url: "/api/upload_arduino",
            type: 'POST',
            contentType: "application/json",
            data : JSON.stringify(body),
            success: function(response){
                var json = $.parseJSON(JSON.stringify(response));
                if (['upload', 'compile'].indexOf(tipo_op) >= 0)
                    $.unblockUI();
                if (json["output"].search("OK") == 0){
                    if (tipo_op == 'core'){
                        var cores = json["cores"]
                        var device_template = Handlebars.compile($("#drop_device_arduino-template")[0].innerHTML);
                        $('#drop_device_arduino').html(device_template(cores));
                        for(var i = 0; i < cores.length; i++) {
                            $("#drop_device_arduino li").click(function(){
                              $('#device_arduino').text($(this).text());
                              $("#device_arduino").val($(this).text());
                           });
                        }
                    }
                    if (tipo_op == 'tipo'){
                        var types = json["types"]
                        var tipo_template = Handlebars.compile($("#drop_tipo_arduino-template")[0].innerHTML);
                        $('#drop_tipo_arduino').html(tipo_template(types));
                        for(var j = 0; j < types.length; j++) {
                            $("#drop_tipo_arduino li").click(function(){
                              $('#tipo_arduino').text($(this).text());
                              $("#tipo_arduino").val($(this).text());
                           });
                        }
                    }
                    if (tipo_op == 'compile'){
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
                    if (tipo_op == 'upload'){
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
                    if (tipo_op == 'upload' || tipo_op == 'compile') {
                        $('#errore_title').text(json["result"]);
                        $('#esito_upload')[0].value = json["result"];
                    }
                }
            },
            error: function(xhr){
            }
        });
    }
}

function update(){
    $.blockUI();
    $.ajax({
        url: "/api/update_last_version",
        type: 'GET',
        success: function(response){
            var json = $.parseJSON(JSON.stringify(response));
            if (json["output"].search("OK") == 0){
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
