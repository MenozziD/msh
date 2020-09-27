let device_tabella = {
    "id": "device",
    "id_char": "d",
    "record_per_pagina": 8,
    "page_up": 0,
    "page_down": 0,
    "table": {},
    "table_key": "devices",
    "primary_key": "net_mac",
	"new_list": [],
    "last_sort": true,
	"select_all": false,
	"tipologie": {},
    "mex_add": {},
    "mex_set": {},
    "mex_del": {
		"static": "- Il device con MAC address %1 verra eliminato\n",
		"param": ["struct_tabella['devices'][i]['net_mac']"]
	},
    "mex_up": {
		"static": "- Modificato device con MAC address %1 \n",
		"param": ["struct_tabella['devices'][i]['net_mac']"]
	},
    "editable": [
		{
			'key': 'net_code',
			'name': "CODICE",
			'id_frontend': 'code'
		},
		{
			'key': 'net_type',
			'name': "TIPO",
			'id_frontend': 'type'
		},
		{
			'key': 'net_usr',
			'name': "USER SSH",
			'id_frontend': 'usr'
		},
		{
			'key': 'net_psw',
			'name': "PASSWORD SSH",
			'id_frontend': 'psw'
		}
    ],
    "checkbox_action": "to_delete",
    "field_add": [],
    'method_add': ""
};

function net(type_op){
    let type = null;
    let dispositivo = null;
    let comando = null;
    let list_up_device = [];
    if (type_op === 'update'){
        for (let i = 0; i < device_tabella["table"][device_tabella["table_key"]].length; i++){
            if (JSON.stringify(device_tabella["table"][device_tabella["table_key"]][i]) !== JSON.stringify(device_tabella["new_list"][i])){
                let dev = {
                    'net_mac': device_tabella["table"][device_tabella["table_key"]][i]['net_mac']
                };
                if (checkChange(i, 'to_delete', "", device_tabella) !== ""){
                    dev['to_delete'] = true;
                } else {
                    if (checkChange(i, 'net_code', "CODICE", device_tabella) !== "")
                        dev['net_code'] = device_tabella["new_list"][i]['net_code'];
                    if (checkChange(i, 'net_type', "TIPO", device_tabella) !== "")
                        dev['net_type'] = device_tabella["new_list"][i]['net_type'];
                    if (checkChange(i, 'net_usr', "USER SSH", device_tabella) !== "")
                        dev['net_usr'] = device_tabella["new_list"][i]['net_usr'];
                    if (checkChange(i, 'net_psw', "PASSWORD SSH", device_tabella) !== "")
                        dev['net_psw'] = device_tabella["new_list"][i]['net_psw'];
                }
                list_up_device.push(dev);
            }
        }
    }
    if (type_op === 'command'){
        for(let l = 0; l < device_tabella["table"][device_tabella["table_key"]].length; l++) {
            if (device_tabella["table"][device_tabella["table_key"]][l]['net_code'] === $('#device')[0].value){
                type = device_tabella["table"][device_tabella["table_key"]][l]['net_type'];
                break;
            }
        }
    }
    if (type_op === "cmd"){
        dispositivo = $('#device')[0].value;
        comando = $('#command')[0].value;
    }
    let body = {
        "tipo_operazione": type_op
    };
    if (type != null)
        body['net_type'] = type;
    if (dispositivo != null)
        body['dispositivo'] = dispositivo;
    if (comando != null)
        body['comando'] = comando;
    if (list_up_device.length > 0)
        body['list_up_device'] = list_up_device;
    if (['scan', 'update', 'cmd', 'command'].indexOf(type_op) >= 0)
        $.blockUI();
    $.ajax({
        url: "/api/net",
        type: 'POST',
        contentType: "application/json",
        data : JSON.stringify(body),
        success: function(response){
            let json = $.parseJSON(JSON.stringify(response));
            if (['scan', 'update', 'cmd', 'command'].indexOf(type_op) >= 0)
                $.unblockUI();
            if (json["output"].search("OK") === 0){
                if (type_op === 'scan'){
                    $('#found')[0].value = json["find_device"];
                    $('#new')[0].value = json["new_device"];
                    $('#update')[0].value = json["updated_device"];
                    net('list');
                }
                if (type_op === 'type'){
                    let typ = [];
                    for (let i=0; i<json["types"].length; i++)
                        typ.push(json["types"][i]["type_code"]);
                    device_tabella["tipologie"] = {"types": typ};
                }
                if (type_op === 'list'){
                    let funzioni_bar_template = Handlebars.compile($("#funzioni-bar-template")[0].innerHTML);
                    $('#funzioni_bar').html(funzioni_bar_template(json));
                    let page_number = Math.floor(json[device_tabella["table_key"]].length / device_tabella["record_per_pagina"]);
                    let resto = json[device_tabella["table_key"]].length % device_tabella["record_per_pagina"];
                    if (resto > 0)
                        page_number = page_number + 1;
                    json['pages'] = page_number;
                    json['current_page'] = 1;
                    for (let i = 0; i < json[device_tabella["table_key"]].length; i++){
                        json[device_tabella["table_key"]][i]['to_delete'] = false;
                    }
                    device_tabella["table"] = Object.assign({}, json);
                    device_tabella["new_list"] = $.extend(true, [], device_tabella["table"][device_tabella["table_key"]]);
                    json[device_tabella["table_key"]] = json[device_tabella["table_key"]].slice(0, device_tabella["record_per_pagina"]);
                    createTable(json, device_tabella);
                }
                if (type_op === 'command'){
                    let commands = json["commands"];
                    let command_template = Handlebars.compile($("#drop_command-template")[0].innerHTML);
                    $('#drop_command').html(command_template(commands));
                    for(let k = 0; k < commands.length; k++) {
                        $("#drop_command li").click(function(){
                          $('#command').text($(this).text());
                          $("#command").val($(this).text());
                          abilButtonTooltip("invia");
                       });
                    }
                }
                if (type_op === 'update'){
                    net('list');
                }
                if (type_op === 'cmd'){
                    $('#cmd_result')[0].value = json["result"];
                }
            } else {
                $("#error_modal").modal();
                $('#errore').text(json["output"]);
                if (type_op == 'cmd'){
                    $('#errore_title').text(json["result"]);
                    $('#cmd_result')[0].value = json["result"];
                }
            }
        },
        error: function(xhr){
        }
    });
}

function device_net_code(){
    var template = Handlebars.compile($("#drop_device-template")[0].innerHTML);
    $('#drop_device').html(template(device_tabella["table"][device_tabella["table_key"]]));
    for(var i = 0; i < device_tabella["table"][device_tabella["table_key"]].length;i++) {
        $("#drop_device li").click(function(){
          $('#device').text($(this).text());
          $("#device").val($(this).text());
          abilCommand();
       });
    }
}

function abilCommand(){
    var mex = "Campi mancanti: <ul><li>COMANDO</li></ul>";
    disabilButtonTooltip("invia", mex);
    $("#command").val("");
    $("#command").text("");
    abilButtonTooltip("command");
}