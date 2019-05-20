var device_net_list = [];
var device_net_commands = [];
var device_net_types = [];

function net_cmd(){
    var form = $('#form')[0];
	var device = $('#device')[0].value;
	var command = $('#command')[0].value;
	var ko = 0;
	form.classList.add('was-validated');
	Array.prototype.filter.call(form, function (element) {
      if (element.checkValidity() == false) {
		  ko++;
        }
    })
	if (ko > 0){
		console.log("Non faccio niente, ci sono dei campi invaldi");
	} else {
	    console.log("Tutto ok, faccio la chiamata");
        var body = {
            "dispositivo": device,
            "comando": command
        };
		$.ajax({
		    url: "/api/net_cmd",
		    type: 'POST',
		    contentType: "application/json",
            data : JSON.stringify(body),
		    success: function(response){
				var json = $.parseJSON(JSON.stringify(response));
				$('#result')[0].value = json["output"];
				net_device('list');
            },
            error: function(xhr){
            }
        });
	}
}

function net_scan(){
    $.ajax({
        url: "/api/net_scan",
        type: 'GET',
        success: function(response){
            var json = $.parseJSON(JSON.stringify(response));
            $('#result')[0].value = json["output"];
            $('#found')[0].value = json["find_device"];
            $('#new')[0].value = json["new_device"];
            $('#update')[0].value = json["updated_device"];
            net_device('list');
        },
        error: function(xhr){
        }
    });
}

function net_device(type_op){
    var code = '';
    var type = '';
    var mac = '';
    var user = '';
    var password = '';
    var id = '';
    if (type_op.search('update') >=0){
        id = type_op.replace('update','');
        type_op = 'update';
        type = $("#type" + id)[0].value;
        code = $("#code" + id)[0].value;
        mac = $("#mac" + id).text();
        user = $("#usr" + id)[0].value;
        password = $("#psw" + id)[0].value;
    }
    if (type_op.search('type') >=0){
        id = type_op.replace('type','');
        type_op = 'type';
    }
    if (type_op == 'command'){
        for(var i = 0; i < device_net_list.length;i++) {
            if (device_net_list[i]['net_code'] == $('#device')[0].value)
                type = device_net_list[i]['net_type'];
        }
    }
    var body = {
        "tipo_operazione": type_op,
        "codice": code,
        "tipo": type,
        "mac": mac,
        "user": user,
        "password": password
    };
    $.ajax({
        url: "/api/net_device",
        type: 'POST',
        contentType: "application/json",
        data : JSON.stringify(body),
        success: function(response){
            var json = $.parseJSON(JSON.stringify(response));
            if (json["output"].search("OK") == 0){
				$('#errore').text("");
                if (type_op == 'type'){
                    var types = json["types"]
                    $("#drop_type" + id).empty();
                    device_net_types = []
                    for(var i = 0; i < types.length;i++) {
                        device_net_types.push(types[i]);
                        $('#drop_type' + id).append('<li class="dropdown-item">' + types[i]['type_code'] + '</li>');
                        $('#drop_type' + id + ' li').click(function(){
                          $('#type' + id).text($(this).text());
                          $("#type" + id).val($(this).text());
                          must_save(id);
                       });
                    }
                }
                if (type_op == 'list'){
                    var devices = json["devices"]
                    $("#table tbody").empty();
                    device_net_list = [];
                    for(var i = 0; i < devices.length;i++) {
                        device_net_list.push(devices[i]);
                        $('#table tbody').append('<tr>');
                        $('#table tbody').append('<td><input class="form-control" style="width: auto" type="text" id="code' + i + '" value="' + devices[i]['net_code'] + '"></td>');
                        $('#table tbody').append('<td><div class="dropdown' + i + '"><button disabled class="btn btn-secondary btn-lg btn-block dropdown-toggle " type="button" data-toggle="dropdown" id="type' + i + '" onclick="net_device(\'type' + i + '\')" value="' + devices[i]['net_type'] + '">' + devices[i]['net_type'] + '</button><ul class="dropdown-menu" id="drop_type' + i + '"></ul></div></td>');
                        $('#table tbody').append('<td>' + devices[i]['net_status'] + '</td>');
                        $('#table tbody').append('<td>' + devices[i]['net_ip'] + '</td>');
                        $('#table tbody').append('<td><span id="mac' + i + '">' + devices[i]['net_mac'] + '</span></td>');
                        $('#table tbody').append('<td>' + devices[i]['net_mac_info'] + '</td>');
                        $('#table tbody').append('<td><input class="form-control" style="width: auto" type="text" id="usr' + i + '" value="' + devices[i]['net_usr'] + '"></td>');
                        $('#table tbody').append('<td ><div class="input-group" style="width: 230px"><input class="form-control" id="psw' + i + '" value="' + devices[i]['net_psw'] + '" type="password"><div class="input-group-append"><button class="btn btn-primary input-group-button" onclick="view_password(' + i + ')"><i id="psw_icon' + i + '" class="fa fa-eye-slash" aria-hidden="true"></i></button></div></div></td>');
                        $('#table tbody').append('<td>' + devices[i]['net_last_update'] + '</td>');
                        $('#table tbody').append('<td><button disabled class="btn btn-primary btn-lg btn-block" type="button" id=salva' + i + ' onclick="net_device(\'update' + i + '\')">Salva</button></td>');
                        $('#table tbody').append('<td><button disabled class="btn btn-primary btn-lg btn-block" type="button" id=reset' + i + ' onclick="net_reset(' + i + ')">Reset</button></td>');
                        $('#table tbody').append('</tr>');
                        $('#code' + i).on('input',function(e){must_save(this.id.replace("code", ""))});
                        $('#usr' + i).on('input',function(e){must_save(this.id.replace("usr", ""))});
                        $('#psw' + i).on('input',function(e){must_save(this.id.replace("psw", ""))});
                    }
                    $('#table')[0].classList.remove('invisible');
                }
                if (type_op == 'command'){
                    var commands = json["commands"]
                    $("#drop_command").empty();
                    device_net_commands = [];
                    for(var i = 0; i < commands.length;i++) {
                        device_net_commands.push(commands[i]);
                        $('#drop_command').append('<li class="dropdown-item">' + commands[i]['cmd_str'] + '</li>');
                        $("#drop_command li").click(function(){
                          $('#command').text($(this).text());
                          $("#command").val($(this).text());
                       });
                    }
                }
                if (type_op == 'update'){
                    net_device('list');
                }
            } else {
                $('#errore').text(json["output"]);
            }
        },
        error: function(xhr){
        }
    });
}

function deviceNetCode(){
    $("#drop_device").empty();
    for(var i = 0; i < device_net_list.length;i++) {
        $('#drop_device').append('<li class="dropdown-item">' + device_net_list[i]['net_code'] + '</li>');
        $("#drop_device li").click(function(){
          $('#device').text($(this).text());
          $("#device").val($(this).text());
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
