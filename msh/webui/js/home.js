var device_net_list = [];
var device_net_commands= [];

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
		$.ajax({
		    url: "/api/net_cmd",
		    type: 'GET',
		    data: {
				d: device,
				c: command
			},
		    success: function(response){
				var json = $.parseJSON(JSON.stringify(response));
				if (json["output"].search(":") > -1){
                    $('#result')[0].value = json["output"].split(": ")[1];
                } else {
                    $('#result')[0].value = json["output"];
                }
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
            if (json["output"].search(":") > -1){
                $('#esito')[0].value = json["output"].split(": ")[1];
            } else {
                $('#esito')[0].value = json["output"];
            }
            $('#found')[0].value = json["find_device"];
            $('#new')[0].value = json["new_device"];
            $('#update')[0].value = json["updated_device"];
        },
        error: function(xhr){
        }
    });
}

function net_device(type_op){
    code = '';
    type = '';
    mac = '';
    if (type_op.search('update') >=0){
        type = $("#type" + type_op.replace('update',''))[0].value;
        code = $("#code" + type_op.replace('update',''))[0].value;
        mac = $("#mac" + type_op.replace('update','')).text();
        type_op = 'update';
    }
    if (type_op == 'command'){
        for(var i = 0; i < device_net_list.length;i++) {
            if (device_net_list[i]['net_code'] == $('#device')[0].value)
                type = device_net_list[i]['net_type'];
        }
    }
    $.ajax({
        url: "/api/net_device",
        type: 'GET',
        data: {
            to: type_op,
            c: code,
            t: type,
            m: mac
        },
        success: function(response){
            var json = $.parseJSON(JSON.stringify(response));
            if (json["output"].search(":") > -1){
                $('#errore').text(json["output"].split(": ")[1]);
            } else {
                $('#errore').text("");
                if (type_op == 'type'){
                    var types = json["types"]
                    console.log(types);
                }
                if (type_op == 'list'){
                    var devices = json["devices"]
                    $("#table tbody").empty();
                    device_net_list = [];
                    for(var i = 0; i < devices.length;i++) {
                        device_net_list.push(devices[i]);
                        $('#table tbody').append('<tr>');
                        $('#table tbody').append('<td><input type="text" id="code' + i + '" value="' + devices[i]['net_code'] + '"></td>');
                        $('#table tbody').append('<td><input type="text" id="type' + i + '" value="' + devices[i]['net_type'] + '"></td>');
                        $('#table tbody').append('<td>' + devices[i]['net_status'] + '</td>');
                        $('#table tbody').append('<td>' + devices[i]['net_ip'] + '</td>');
                        $('#table tbody').append('<td><span id="mac' + i + '">' + devices[i]['net_mac'] + '</span></td>');
                        $('#table tbody').append('<td>' + devices[i]['net_mac_info'] + '</td>');
                        $('#table tbody').append('<td><button class="btn btn-primary btn-lg btn-block" type="button" name=salva"' + i + '" onclick="net_device(\'update' + i + '\')">Salva</button></td>');
                        $('#table tbody').append('</tr>');
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