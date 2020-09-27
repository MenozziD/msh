function carica(){
    $.blockUI.defaults.css.width = '0%';
    $.blockUI.defaults.css.height = '0%';
    $.blockUI.defaults.css.left = '50%';
    $.blockUI.defaults.css.border = '';
    $.blockUI.defaults.baseZ = 2000;
    $.blockUI.defaults.message = '<div class="spinner-border text-light" role="status" style=""><span class="sr-only">Loading...</span></div>';
    $.blockUI();
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
                device_tabella["page_up"] = device_tabella["page_up"] + 1;
            else {
                if (d == 'user')
                    page_up_u = page_up_u + 1;
               else
                    wifi_tabella["page_up"] = wifi_tabella["page_up"] + 1;
            }
            return opts.fn(this);
        } else {
            return opts.inverse(this);
        }
    });
    Handlebars.registerHelper('if_mag', function(a, b, c, d, opts) {
        if (a-b > 0) {
            if (d == 'device')
                device_tabella["page_down"] = device_tabella["page_down"] + 1;
            else {
                if (d == 'user')
                    page_down_u = page_down_u + 1;
               else
                    wifi_tabella["page_down"] = wifi_tabella["page_down"] + 1;
            }
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
    net('type');
    user('list');
    upload_arduino('core');
    upload_arduino('tipo');
    wifi('list');
    $('#modal_user').on('shown.bs.modal', function (e) {
        var cw = $("#tooltip_plus_user").height();
        $('#tooltip_plus_user').css({'width':cw+'px'});
        var h_col = ($("#colonna-table-user")[0].rows[1].offsetHeight * numero_user_pagina) + $("#colonna-table-user")[0].rows[0].offsetHeight + 2;
        $("#colonna-table-user").css({'height':h_col});
    })
    $('#modal_wifi').on('shown.bs.modal', function (e) {
        if ( ! (typeof $("#colonna-table-wifi") === "undefined")){
            var h_col = ($("#colonna-table-wifi")[0].rows[1].offsetHeight * wifi_tabella["record_per_pagina"]) + $("#colonna-table-wifi")[0].rows[0].offsetHeight + 2;
            $("#colonna-table-wifi").css({'height':h_col});
        }
    })
    $('#modal_add_user').on('hide.bs.modal', function () {
        user_clear_add();
    })
    $('#modal_user').on('hide.bs.modal', function () {
        user_reset();
    })
    $('#modal_search').on('hide.bs.modal', function () {
        search_clear();
    })
    $('#modal_exec_cmd').on('hide.bs.modal', function () {
        exec_cmd_clear();
    })
    $('#modal_compile').on('hide.bs.modal', function () {
        compile_clear();
    })
}

function compile_clear(){
    $("#device_arduino").val("");
    $("#device_arduino").text("");
    $("#tipo_arduino").val("");
    $("#tipo_arduino").text("");
    $('#esito_upload').val("");
    $('#program_bytes_used').val("");
    $('#program_percentual_used').val("");
    $('#program_bytes_total').val("");
    $('#memory_bytes_used').val("");
    $('#memory_percentual_used').val("");
    $('#memory_bytes_free').val("");
    $('#memory_bytes_total').val("");
    $('#porta_seriale').val("");
    $('#chip').val("");
    $('#mac_addres').val("");
    $('#byte_write').val("");
    $('#byte_write_compressed').val("");
    $('#time').val("");
    cambioValSvil();
}

function search_clear(){
    $('#found').val("");
    $('#new').val("");
    $('#update').val("");
}

function exec_cmd_clear(){
    $('#device').val("");
    $('#device').text("");
    $('#command').val("");
    $('#command').text("");
    $('#cmd_result').text("");
    $('#cmd_result').val("");
    var mex = "Campi mancanti: <ul><li>DISPOSITIVO</li><li>COMANDO</li></ul>";
    disabilButtonTooltip("invia", mex);
    mex = "Scegliere il DISPOSITIVO";
    disabilButtonTooltip("command", mex);
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

function abilButtonTooltip(name){
    $("#" + name).prop("disabled", false);
    $("#" + name).removeAttr("style");
    $("#tooltip_" + name).removeAttr("data-original-title");
}

function disabilButtonTooltip(name, mex){
    $("#" + name).prop("disabled", true);
    $("#" + name).attr("style", "pointer-events: none;");
    $("#tooltip_" + name).attr("data-original-title", mex);
}
