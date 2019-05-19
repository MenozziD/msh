function invia(){
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

function scan(){
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

function deviceNetList(){
    $.ajax({
        url: "/api/device_net_list",
        type: 'GET',
        success: function(response){
            var json = $.parseJSON(JSON.stringify(response));
            if (json["output"].search(":") > -1){
                $('#errore').text(json["output"].split(": ")[1]);
            } else {
                $('#errore').text("");
                var devices = json["devices"]
                $("#table tbody").empty();
                for(var i = 0; i < devices.length;i++) {
                    $('#table tbody').append('<tr>');
                    $('#table tbody').append('<td><input type="text" id="code' + i + '" value="' + devices[i]['net_code'] + '"></td>');
                    $('#table tbody').append('<td><input type="text" id="type' + i + '" value="' + devices[i]['net_type'] + '"></td>');
                    $('#table tbody').append('<td>' + devices[i]['net_status'] + '</td>');
                    $('#table tbody').append('<td>' + devices[i]['net_ip'] + '</td>');
                    $('#table tbody').append('<td><span id="mac' + i + '">' + devices[i]['net_mac'] + '</span></td>');
                    $('#table tbody').append('<td>' + devices[i]['net_mac_info'] + '</td>');
                    $('#table tbody').append('<td><button class="btn btn-primary btn-lg btn-block" type="button" name=salva"' + i + '" onclick="deviceNetUpdate(' + i + ')">Salva</button></td>');
                    $('#table tbody').append('</tr>');
                }
                $('#table')[0].classList.remove('invisible');
            }
        },
        error: function(xhr){
        }
    });
}

function deviceNetCode(){
    $.ajax({
        url: "/api/device_net_list",
        type: 'GET',
        success: function(response){
            var json = $.parseJSON(JSON.stringify(response));
            if (json["output"].search(":") > -1){
                $('#errore').text(json["output"].split(": ")[1]);
            } else {
                var devices = json["devices"]
                $("#drop_device").empty();
                for(var i = 0; i < devices.length;i++) {
                    $('#drop_device').append('<li class="dropdown-item">' + devices[i]['net_code'] + '</li>');
                    $("#drop_device li").click(function(){
                      $('#device').text($(this).text());
                      $("#device").val($(this).text());
                   });
                }
            }
        },
        error: function(xhr){
        }
    });
}

function deviceNetCommand(){
     $.ajax({
        url: "/api/device_net_list",
        type: 'GET',
        success: function(response){
            var json = $.parseJSON(JSON.stringify(response));
            if (json["output"].search(":") > -1){
                $('#errore').text(json["output"].split(": ")[1]);
            } else {
                var devices = json["devices"]
                $("#drop_device").empty();
                for(var i = 0; i < devices.length;i++) {
                    if (devices[i]['net_code'] == $('#device')[0].value){
                        $.ajax({
                            url: "/api/device_net_command",
                            type: 'GET',
                            data: {
                                d: devices[i]['net_type']
                            },
                            success: function(response){
                                var json = $.parseJSON(JSON.stringify(response));
                                if (json["output"].search(":") > -1){
                                    $('#errore').text(json["output"].split(": ")[1]);
                                } else {
                                    var commands = json["commands"]
                                    $("#drop_command").empty();
                                    for(var i = 0; i < commands.length;i++) {
                                        $('#drop_command').append('<li class="dropdown-item">' + commands[i]['cmd_str'] + '</li>');
                                        $("#drop_command li").click(function(){
                                          $('#command').text($(this).text());
                                          $("#command").val($(this).text());

                                       });
                                    }
                                }
                            },
                            error: function(xhr){
                            }
                        });
                    }
                }
            }
        },
        error: function(xhr){
        }
    });
}

function deviceNetUpdate(i){
    code = $("#code" + i)[0].value;
    type = $("#type" + i)[0].value;
    mac = $("#mac" + i).text();
    $.ajax({
        url: "/api/device_net_update",
        type: 'GET',
        data: {
            c: code,
            t: type,
            m: mac
        },
        success: function(response){
            var json = $.parseJSON(JSON.stringify(response));
            if (json["output"].search(":") > -1){
                $('#errore').text(json["output"].split(": ")[1]);
            }
        },
        error: function(xhr){
        }
    });
}

function deviceNetType(){
    $.ajax({
        url: "/api/device_net_type",
        type: 'GET',
        success: function(response){
            var json = $.parseJSON(JSON.stringify(response));
            if (json["output"].search(":") > -1){
                $('#errore').text(json["output"].split(": ")[1]);
            } else {
                var types = json["types"]
                $("#drop_device").empty();
                for(var i = 0; i < types.length;i++) {
                    $('#drop_device').append('<li class="dropdown-item">' + types[i]['type_code'] + '</li>');
                    $("#drop_device li").click(function(){
                      $('#device').text($(this).text());
                      $("#device").val($(this).text());

                   });
                }
            }
        },
        error: function(xhr){
        }
    });
}