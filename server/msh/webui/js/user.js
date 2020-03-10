var numero_user_pagina = 5;
var user_table = {};
var new_user_list = [];
var tipologie_user = {'role': ['ADMIN', 'USER']};
var page_up_u = 0;
var page_down_u = 0;
var select_all_u = false;
var last_sort_u = true;

function view_user_role(id){
    var template = Handlebars.compile($("#drop_type_user-template")[0].innerHTML);
    $('#drop_role' + id).html(template(tipologie_user));
    $('#drop_role' + id + ' li').click(function() {
        $('#role_user' + id).text($(this).text());
        $("#role_user" + id).val($(this).text());
        if (id != 'add')
            cambioValUser(id);
    });
}

function createTableUser(struttura){
    var user_template = Handlebars.compile($("#table-user-template")[0].innerHTML);
    $('#table-user').html(user_template(struttura));
    $('[data-toggle="tooltip"]').tooltip({html: true});
    abilButtonUser();
}

function sortTableUser(attribute){
    // a.data.localeCompare(b.data); crescente
    // b.data.localeCompare(a.data); decrescente
    if (last_sort_u) {
        new_user_list.sort(function(a, b){
            return a[attribute].localeCompare(b[attribute], undefined, {'numeric': true});
        });
    } else {
       new_user_list.sort(function(a, b){
            return b[attribute].localeCompare(a[attribute], undefined, {'numeric': true});
        });
    }
    tmp_usr = []
    for (var i=0; i < new_user_list.length; i++){
        for (var j=0; j < new_user_list.length; j++){
            if (new_user_list[i]['username'] == user_table['users'][j]['username']){
                tmp_usr.push(user_table['users'][j]);
                break;
            }
        }
    }
    user_table['users'] = $.extend(true, [], tmp_usr);
    user_table['current_page'] = 1;
    var tmp_list = Object.assign({}, user_table);
    tmp_list['users'] = $.extend(true, [], new_user_list);
    tmp_list['users'] = tmp_list['users'].slice(0, numero_user_pagina);
    createTableUser(tmp_list);
    last_sort_u = !last_sort_u;
}

function check_change_user(indice, chiave, nome){
    var mex = "";
    if (user_table['users'][indice][chiave] != new_user_list[indice][chiave])
        mex = "\t# Cambiato il " +  nome + " da " + user_table['users'][indice][chiave] + " a " + new_user_list[indice][chiave] + "\n";
    return mex;
}

function getRiepilogoUser() {
    var message = "";
    for (var i = 0; i < user_table['users'].length; i++){
        if (JSON.stringify(user_table['users'][i]) != JSON.stringify(new_user_list[i])){
            if (check_change_user(i, 'to_delete', "") != ""){
                message = message + "- L'utente con username " + user_table['users'][i]['username'] + " verra eliminato\n";
            } else {
                message = message + "- Modificato utente con username " + user_table['users'][i]['username'] + "\n";
                message = message + check_change_user(i, 'password', "PASSWORD");
                message = message + check_change_user(i, 'role', "RUOLO");
            }
            message = message + "\n"
        }
    }
    $('#recap_user').text(message);
    $('#modal_recap_change_user').modal();
}

function user(type_op){
    var user = null;
    var password = null;
    var role = null;
    var id = null;
    if (type_op.search('update') >= 0){
        id = type_op.replace('update','');
        type_op = 'update';
        user = $("#username" + id).text();
        for (var i = 0; i < user_list.length; i++){
            if (user_list[i]['username'] == user){
                if ($("#psw_user" + id)[0].value != user_list[i]['password'])
                    password = $("#psw_user" + id)[0].value;
                if ($("#role_user" + id)[0].value != user_list[i]['role'])
                    role = $("#role_user" + id)[0].value;
            }
        }
    }
    if (type_op != 'add' || (user != "" && password != "" && role != "")){
        var body = {
            "tipo_operazione": type_op
        };
        if (role != null)
            body['role'] = role
        if (user != null)
            body['username'] = user
        if (password != null)
            body['password'] = password
        $.ajax({
            url: "/api/user",
            type: 'POST',
            contentType: "application/json",
            data : JSON.stringify(body),
            success: function(response){
                var json = $.parseJSON(JSON.stringify(response));
                if (json["output"].search("OK") == 0){
                    if (type_op == 'list'){
                        var page_number = Math.floor(json['users'].length / numero_user_pagina);
                        var resto = json['users'].length % numero_user_pagina;
                        if (resto > 0)
		                    page_number = page_number + 1;
		                json['pages'] = page_number;
	                    json['current_page'] = 1;
	                    for (i = 0; i < json['users'].length; i++){
		                    json['users'][i]['to_delete'] = false;
	                    }
	                    user_table = Object.assign({}, json);
	                    new_user_list = $.extend(true, [], user_table["users"]);
	                    json['users'] = json['users'].slice(0, numero_user_pagina);
	                    createTableUser(json);
                    }
                    if (type_op == 'update' || type_op == 'delete' || type_op == 'add'){
                        user('list');
                    }
                } else {
                    $("#error_modal").modal();
                    $('#errore').text(json["output"]);
                }
            },
            error: function(xhr){
            }
        });
    }
}

