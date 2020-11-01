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
	"tipologie": {
        "types": [],
        "device": []
    },
    "mex_add": {},
    "mex_set": {},
    "mex_del": {
		"static": "- Il device con MAC address %1 verra eliminato\n",
		"param": ["struct_tabella['table']['devices'][indice]['net_mac']"]
	},
    "mex_up": {
		"static": "- Modificato device con MAC address %1 \n",
		"param": ["struct_tabella['table']['devices'][indice]['net_mac']"]
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
			'id_frontend': 'types_device'
		}
    ],
    'to_update': [],
    "cmd_exec": {
        "device": "",
        "command": ""
    },
    "checkbox_action": "to_delete",
    "field_add": [],
    'method_add': ""
};
let device_types = [];
let user_tabella = {
    "id": "user",
    "id_char": "u",
    "record_per_pagina": 5,
    "page_up": 0,
    "page_down": 0,
    "table": {},
    "table_key": "users",
    "primary_key": "username",
	"new_list": [],
    "last_sort": true,
	"select_all": false,
	"tipologie": {
        'role': ['ADMIN', 'USER']
    },
    "mex_add": {
        "static": "- L'utente con username %1 verrà aggiunto con il ruolo di %2 \n",
        "param": ["struct_tabella['table']['users'][indice]['username']", "struct_tabella['new_list'][indice]['role']"]
    },
    "mex_set": {},
    "mex_del": {
		"static": "- L'utente con username %1 verra eliminato\n",
		"param": ["struct_tabella['table']['users'][indice]['username']"]
	},
    "mex_up": {
		"static": "- Modificato utente con username %1 \n",
		"param": ["struct_tabella['table']['users'][indice]['username']"]
	},
    "editable": [
		{
			'key': 'password',
			'name': "PASSWORD",
			'id_frontend': 'psw_user'
		},
		{
			'key': 'role',
			'name': "RUOLO",
			'id_frontend': 'role_user'
		}
    ],
    'to_update': [],
    "checkbox_action": "to_delete",
    "field_add": [
        {
            "key": "username",
            "id_frontend": "username_add"
        },
        {
            "key": "password",
            "id_frontend": "password_add"
        },
        {
            "key": "role",
            "id_frontend": "role_useradd"
        }
    ],
    'method_add': "checkUserAdd()"
};
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
    'to_update': [],
    "checkbox_action": "to_set",
    "field_add": [],
    'method_add': ""
};
let arduino_tabella = {
    "id": "arduino",
    "tipologie": {
        'device': [],
        'tipo': []
    }
};
let settings_data = {
    "id": "settings",
    "settings": {},
    "new_settings": {},
    "diff_settings": {}
};