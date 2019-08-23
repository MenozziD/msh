var device_net_list = [];
var user_list = [];

function carica(){
    Handlebars.registerHelper('if_eq', function(a, b, opts) {
        if (a == b) {
            return opts.fn(this);
        } else {
            return opts.inverse(this);
        }
    });
    net('list');
    setTimeout(user_function, 250, 'list');
    $.blockUI.defaults.css.width = '0%';
    $.blockUI.defaults.css.height = '0%';
    $.blockUI.defaults.css.left = '50%';
    $.blockUI.defaults.css.border = '';
    $.blockUI.defaults.message = '<div class="spinner-border text-light" role="status" style=""><span class="sr-only">Loading...</span></div>';
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
    if (type_op.search('update') >=0){
        id = type_op.replace('update','');
        mac = $("#mac" + id).text();
        type_op = 'update';
        for (var i = 0; i < device_net_list.length; i++){
            if (device_net_list[i]['net_mac'] == mac){
                if ($("#type" + id)[0].value != device_net_list[i]['net_type'])
                    type = $("#type" + id)[0].value;
                if ($("#code" + id)[0].value != device_net_list[i]['net_code'])
                    code = $("#code" + id)[0].value;
                if ($("#usr" + id)[0].value != device_net_list[i]['net_usr'])
                    user = $("#usr" + id)[0].value;
                if ($("#psw" + id)[0].value != device_net_list[i]['net_psw'])
                    password = $("#psw" + id)[0].value;
            }
        }
    }
    if (type_op.search('type') >=0){
        id = type_op.replace('type','');
        type_op = 'type';
    }
    if (type_op == 'command'){
        for(var l = 0; l < device_net_list.length; l++) {
            if (device_net_list[l]['net_code'] == $('#device')[0].value)
                type = device_net_list[l]['net_type'];
        }
    }
    if (type_op.search('delete') >= 0){
        id = type_op.replace('delete','');
        type_op = 'delete';
        mac = $("#mac" + id).text();
    }
    if (type_op.search('cmd') >= 0){
        dispositivo = $('#device')[0].value;
        comando = $('#command')[0].value;
        var check_device = $('#chk_device');
        var check_command = $('#chk_command');
        if (device == "")
            check_device.show();
        else
            check_device.hide();
        if (command == "")
            check_command.show();
        else
            check_command.hide();
    }
    if (type_op != 'cmd' || (dispositivo != "" && comando != "")){
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
                        $('#esito')[0].value = json["output"];
                        $('#found')[0].value = json["find_device"];
                        $('#new')[0].value = json["new_device"];
                        $('#update')[0].value = json["updated_device"];
                        net('list');
                    }
                    if (type_op == 'type'){
                        var types = json["types"]
                        var type_template = Handlebars.compile($("#drop_type-template")[0].innerHTML);
                        $('#drop_type' + id).html(type_template(types));
                        for(var i = 0; i < types.length;i++) {
                            $('#drop_type' + id + ' li').click(function() {
                                $('#type' + id).text($(this).text());
                                $("#type" + id).val($(this).text());
                                must_save(id);
                            });
                        }
                    }
                    if (type_op == 'list'){
                        var devices = json["devices"];
                        var device_template = Handlebars.compile($("#table-device-template")[0].innerHTML);
                        $('#table-device').html(device_template(json));
                        device_net_list = [];
                        for(var j = 0; j < devices.length; j++) {
                            device_net_list.push(devices[j]);
                            $('#code' + j).on('input',function(e){must_save(this.id.replace("code", ""))});
                            $('#usr' + j).on('input',function(e){must_save(this.id.replace("usr", ""))});
                            $('#psw' + j).on('input',function(e){must_save(this.id.replace("psw", ""))});
                            if (json['user_role'] != 'ADMIN'){
                                $('#code' + j).prop('readonly', true);
                                $('#type' + j).prop('disabled', true);
                            }
                        }
                    }
                    if (type_op == 'command'){
                        var commands = json["commands"]
                        var command_template = Handlebars.compile($("#drop_command-template")[0].innerHTML);
                        $('#drop_command').html(command_template(commands));
                        for(var k = 0; k < commands.length; k++) {
                            $("#drop_command li").click(function(){
                              $('#command').text($(this).text());
                              $("#command").val($(this).text());
                              $('#chk_command').hide();
                           });
                        }
                    }
                    if (type_op == 'update' || type_op == 'delete'){
                        net('list');
                    }
                    if (type_op == 'cmd'){
                        $('#result')[0].value = json["output"];
                        $('#cmd_result')[0].value = json["result"];
                        net('list');
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

function device_net_code(){
    var template = Handlebars.compile($("#drop_device-template")[0].innerHTML);
    $('#drop_device').html(template(device_net_list));
    for(var i = 0; i < device_net_list.length;i++) {
        $("#drop_device li").click(function(){
          $('#device').text($(this).text());
          $("#device").val($(this).text());
          $('#chk_device').hide();
       });
    }
}

function must_save(id){
    var type = $("#type" + id)[0].value;
    var code = $("#code" + id)[0].value;
    var mac = $("#mac" + id).text();
    var user = $("#usr" + id)[0].value;
    var password = $("#psw" + id)[0].value;
    for (var i = 0; i < device_net_list.length; i++){
        if (device_net_list[i]['net_mac'] == mac){
            if (type != device_net_list[i]['net_type'] || code != device_net_list[i]['net_code'] || user != device_net_list[i]['net_usr'] || password != device_net_list[i]['net_psw']){
                $("#salva" + i).attr("disabled", false);
                $("#reset" + i).attr("disabled", false);
            } else {
                $("#salva" + i).attr("disabled", true);
                $("#reset" + i).attr("disabled", true);
            }
        }
    }
}

function net_reset(id){
    var mac = $("#mac" + id).text();
    for (var i = 0; i < device_net_list.length; i++){
        if (device_net_list[i]['net_mac'] == mac){
            $("#salva" + i).attr("disabled", true);
            $("#reset" + i).attr("disabled", true);
            $("#type" + id)[0].value = device_net_list[i]['net_type'];
            $("#type" + id).text(device_net_list[i]['net_type']);
            $("#code" + id)[0].value = device_net_list[i]['net_code'];
            $("#usr" + id)[0].value = device_net_list[i]['net_usr'];
            $("#psw" + id)[0].value = device_net_list[i]['net_psw'];
        }
    }
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
        role = $("#role_user_add" + id)[0].value;
        var check_username = $('#chk_username');
	    var check_password = $('#chk_password');
	    var check_role = $('#chk_role');
        if (user == "")
            check_username.show();
        else
            check_username.hide();
        if (password == "")
            check_password.show();
        else
            check_password.hide();
        if (role == "")
            check_role.show();
        else
            check_role.hide();
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
                        if (json['user_role'] == 'ADMIN'){
                            $('#add-user')[0].classList.remove("d-none");
                            $('#add-user')[0].classList.add("d-block");
                            $('#upload-arduino')[0].classList.remove("d-none");
                            $('#upload-arduino')[0].classList.add("d-block");
                        }
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
        var check_core = $('#chk_device_arduino');
        var check_tipologia = $('#chk_tipo_arduino');
        if (core == "")
            check_core.show();
        else
            check_core.hide();
        if (tipologia == "")
            check_tipologia.show();
        else
            check_tipologia.hide();
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
                              $('#chk_device_arduino').hide();
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
                              $('#chk_tipo_arduino').hide();
                           });
                        }
                    }
                    if (tipo_op == 'compile'){
                        $('#esito_upload')[0].value = json["output"];
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
                        $('#esito_upload')[0].value = json["output"];
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
                }
            },
            error: function(xhr){
            }
        });
    }
}

function update(){
    $.ajax({
        url: "/api/update_last_version",
        type: 'GET',
        success: function(response){
            var json = $.parseJSON(JSON.stringify(response));
            if (json["output"].search("OK") == 0){
                $.blockUI();
                setTimeout(function () {
                    $.unblockUI();
                    $(window.location).attr('href', '/');
                }, 15000);
            }
        },
        error: function(xhr){
        }
    });
}