function selectAllU(){
    var ind = ((user_table['current_page']-1)*numero_user_pagina);
    var ind_final = null;
    var value = null;
    if (user_table['current_page'] == user_table['pages'])
        ind_final = user_table['users'].length;
    else
        ind_final = ind + numero_user_pagina;
    if (! select_all_u)
        value = true;
    else
        value = false;
    for (var i = 0; i < ind_final - ind; i++)
        $("#checkbox_user" + i).prop("checked", value);
    for(var j = ind; j < ind_final; j++)
        cambioValUser(j);
    select_all_u = value;
}

function abilButtonUser(){
    if (JSON.stringify(user_table['users']) != JSON.stringify(new_user_list)){
        $("#reset_user").prop("disabled", false);
        $("#reset_user").removeAttr("style");
        $("#salva_user").prop("disabled", false);
        $("#salva_user").removeAttr("style");
        $("#tooltip_reset_user").removeAttr("data-original-title");
        $("#tooltip_salva_user").removeAttr("data-original-title");
    } else {
        $("#reset_user").prop("disabled", true);
        $("#reset_user").attr("style", "pointer-events: none;");
        $("#salva_user").prop("disabled", true);
        $("#salva_user").attr("style", "pointer-events: none;");
        $("#tooltip_reset_user").attr("data-original-title", "È necessario modificare almeno un valore per attivare questa funzione");
        $("#tooltip_salva_user").attr("data-original-title", "È necessario modificare almeno un valore per attivare questa funzione");
    }
}

function change_page_u(pagina){
    if (pagina >= 1 && pagina <= user_table['pages']) {
        page_up_u = 0;
        page_down_u = 0;
        user_table['current_page'] = pagina;
        var tmp_list = Object.assign({}, user_table);
        tmp_list['users'] = $.extend(true, [], new_user_list);
        tmp_list['users'] = tmp_list['devices'].slice((pagina-1)*numero_user_pagina, pagina*numero_user_pagina);
        createTableUser(tmp_list);
        select_all_u = false;
        if (page_down_u+page_up_u > 4){
            if (page_up_u+page_down_u == 6 || page_up_u+page_down_u == 7 || page_up_u+page_down_u == 8){
                for (var i=page_up_u; i > 2; i--){
                    $("#u" + (pagina+i))[0].classList.add("d-none");
                }
                for (var i=page_down; i > 2; i--){
                    $("#u" + (pagina-i))[0].classList.add("d-none");
                }
            }
            if (page_up_u+page_down_u == 5){
                if (page_up_u == 4){
                   $("#u" + (pagina+page_up_u))[0].classList.add("d-none");
                }
                if (page_down == 4){
                   $("#u" + (pagina-page_down_u))[0].classList.add("d-none");
                }
            }
        }
    }
}

function cambioValUser(id){
    var ind = ((user_table['current_page']-1)*numero_user_pagina) + parseInt(id);
    var password = $("#psw_user" + id)[0].value;
    var ruolo = $("#role_user" + id)[0].value;
    var to_del = $("#checkbox_user" + id).prop("checked");
    new_user_list[ind]['password'] = password;
    new_user_list[ind]['role'] = ruolo;
    new_user_list[ind]['to_delete'] = to_del;
    abilButtonUser();
}

function user_reset(){
    new_user_list = $.extend(true, [], user_table["users"]);
    var tmp_list = Object.assign({}, user_table);
    tmp_list['users'] = tmp_list['users'].slice((user_table['current_page']-1)*numero_user_pagina, user_table['current_page']*numero_user_pagina);
    createTableUser(tmp_list);
}

function view_password_user(i){
    var input_text = $("#psw_user" + i)[0];
    var icon = $("#psw_icon_user" + i)[0];
    if (input_text.type == 'text'){
        input_text.type = 'password';
        icon.classList.remove("fa-eye");
        icon.classList.add("fa-eye-slash");
    } else {
        input_text.type = 'text';
        icon.classList.remove("fa-eye-slash");
        icon.classList.add("fa-eye");
    }
}