let wifi_tabella = {
    "id": "wifi",
    "id_char": "w",
    "record_per_pagina": 5,
    "page_up": 0,
    "page_down": 0,
    "table": {},
    "table_key": "wifi_ap",
    "primary_key": "ssid",
	"new_list": [],
    "last_sort": true,
	"select_all": false,
	"tipologie": {},
    "mex_add": {},
    "mex_set": {
		"static": "- L'AP con SSID %1 verra settato come default\n",
		"param": ["struct_tabella['table']['wifi_ap'][indice]['ssid']"]
	},
    "mex_del": {},
    "mex_up": {},
    "editable": [],
    "checkbox_action": "to_set",
    "field_add": [],
    'method_add': ""
};


function wifi(type_op){
    let wifi_set = null;
    if (type_op === 'update'){
        for (let i = 0; i < wifi_tabella["new_list"].length; i++){
            if (JSON.stringify(wifi_tabella['table'][wifi_tabella['table_key']][i]) !== JSON.stringify(wifi_tabella["new_list"][i])){
                wifi_set = {
                    'ssid': wifi_tabella['table'][wifi_tabella['table_key']][i]['ssid'],
                    'psw': wifi_tabella['table'][wifi_tabella['table_key']][i]['wpa_psk_key']
                }
            }
        }
    }
    let body = {
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
            let json = $.parseJSON(JSON.stringify(response));
            $.unblockUI();
            if (json["output"].search("OK") === 0){
                if (type_op === 'list'){
                    let page_number = Math.floor(json[wifi_tabella['table_key']].length / wifi_tabella["record_per_pagina"]);
                    let resto = json[wifi_tabella['table_key']].length % wifi_tabella["record_per_pagina"];
                    if (resto > 0)
                        page_number = page_number + 1;
                    json['pages'] = page_number;
                    json['current_page'] = 1;
                    for (let i = 0; i < json[wifi_tabella['table_key']].length; i++){
                        json[wifi_tabella['table_key']][i]['to_set'] = false;
                    }
                    wifi_tabella['table'] = Object.assign({}, json);
                    wifi_tabella["new_list"] = $.extend(true, [], wifi_tabella['table'][wifi_tabella['table_key']]);
                    json[wifi_tabella['table_key']] = json[wifi_tabella['table_key']].slice(0,  wifi_tabella["record_per_pagina"]);
                    createTable(json, wifi_tabella);
                }
                if (type_op === 'update'){
                    wifi('list');
                }
            } else {
                if (json["output"].indexOf("essere eseguita solo da un ADMIN") === -1){
                    $("#error_modal").modal();
                    $('#errore').text(json["output"]);
                }
            }
        },
        error: function(xhr){
        }
    });
}
