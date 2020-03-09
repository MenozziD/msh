var user_list = {};
var page_up_u = 0;
var page_down_u = 0;

function user_function(type_op){
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
    if (type_op.search('delete') >= 0){
        id = type_op.replace('delete','');
        type_op = 'delete';
        user = $("#username" + id).text();
    }
    if (type_op == 'add'){
        user = $("#username_add")[0].value;
        password = $("#password_add")[0].value;
        role = $("#role_user_add")[0].value;
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
                        var users = json["users"];
                        var user_template = Handlebars.compile($("#table-user-template")[0].innerHTML);
                        $('#table-user').html(user_template(json));
                        user_list = [];
                        for(var i = 0; i < users.length;i++) {
                            user_list.push(users[i]);
                            $('#psw_user' + i).on('input',function(e){must_save_user(this.id.replace("psw_user", ""))});
                            if (json['user_username'] != users[i].username)
                                $('#psw_user' + i).prop('readonly', true);
                            if (json['user_role'] != 'ADMIN'){
                                $('#role_user' + i).prop('disabled', true);
                            }
                        }
                    }
                    if (type_op == 'update' || type_op == 'delete' || type_op == 'add'){
                        user_function('list');
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

function must_save_user(id){
    var user = $("#username" + id).text();
    var password = $("#psw_user" + id)[0].value;
    var role = $("#role_user" + id)[0].value;
    for (var i = 0; i < user_list.length; i++){
        if (user_list[i]['username'] == user){
            if (password != user_list[i]['password'] || role != user_list[i]['role']){
                $("#salva_user" + i).attr("disabled", false);
                $("#reset_user" + i).attr("disabled", false);
            } else {
                $("#salva_user" + i).attr("disabled", true);
                $("#reset_user" + i).attr("disabled", true);
            }
        }
    }
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

function user_reset(id){
    var username = $("#username" + id).text();
    for (var i = 0; i < user_list.length; i++){
        if (user_list[i]['username'] == username){
            $("#salva_user" + i).attr("disabled", true);
            $("#reset_user" + i).attr("disabled", true);
            $("#psw_user" + id)[0].value = user_list[i]['password'];
            $("#role_user" + id)[0].value = user_list[i]['role'];
            $("#role_user" + id).text(user_list[i]['role']);
            console.log(user_list[i]['role']);
        }
    }
}

function user_role(id, text){
    if (id != "add"){
        $('#role_user' + id).text(text);
        $("#role_user" + id).val(text);
        must_save_user(id);
    } else {
        $('#role_user_add').text(text);
        $("#role_user_add").val(text);
    }
}