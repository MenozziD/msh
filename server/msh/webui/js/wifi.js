var numero_wifi_pagina = 5;
var page_up_w = 0;
var page_down_w = 0;
var table_wifi = {};
var new_wifi_list = [];
var last_sort_w = true;

function createTableWifi(struttura){
    var wifi_template = Handlebars.compile($("#table-wifi-template")[0].innerHTML);
    $('#table-wifi').html(wifi_template(struttura));
    $('[data-toggle="tooltip"]').tooltip({html: true});
    abilButtonWifi();
}

function sortTableWifi(attribute){
    // a.data.localeCompare(b.data); crescente
    // b.data.localeCompare(a.data); decrescente
    if (last_sort_w) {
        new_wifi_list.sort(function(a, b){
            return a[attribute].localeCompare(b[attribute], undefined, {'numeric': true});
        });
    } else {
       new_wifi_list.sort(function(a, b){
            return b[attribute].localeCompare(a[attribute], undefined, {'numeric': true});
        });
    }
    tmp_wifi = []
    for (var i=0; i < new_wifi_list.length; i++){
        for (var j=0; j < new_wifi_list.length; j++){
            if (new_wifi_list[i]['ssid'] == wifi_table['wifi_ap'][j]['ssid']){
                tmp_wifi.push(wifi_table['wifi_ap'][j]);
                break;
            }
        }
    }
    wifi_table['wifi_ap'] = $.extend(true, [], tmp_wifi);
    wifi_table['current_page'] = 1;
    var tmp_list = Object.assign({}, wifi_table);
    tmp_list['wifi_ap'] = $.extend(true, [], new_wifi_list);
    tmp_list['wifi_ap'] = tmp_list['wifi_ap'].slice(0, numero_wifi_pagina);
    createTableWifi(tmp_list);
    last_sort_w = !last_sort_w;
}

function check_change_wifi(indice, chiave, nome){
    var mex = "";
    if (wifi_table['wifi_ap'][indice][chiave] != new_wifi_list[indice][chiave])
        mex = "\t# Cambiato il " +  nome + " da " + wifi_table['wifi_ap'][indice][chiave] + " a " + new_wifi_list[indice][chiave] + "\n";
    return mex;
}

function getRiepilogoWiFi() {
    var message = "";
    for (var i = 0; i < new_wifi_list.length; i++){
        if (JSON.stringify(wifi_table['wifi_ap'][i]) != JSON.stringify(new_wifi_list[i])){
            if (check_change_wifi(i, 'to_set', "") != "")
                message = message + "- L'AP con SSID " + wifi_table['wifi_ap'][i]['ssid'] + " verra settato come default\n";
            message = message + "\n";
        }
    }
    $('#recap_wifi').text(message);
    $('#modal_recap_change_wifi').modal();
}

function wifi(type_op){
    var wifi_set = null;
    if (type_op == 'update'){
        for (var i = 0; i < new_wifi_list.length; i++){
            if (JSON.stringify(wifi_table['wifi_ap'][i]) != JSON.stringify(new_wifi_list[i])){
                wifi_set = {
                    'ssid': wifi_table['wifi_ap'][i]['ssid'],
                    'psw': wifi_table['wifi_ap'][i]['wpa_psk_key']
                }
            }
        }
    }
    var body = {
        "tipo_operazione": type_op
    };
    if (wifi_set != null)
        body['wifi'] = wifi_set;
    $.blockUI();
    $.ajax({
        url: "/api/wifi",
        type: 'POST',
        contentType: "application/json",
        data : JSON.stringify(body),
        success: function(response){
            var json = $.parseJSON(JSON.stringify(response));
            $.unblockUI();
            if (json["output"].search("OK") == 0){
                if (type_op == 'list'){
                    var page_number = Math.floor(json['wifi_ap'].length / numero_wifi_pagina);
                    var resto = json['wifi_ap'].length % numero_wifi_pagina;
                    if (resto > 0)
                        page_number = page_number + 1;
                    json['pages'] = page_number;
                    json['current_page'] = 1;
                    for (i = 0; i < json['wifi_ap'].length; i++){
                        json['wifi_ap'][i]['to_set'] = false;
                    }
                    wifi_table = Object.assign({}, json);
                    new_wifi_list = $.extend(true, [], wifi_table["wifi_ap"]);
                    json['wifi_ap'] = json['wifi_ap'].slice(0, numero_wifi_pagina);
                    createTableWifi(json);
                }
                if (type_op == 'update'){
                    wifi('list');
                }
            } else {
                if (json["output"].indexOf("essere eseguita solo da un ADMIN") == -1){
                    $("#error_modal").modal();
                    $('#errore').text(json["output"]);
                }
            }
        },
        error: function(xhr){
        }
    });
}

function abilButtonWifi(){
    var mex = "È necessario modificare almeno un valore per attivare questa funzione";
    if (JSON.stringify(wifi_table['wifi_ap']) != JSON.stringify(new_wifi_list)){
        abilButtonTooltip("reset_wifi");
        abilButtonTooltip("salva_wifi");
    } else {
        disabilButtonTooltip("reset_wifi", mex);
        disabilButtonTooltip("salva_wifi", mex);
    }
}

function change_page_w(pagina){
    if (pagina >= 1 && pagina <= wifi_table['wifi_ap']) {
        page_up_w = 0;
        page_down_w = 0;
        wifi_table['current_page'] = pagina;
        var tmp_list = Object.assign({}, wifi_table);
        tmp_list['wifi_ap'] = $.extend(true, [], new_wifi_list);
        tmp_list['wifi_ap'] = tmp_list['wifi_ap'].slice((pagina-1)*numero_wifi_pagina, pagina*numero_wifi_pagina);
        createTableUser(tmp_list);
        select_all_w = false;
        if (page_down_w+page_up_w > 4){
            if (page_up_w+page_down_w == 6 || page_up_w+page_down_w == 7 || page_up_w+page_down_w == 8){
                for (var i=page_up_w; i > 2; i--){
                    $("#w" + (pagina+i))[0].classList.add("d-none");
                }
                for (var i=page_down_w; i > 2; i--){
                    $("#w" + (pagina-i))[0].classList.add("d-none");
                }
            }
            if (page_up_w+page_down_w == 5){
                if (page_up_w == 4){
                   $("#w" + (pagina+page_up_w))[0].classList.add("d-none");
                }
                if (page_down == 4){
                   $("#w" + (pagina-page_down_w))[0].classList.add("d-none");
                }
            }
        }
    }
}

function cambioValWifi(id){
    var ind = null;
    ind = ((wifi_table['current_page']-1)*numero_wifi_pagina) + parseInt(id);
    var to_set = $("#checkbox_wifi" + id).prop("checked");
    for (var i=0; i < new_wifi_list.length; i++){
        new_wifi_list[i]['to_set'] = false;
        $("#checkbox_wifi" + i).prop("checked", false);
    }
    $("#checkbox_wifi" + id).prop("checked", to_set);
    new_wifi_list[ind]['to_set'] = to_set;
    abilButtonWifi();
}

function wifi_reset(){
    new_wifi_list = $.extend(true, [], wifi_table["wifi_ap"]);
    var tmp_list = Object.assign({}, wifi_table);
    tmp_list['wifi_ap'] = tmp_list['wifi_ap'].slice((wifi_table['current_page']-1)*numero_wifi_pagina, wifi_table['current_page']*numero_wifi_pagina);
    createTableWifi(tmp_list);
}