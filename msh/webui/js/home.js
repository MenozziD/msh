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

function deviceList(){
    $.ajax({
        url: "/api/device_list",
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
                    device = devices[i];
                    $('#table tbody').append('<tr>');
                    $('#table tbody').append('<td>' + device['device_code'] + '</td>');
                    $('#table tbody').append('<td>' + device['device_type'] + '</td>');
                    $('#table tbody').append('<td>' + device['device_status'] + '</td>');
                    $('#table tbody').append('<td>' + device['device_ip'] + '</td>');
                    $('#table tbody').append('<td>' + device['device_mac'] + '</td>');
                    $('#table tbody').append('<td>' + device['device_mac_info'] + '</td>');
                    $('#table tbody').append('</tr>');
                }
                $('#table')[0].classList.remove('invisible');
            }
        },
        error: function(xhr){
        }
    });
}