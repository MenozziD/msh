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