function login(){
    var user = $("#username")[0].value;
    var password = $("#password")[0].value;
    var form = $('#form')[0];
    var ko = 0;
	form.classList.add('was-validated');
	Array.prototype.filter.call(form, function (element) {
      if (element.checkValidity() == false) {
		  ko++;
        }
    })
	if (ko == 0){
        var body = {
            "user": user,
            "password": password
        };
        $('#errore').text("");
        $('#errore')[0].classList.remove("d-block");
        $('#errore')[0].classList.add("d-none");
        $.ajax({
            url: "/api/login",
            type: 'POST',
            contentType: "application/json",
            data : JSON.stringify(body),
            success: function(response){
                var json = $.parseJSON(JSON.stringify(response));
                if (json["output"] == 'OK')
                    $(window.location).attr('href', '/');
                else {
                    $('#errore').text(json["output"]);
                    $('#errore')[0].classList.remove("d-none");
                    $('#errore')[0].classList.add("d-block");
                }
            },
            error: function(xhr){
            }
        });
    }
}