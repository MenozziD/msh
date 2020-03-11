function carica(){
    $.blockUI.defaults.css.width = '0%';
    $.blockUI.defaults.css.height = '0%';
    $.blockUI.defaults.css.left = '50%';
    $.blockUI.defaults.css.border = '';
    $.blockUI.defaults.baseZ = 2000;
    $.blockUI.defaults.message = '<div class="spinner-border text-light" role="status" style=""><span class="sr-only">Loading...</span></div>';
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
    net('type');
    upload_arduino('core');
    upload_arduino('tipo');
    user('list');
    $('#modal_user').on('shown.bs.modal', function (e) {
        var cw = $("#tooltip_plus_user").height();
        $('#tooltip_plus_user').css({'width':cw+'px'});
    })
    $('#modal_add_user').on('hide.bs.modal', function () {
        user_clear_add();
    })
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
