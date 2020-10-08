function carica_pag(lnk_pag){
    let struct_set = {
        "id":"set",
        "visibility": true
    };
    let struct_home = {
        "id":"home",
        "visibility": true
    };
    let struct_dev = {
        "id":"dev",
        "visibility": true
    };
    let struct_user = {
        "id":"user",
        "visibility": true
    };
    let struct_device = {
        "id":"device",
        "devices": [
            {
                "commands": [
                    "online",
                    "reboot"
                ],
                 "net_code": "YYY",
                "net_desc": "None",
                "net_ip": "YYYY",
                "net_last_update": "2020-10-03 20:49:43",
                "net_mac": "YYYY",
                "net_mac_info": "YYY",
                "net_psw": "YYY",
                "net_type": "YYY",
                "net_usr": "YYY"
            },
            {
                "commands": [
                    "online",
                    "on",
                    "off"
                ],
                "net_code": "XXX",
                "net_desc": "None",
                "net_ip": "XXXX",
                "net_last_update": "2020-10-03 20:49:43",
                "net_mac": "XXXX",
                "net_mac_info": "XXX",
                "net_psw": "XXX",
                "net_type": "XXX",
                "net_usr": "XXX"
            }
        ],
        "output": "OK",
        "timestamp": "2020-10-04 04:00:38",
        "user_role": "ADMIN"
    };

    let json = $.parseJSON(JSON.stringify(eval('struct_'.concat(lnk_pag))));
    console.log(json);
    //Disattivo Colorazione Selezionato
    let lista_lnk=[struct_home,struct_device,struct_user,struct_dev,struct_set];

    for (let i=0;i<lista_lnk.length;i++)
        $('#lnk_'.concat(lista_lnk[i]["id"])).attr('class', 'nav-link');

    //Attivo Colorazione Selezionato su Target
    $('#lnk_'.concat(lnk_pag)).attr('class', 'nav-link active');
    let template_form = Handlebars.compile($('#form_'.concat(lnk_pag))[0].innerHTML);
    $('#form-main').html(template_form(json));

}