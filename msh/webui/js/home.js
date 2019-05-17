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
		    url: "/api/netcmd",
		    type: 'GET',
		    data: {
				d: device,
				c: command
			},
		    success: function(response){
				var json = $.parseJSON(JSON.stringify(response));
				$('#result')[0].value = json["device_status"];
            },
            error: function(xhr){
            }
        });
	}
}

function scan(){
    $.ajax({
        url: "/api/netscan",
        type: 'GET',
        success: function(response){
            var json = $.parseJSON(JSON.stringify(response));
            $('#esito')[0].value = json["output"];
            $('#found')[0].value = json["find_device"];
            $('#new')[0].value = json["new_device"];
            $('#update')[0].value = json["updated_device"];
        },
        error: function(xhr){
        }
    });
}
