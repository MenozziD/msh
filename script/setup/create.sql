BEGIN TRANSACTION;
-- CREAZIONE TABELLE
CREATE TABLE "TB_NET_DEVICE_TYPE" ( `TYPE_CODE` TEXT NOT NULL UNIQUE, `TYPE_DESCRIPTION` TEXT DEFAULT '-', `FUNCTION_CODE` TEXT NOT NULL, `SYNC_RESPONSE` TEXT DEFAULT '' NOT NULL, `QUERY_RESPONSE` TEXT DEFAULT '' NOT NULL, `EXECUTE_REQUEST` TEXT DEFAULT '' NOT NULL, `EXECUTE_RESPONSE_OK` TEXT DEFAULT '' NOT NULL, `EXECUTE_RESPONSE_KO` TEXT DEFAULT '' NOT NULL, PRIMARY KEY(`TYPE_CODE`) );
CREATE TABLE "TB_NET_DEVICE" ( `NET_CODE` TEXT NOT NULL, `NET_DESC` TEXT, `NET_TYPE` TEXT NOT NULL, `NET_LASTUPDATE` TEXT DEFAULT (datetime('now','localtime')), `NET_IP` TEXT DEFAULT '', `NET_MAC` TEXT NOT NULL DEFAULT '' UNIQUE, `NET_USER` TEXT, `NET_PSW` TEXT, `NET_MAC_INFO` TEXT DEFAULT '', PRIMARY KEY(`NET_MAC`) );
CREATE TABLE "TB_NET_DIZ_CMD" ( `CMD_STR` TEXT NOT NULL, `CMD_NET_TYPE` TEXT NOT NULL );
CREATE TABLE "TB_STRING" ( `LANGUAGE` TEXT NOT NULL, `VALUE` TEXT NOT NULL, `RESULT` TEXT NOT NULL, PRIMARY KEY(`LANGUAGE`,`VALUE`) );
CREATE TABLE "TB_USER" ( `USERNAME` TEXT NOT NULL, `PASSWORD` TEXT, `ROLE` TEXT, PRIMARY KEY(`USERNAME`));
CREATE TABLE "TB_WIFI" ( `SSID` TEXT NOT NULL, `PASSWORD` TEXT, PRIMARY KEY(`SSID`));
-- POPOLO TB_NET_DEVICE_TYPE
INSERT INTO TB_NET_DEVICE_TYPE (TYPE_CODE,TYPE_DESCRIPTION,FUNCTION_CODE,SYNC_RESPONSE,QUERY_RESPONSE,EXECUTE_REQUEST,EXECUTE_RESPONSE_OK,EXECUTE_RESPONSE_KO) VALUES ("NET","Generic Device", "1",
"{  
   ""id"":""dev['net_mac']"",
   ""type"":""action.devices.types.SWITCH"",
   ""traits"":[  
      ""action.devices.traits.OnOff""
   ],
   ""name"":{  
      ""defaultNames"":[  
         ""Generic Device""
      ],
      ""name"":""dev['net_code']"",
      ""nicknames"":[  

      ]
   },
   ""willReportState"":true,
   ""deviceInfo"":{  
      ""manufacturer"":""MSH"",
      ""model"":""1"",
      ""hwVersion"":""1.0"",
      ""swVersion"":""1.0""
   },
   ""customData"":{  
      ""mshType"":""dev['net_type']""
   }
}",
"{  
   ""requestId"":""data['requestId']"",
   ""payload"":{  
      ""devices"":{  
         ""data['inputs'][0]['payload']['devices'][0]['id']"":{  
            ""on"":""cmd_ping(dev['net_ip'])['result']"",
            ""online"":""cmd_ping(dev['net_ip'])['result']""
         }
      }
   }
}",
"{
   ""on"":""{'output': 'OK'}""
}",
"{
   ""requestId"":""data['requestId']"",
   ""payload"":{
      ""commands"":[
         {
            ""ids"":[
               ""data['inputs'][0]['payload']['commands'][0]['devices'][0]['id']""
            ],
            ""status"":""SUCCESS"",
            ""states"":{  
               ""on"":""cmd_ping(dev['net_ip'])['result']"",
               ""online"":""cmd_ping(dev['net_ip'])['result']""
            }
         }
      ]
   }
}",
"{  
   ""requestId"":""data['requestId']"",
   ""payload"":{  
      ""commands"":[  
         {  
            ""ids"":[  
               ""data['inputs'][0]['payload']['commands'][0]['devices'][0]['id']""
            ],
            ""status"":""ERROR"",
            ""errorCode"":""result['output']""
         }
      ]
   }
}");
INSERT INTO TB_NET_DEVICE_TYPE (TYPE_CODE,TYPE_DESCRIPTION,FUNCTION_CODE,SYNC_RESPONSE,QUERY_RESPONSE,EXECUTE_REQUEST,EXECUTE_RESPONSE_OK,EXECUTE_RESPONSE_KO) VALUES ("PCWIN","PC Windows", "2",
"{  
   ""id"":""dev['net_mac']"",
   ""type"":""action.devices.types.TV"",
   ""traits"":[  
      ""action.devices.traits.OnOff""
   ],
   ""name"":{  
      ""defaultNames"":[  
         ""PC Windows""
      ],
      ""name"":""dev['net_code']"",
      ""nicknames"":[  

      ]
   },
   ""willReportState"":true,
   ""deviceInfo"":{  
      ""manufacturer"":""MSH"",
      ""model"":""1"",
      ""hwVersion"":""1.0"",
      ""swVersion"":""1.0""
   },
   ""customData"":{  
      ""mshType"":""dev['net_type']""
   }
}",
"{  
   ""requestId"":""data['requestId']"",
   ""payload"":{  
      ""devices"":{  
         ""data['inputs'][0]['payload']['devices'][0]['id']"":{  
            ""on"":""cmd_ping(dev['net_ip'])['result']"",
            ""online"":""cmd_ping(dev['net_ip'])['result']""
         }
      }
   }
}",
"{  
   ""on"":""cmd_pcwin('on', dev['net_mac'], dev['net_ip'], dev['net_usr'], dev['net_psw']) if parametri['on'] == 'ON' else cmd_pcwin('off', dev['net_mac'], dev['net_ip'], dev['net_usr'], dev['net_psw'])""
}",
"{  
   ""requestId"":""data['requestId']"",
   ""payload"":{  
      ""commands"":[  
         {  
            ""ids"":[  
               ""data['inputs'][0]['payload']['commands'][0]['devices'][0]['id']""
            ],
            ""status"":""SUCCESS"",
            ""states"":{  
               ""on"":""cmd_ping(dev['net_ip'])['result']"",
               ""online"":""cmd_ping(dev['net_ip'])['result']""
            }
         }
      ]
   }
}",
"{  
   ""requestId"":""data['requestId']"",
   ""payload"":{  
      ""commands"":[  
         {  
            ""ids"":[  
               ""data['inputs'][0]['payload']['commands'][0]['devices'][0]['id']""
            ],
            ""status"":""ERROR"",
            ""errorCode"":""result['output']""
         }
      ]
   }
}");
INSERT INTO TB_NET_DEVICE_TYPE (TYPE_CODE,TYPE_DESCRIPTION,FUNCTION_CODE,SYNC_RESPONSE,QUERY_RESPONSE,EXECUTE_REQUEST,EXECUTE_RESPONSE_OK,EXECUTE_RESPONSE_KO) VALUES ("AP","Access Point UNIX based SSH Compatible", "3",
"{  
   ""id"":""dev['net_mac']"",
   ""type"":""action.devices.types.SETTOP"",
   ""traits"":[  
      ""action.devices.traits.OnOff""
   ],
   ""name"":{  
      ""defaultNames"":[  
         ""Access Point UNIX based SSH Compatible""
      ],
      ""name"":""dev['net_code']"",
      ""nicknames"":[  

      ]
   },
   ""willReportState"":true,
   ""deviceInfo"":{  
      ""manufacturer"":""MSH"",
      ""model"":""1"",
      ""hwVersion"":""1.0"",
      ""swVersion"":""1.0""
   },
   ""customData"":{  
      ""mshType"":""dev['net_type']""
   }
}",
"{  
   ""requestId"":""data['requestId']"",
   ""payload"":{  
      ""devices"":{  
         ""data['inputs'][0]['payload']['devices'][0]['id']"":{  
            ""on"":""cmd_radio(dev['net_ip'], 'stato', dev['net_usr'], dev['net_psw'])['result']"",
            ""online"":""cmd_ping(dev['net_ip'])['result']""
         }
      }
   }
}",
"{  
   ""on"":""cmd_radio(dev['net_ip'], 'up', dev['net_usr'], dev['net_psw']) if parametri['on'] == 'ON' else cmd_radio(dev['net_ip'], 'down', dev['net_usr'], dev['net_psw']))""
}",
"{  
   ""requestId"":""data['requestId']"",
   ""payload"":{  
      ""commands"":[  
         {  
            ""ids"":[  
               ""data['inputs'][0]['payload']['commands'][0]['devices'][0]['id']""
            ],
            ""status"":""SUCCESS"",
            ""states"":{  
               ""on"":""cmd_radio(dev['net_ip'], 'stato', dev['net_usr'], dev['net_psw'])['result']"",
               ""online"":""cmd_ping(dev['net_ip'])['result']""
            }
         }
      ]
   }
}",
"{  
   ""requestId"":""data['requestId']"",
   ""payload"":{  
      ""commands"":[  
         {  
            ""ids"":[  
               ""data['inputs'][0]['payload']['commands'][0]['devices'][0]['id']""
            ],
            ""status"":""ERROR"",
            ""errorCode"":""result['output']""
         }
      ]
   }
}");
INSERT INTO TB_NET_DEVICE_TYPE (TYPE_CODE,TYPE_DESCRIPTION,FUNCTION_CODE,SYNC_RESPONSE,QUERY_RESPONSE,EXECUTE_REQUEST,EXECUTE_RESPONSE_OK,EXECUTE_RESPONSE_KO) VALUES ("ESP_RELE","ESP8266 con software per rele", "4",
"{  
   ""id"":""dev['net_mac']"",
   ""type"":""action.devices.types.OUTLET"",
   ""traits"":[
      ""action.devices.traits.OnOff""
   ],
   ""name"":{
      ""defaultNames"":[
         ""ESP8266 con software per rele""
      ],
      ""name"":""dev['net_code']"",
      ""nicknames"":[

      ]
   },
   ""willReportState"":true,
   ""deviceInfo"":{
      ""manufacturer"":""MSH"",
      ""model"":""1"",
      ""hwVersion"":""1.0"",
      ""swVersion"":""1.0""
   },
   ""customData"":{
      ""mshType"":""dev['net_type']""
   }
}",
"{  
   ""requestId"":""data['requestId']"",
   ""payload"":{  
      ""devices"":{  
         ""data['inputs'][0]['payload']['devices'][0]['id']"":{  
            ""on"":""cmd_esp(dev['net_ip'], 'stato')['result']"",
            ""online"":""cmd_ping(dev['net_ip'])['result']""
         }
      }
   }
}",
"{  
   ""on"":""cmd_esp(dev['net_ip'], 'toggle')""
}",
"{  
   ""requestId"":""data['requestId']"",
   ""payload"":{  
      ""commands"":[  
         {  
            ""ids"":[  
               ""data['inputs'][0]['payload']['commands'][0]['devices'][0]['id']""
            ],
            ""status"":""SUCCESS"",
            ""states"":{
               ""on"": ""cmd_esp(dev['net_ip'], 'stato')['result']"",
			   ""online"": ""cmd_ping(dev['net_ip'])['result']""
            }
         }
      ]
   }
}",
"{  
   ""requestId"":""data['requestId']"",
   ""payload"":{  
      ""commands"":[  
         {  
            ""ids"":[  
               ""data['inputs'][0]['payload']['commands'][0]['devices'][0]['id']""
            ],
            ""status"":""ERROR"",
            ""errorCode"":""result['output']""
         }
      ]
   }
}");
INSERT INTO TB_NET_DEVICE_TYPE (TYPE_CODE,TYPE_DESCRIPTION,FUNCTION_CODE,SYNC_RESPONSE,QUERY_RESPONSE,EXECUTE_REQUEST,EXECUTE_RESPONSE_OK,EXECUTE_RESPONSE_KO) VALUES ("ESP_TEMP","ESP8266 con software per temperatura", "4",
"{  
   ""id"":""dev['net_mac']"",
   ""type"":""action.devices.types.THERMOSTAT"",
   ""traits"":[  
      ""action.devices.traits.TemperatureSetting""
   ],
   ""name"":{  
      ""defaultNames"":[  
         ""ESP8266 con software per temperatura""
      ],
      ""name"":""dev['net_code']"",
      ""nicknames"":[  

      ]
   },
   ""willReportState"":true,
   ""attributes"": {
		  ""availableThermostatModes"": ""heat"",
		  ""queryOnlyTemperatureSetting"": true,
          ""thermostatTemperatureUnit"": ""C""
        },
   ""deviceInfo"":{  
      ""manufacturer"":""MSH"",
      ""model"":""1"",
      ""hwVersion"":""1.0"",
      ""swVersion"":""1.0""
   },
   ""customData"":{  
      ""mshType"":""dev['net_type']""
   }
}",
"{  
   ""requestId"":""data['requestId']"",
   ""payload"":{  
      ""devices"":{  
        ""data['inputs'][0]['payload']['devices'][0]['id']"":{  
			""thermostatMode"": ""heat"",
			""thermostatTemperatureSetpoint"": 23,
            ""online"":""cmd_ping(dev['net_ip'])['result']"",
			""thermostatTemperatureAmbient"": ""float(cmd_esp(dev['net_ip'], 'stato')['result'].split('C;')[0][:-1])"",
			""thermostatHumidityAmbient"": ""float(cmd_esp(dev['net_ip'], 'stato')['result'].split('C;')[1].replace('%', ''))""
        }
      }
   }
}",
"{  
   ""temperature"":""{'output': 'OK'}""
}",
"{  
   ""requestId"":""data['requestId']"",
   ""payload"":{  
      ""commands"":[  
         {  
            ""ids"":[  
               ""data['inputs'][0]['payload']['commands'][0]['devices'][0]['id']""
            ],
            ""status"":""SUCCESS"",
            ""states"":{
				""thermostatMode"": ""heat"",
				""thermostatTemperatureSetpoint"": 23,
				""online"":""cmd_ping(dev['net_ip'])['result']"",
				""thermostatTemperatureAmbient"": ""float(cmd_esp(dev['net_ip'], 'stato')['result'].split('C;')[0][:-1])"",
				""thermostatHumidityAmbient"": ""float(cmd_esp(dev['net_ip'], 'stato')['result'].split('C;')[1].replace('%', ''))""
            }
         }
      ]
   }
}",
"{  
   ""requestId"":""data['requestId']"",
   ""payload"":{  
      ""commands"":[  
         {  
            ""ids"":[  
               ""data['inputs'][0]['payload']['commands'][0]['devices'][0]['id']""
            ],
            ""status"":""ERROR"",
            ""errorCode"":""result['output']""
         }
      ]
   }
}");
INSERT INTO TB_NET_DEVICE_TYPE (TYPE_CODE,TYPE_DESCRIPTION,FUNCTION_CODE,SYNC_RESPONSE,QUERY_RESPONSE,EXECUTE_REQUEST,EXECUTE_RESPONSE_OK,EXECUTE_RESPONSE_KO) VALUES ("PS4","Sony Playstation 4", "5",
"{  
   ""id"":""dev['net_mac']"",
   ""type"":""action.devices.types.SWITCH"",
   ""traits"":[  
      ""action.devices.traits.OnOff""
   ],
   ""name"":{  
      ""defaultNames"":[  
         ""Sony Playstation 4""
      ],
      ""name"":""dev['net_code']"",
      ""nicknames"":[  

      ]
   },
   ""willReportState"":true,
   ""deviceInfo"":{  
      ""manufacturer"":""MSH"",
      ""model"":""1"",
      ""hwVersion"":""1.0"",
      ""swVersion"":""1.0""
   },
   ""customData"":{  
      ""mshType"":""dev['net_type']""
   }
}",
"{  
   ""requestId"":""data['requestId']"",
   ""payload"":{  
      ""devices"":{  
         ""data['inputs'][0]['payload']['devices'][0]['id']"":{  
            ""on"":""cmd_ping(dev['net_ip'])['result']"",
            ""online"":""cmd_ping(dev['net_ip'])['result']""
         }
      }
   }
}",
"{  
   ""on"":""{'output': 'OK'}""
}",
"{  
   ""requestId"":""data['requestId']"",
   ""payload"":{  
      ""commands"":[  
         {  
            ""ids"":[  
               ""data['inputs'][0]['payload']['commands'][0]['devices'][0]['id']""
            ],
            ""status"":""SUCCESS"",
            ""states"":{  
               ""on"":""cmd_ping(dev['net_ip'])['result']"",
               ""online"":""cmd_ping(dev['net_ip'])['result']""
            }
         }
      ]
   }
}",
"{  
   ""requestId"":""data['requestId']"",
   ""payload"":{  
      ""commands"":[  
         {  
            ""ids"":[  
               ""data['inputs'][0]['payload']['commands'][0]['devices'][0]['id']""
            ],
            ""status"":""ERROR"",
            ""errorCode"":""result['output']""
         }
      ]
   }
}");

INSERT INTO TB_NET_DEVICE_TYPE (TYPE_CODE,TYPE_DESCRIPTION,FUNCTION_CODE,SYNC_RESPONSE,QUERY_RESPONSE,EXECUTE_REQUEST,EXECUTE_RESPONSE_OK,EXECUTE_RESPONSE_KO) VALUES ("ESP_SWITCH","ESP8266 con software per esecuzione CMD", "4",
"{
   ""id"":""dev['net_mac']"",
   ""type"":""action.devices.types.SWITCH"",
   ""traits"":[
      ""action.devices.traits.OnOff""
   ],
   ""name"":{
      ""defaultNames"":[
         ""ESP8266 con software per esecuzione CMD""
      ],
      ""name"":""dev['net_code']"",
      ""nicknames"":[

      ]
   },
   ""willReportState"":true,
   ""deviceInfo"":{
      ""manufacturer"":""MSH"",
      ""model"":""1"",
      ""hwVersion"":""1.0"",
      ""swVersion"":""1.0""
   },
   ""customData"":{
      ""mshType"":""dev['net_type']""
   }
}",
"{
   ""requestId"":""data['requestId']"",
   ""payload"":{
      ""devices"":{
         ""data['inputs'][0]['payload']['devices'][0]['id']"":{
            ""on"":""cmd_esp(dev['net_ip'], 'stato')['result']"",
            ""online"":""cmd_ping(dev['net_ip'])['result']""
         }
      }
   }
}",
"{
   ""on"":""cmd_esp(dev['net_ip'], 'toggle')""
}",
"{
   ""requestId"":""data['requestId']"",
   ""payload"":{
      ""commands"":[
         {
            ""ids"":[
               ""data['inputs'][0]['payload']['commands'][0]['devices'][0]['id']""
            ],
            ""status"":""SUCCESS"",
            ""states"":{
               ""on"": ""cmd_esp(dev['net_ip'], 'stato')['result']"",
			   ""online"": ""cmd_ping(dev['net_ip'])['result']""
            }
         }
      ]
   }
}",
"{
   ""requestId"":""data['requestId']"",
   ""payload"":{
      ""commands"":[
         {
            ""ids"":[
               ""data['inputs'][0]['payload']['commands'][0]['devices'][0]['id']""
            ],
            ""status"":""ERROR"",
            ""errorCode"":""result['output']""
         }
      ]
   }
}");

INSERT INTO TB_NET_DEVICE_TYPE (TYPE_CODE,TYPE_DESCRIPTION,FUNCTION_CODE,SYNC_RESPONSE,QUERY_RESPONSE,EXECUTE_REQUEST,EXECUTE_RESPONSE_OK,EXECUTE_RESPONSE_KO) VALUES ("ESP_SMOKE","ESP8266 con software per temperatura", "4",
"{
   ""id"":""dev['net_mac']"",
   ""type"":""action.devices.types.SMOKE_DETECTOR"",
   ""traits"":[
      ""action.devices.traits.TemperatureSetting""
   ],
   ""name"":{
      ""defaultNames"":[
         ""Smoke Detector""
      ],
      ""name"":""dev['net_code']"",
      ""nicknames"":[

      ]
   },
   ""willReportState"":true,
   ""deviceInfo"":{
      ""manufacturer"":""MSH"",
      ""model"":""1"",
      ""hwVersion"":""1.0"",
      ""swVersion"":""1.0""
   },
   ""customData"":{
      ""mshType"":""dev['net_type']""
   }
}",
"{
   ""requestId"":""data['requestId']"",
   ""payload"":{
      ""devices"":{
        ""data['inputs'][0]['payload']['devices'][0]['id']"":{
			""thermostatMode"": ""heat"",
			""thermostatTemperatureSetpoint"": 23,
            ""online"":""cmd_ping(dev['net_ip'])['result']"",
			""thermostatTemperatureAmbient"": ""float(cmd_esp(dev['net_ip'], 'stato')['result'].split('C;')[0][:-1])"",
			""thermostatHumidityAmbient"": ""float(cmd_esp(dev['net_ip'], 'stato')['result'].split('C;')[1].replace('%', ''))""
        }
      }
   }
}",
"{
   ""temperature"":""{'output': 'OK'}""
}",
"{
   ""requestId"":""data['requestId']"",
   ""payload"":{
      ""commands"":[
         {
            ""ids"":[
               ""data['inputs'][0]['payload']['commands'][0]['devices'][0]['id']""
            ],
            ""status"":""SUCCESS"",
            ""states"":{
				""thermostatMode"": ""heat"",
				""thermostatTemperatureSetpoint"": 23,
				""online"":""cmd_ping(dev['net_ip'])['result']"",
				""thermostatTemperatureAmbient"": ""float(cmd_esp(dev['net_ip'], 'stato')['result'].split('C;')[0][:-1])"",
				""thermostatHumidityAmbient"": ""float(cmd_esp(dev['net_ip'], 'stato')['result'].split('C;')[1].replace('%', ''))""
            }
         }
      ]
   }
}",
"{
   ""requestId"":""data['requestId']"",
   ""payload"":{
      ""commands"":[
         {
            ""ids"":[
               ""data['inputs'][0]['payload']['commands'][0]['devices'][0]['id']""
            ],
            ""status"":""ERROR"",
            ""errorCode"":""result['output']""
         }
      ]
   }
}");


INSERT INTO TB_NET_DEVICE_TYPE (TYPE_CODE,TYPE_DESCRIPTION,FUNCTION_CODE,SYNC_RESPONSE,QUERY_RESPONSE,EXECUTE_REQUEST,EXECUTE_RESPONSE_OK,EXECUTE_RESPONSE_KO) VALUES ("ESP_LIGHT","ESP8266 con software per LED", "4",
"{
   ""id"":""dev['net_mac']"",
   ""type"":""action.devices.types.LIGHT"",
   ""traits"":[
      ""action.devices.traits.OnOff""
   ],
   ""name"":{
      ""defaultNames"":[
         ""ESP8266 con software per LED""
      ],
      ""name"":""dev['net_code']"",
      ""nicknames"":[]
   },
   ""willReportState"":true,
   ""deviceInfo"":{
      ""manufacturer"":""MSH"",
      ""model"":""1"",
      ""hwVersion"":""1.0"",
      ""swVersion"":""1.0""
   },
   ""customData"":{
      ""mshType"":""dev['net_type']""
   }
}",
"{
   ""requestId"":""data['requestId']"",
   ""payload"":{
      ""devices"":{
         ""data['inputs'][0]['payload']['devices'][0]['id']"":{
            ""on"":""cmd_esp(dev['net_ip'], 'stato')['result']"",
            ""online"":""cmd_ping(dev['net_ip'])['result']""
         }
      }
   }
}",
"{
   ""on"":""cmd_esp(dev['net_ip'], 'toggle')""
}",
"{
   ""requestId"":""data['requestId']"",
   ""payload"":{
      ""commands"":[
         {
            ""ids"":[
               ""data['inputs'][0]['payload']['commands'][0]['devices'][0]['id']""
            ],
            ""status"":""SUCCESS"",
            ""states"":{
               ""on"": ""cmd_esp(dev['net_ip'], 'stato')['result']"",
			   ""online"": ""cmd_ping(dev['net_ip'])['result']""
            }
         }
      ]
   }
}",
"{
   ""requestId"":""data['requestId']"",
   ""payload"":{
      ""commands"":[
         {
            ""ids"":[
               ""data['inputs'][0]['payload']['commands'][0]['devices'][0]['id']""
            ],
            ""status"":""ERROR"",
            ""errorCode"":""result['output']""
         }
      ]
   }
}");

INSERT INTO TB_NET_DEVICE_TYPE (TYPE_CODE,TYPE_DESCRIPTION,FUNCTION_CODE,SYNC_RESPONSE,QUERY_RESPONSE,EXECUTE_REQUEST,EXECUTE_RESPONSE_OK,EXECUTE_RESPONSE_KO) VALUES ("ESP_LOCK","ESP8266 con software per LOCK", "4",
"{
   ""id"":""dev['net_mac']"",
   ""type"":""action.devices.types.LOCK"",
   ""traits"":[
      ""action.devices.traits.LockUnlock""
   ],
   ""name"":{
      ""defaultNames"":[
         ""ESP8266 con software per LOCK""
      ],
      ""name"":""dev['net_code']"",
      ""nicknames"":[]
   },
   ""willReportState"":true,
   ""deviceInfo"":{
      ""manufacturer"":""MSH"",
      ""model"":""1"",
      ""hwVersion"":""1.0"",
      ""swVersion"":""1.0""
   },
   ""customData"":{
      ""mshType"":""dev['net_type']""
   }
}",
"{
   ""requestId"":""data['requestId']"",
   ""payload"":{
      ""devices"":{
         ""data['inputs'][0]['payload']['devices'][0]['id']"":{
			""isLocked"": ""cmd_esp(dev['net_ip'], 'stato')['result']"",
			""isJammed"": false,
            ""online"":""cmd_ping(dev['net_ip'])['result']""
         }
      }
   }
}",
"{
   ""lock"":""cmd_esp(dev['net_ip'], 'toggle')""
}",
"{
   ""requestId"":""data['requestId']"",
   ""payload"":{
      ""commands"":[
         {
            ""ids"":[
               ""data['inputs'][0]['payload']['commands'][0]['devices'][0]['id']""
            ],
            ""status"":""SUCCESS"",
            ""states"":{
				""isLocked"": ""cmd_esp(dev['net_ip'], 'stato')['result']"",
				""isJammed"": false,
				""online"": ""cmd_ping(dev['net_ip'])['result']""
            }
         }
      ]
   }
}",
"{
   ""requestId"":""data['requestId']"",
   ""payload"":{
      ""commands"":[
         {
            ""ids"":[
               ""data['inputs'][0]['payload']['commands'][0]['devices'][0]['id']""
            ],
            ""status"":""ERROR"",
            ""errorCode"":""result['output']""
         }
      ]
   }
}");

--DELETE FROM TB_NET_DEVICE_TYPE WHERE TYPE_CODE like 'ESP_RELE';
-- POPOLO TB_NET_DIZ_CMD
INSERT INTO TB_NET_DIZ_CMD (CMD_STR,CMD_NET_TYPE) VALUES ("online","NET");
INSERT INTO TB_NET_DIZ_CMD (CMD_STR,CMD_NET_TYPE) VALUES ("on","PCWIN");
INSERT INTO TB_NET_DIZ_CMD (CMD_STR,CMD_NET_TYPE) VALUES ("off","PCWIN");
INSERT INTO TB_NET_DIZ_CMD (CMD_STR,CMD_NET_TYPE) VALUES ("stato","AP");
INSERT INTO TB_NET_DIZ_CMD (CMD_STR,CMD_NET_TYPE) VALUES ("up","AP");
INSERT INTO TB_NET_DIZ_CMD (CMD_STR,CMD_NET_TYPE) VALUES ("down","AP");
INSERT INTO TB_NET_DIZ_CMD (CMD_STR,CMD_NET_TYPE) VALUES ("on","ESP_RELE");
INSERT INTO TB_NET_DIZ_CMD (CMD_STR,CMD_NET_TYPE) VALUES ("off","ESP_RELE");
INSERT INTO TB_NET_DIZ_CMD (CMD_STR,CMD_NET_TYPE) VALUES ("toggle","ESP_RELE");
INSERT INTO TB_NET_DIZ_CMD (CMD_STR,CMD_NET_TYPE) VALUES ("stato","ESP_RELE");
INSERT INTO TB_NET_DIZ_CMD (CMD_STR,CMD_NET_TYPE) VALUES ("read_dht","ESP_TEMP");
INSERT INTO TB_NET_DIZ_CMD (CMD_STR,CMD_NET_TYPE) VALUES ("toggle","ESP_SWITCH");
INSERT INTO TB_NET_DIZ_CMD (CMD_STR,CMD_NET_TYPE) VALUES ("read_mq2","ESP_SMOKE");
INSERT INTO TB_NET_DIZ_CMD (CMD_STR,CMD_NET_TYPE) VALUES ("toggle","ESP_LIGHT");
INSERT INTO TB_NET_DIZ_CMD (CMD_STR,CMD_NET_TYPE) VALUES ("stato","ESP_LIGHT");

-- POPOLO TB_STRING
INSERT INTO TB_STRING (LANGUAGE,VALUE,RESULT) VALUES ("IT","0","ON");
INSERT INTO TB_STRING (LANGUAGE,VALUE,RESULT) VALUES ("IT","1","OFF");
INSERT INTO TB_STRING (LANGUAGE,VALUE,RESULT) VALUES ("IT","2","Errore nel comando Ping!");
INSERT INTO TB_STRING (LANGUAGE,VALUE,RESULT) VALUES ("IT","3","Comando Wake-On-Lan OK!");
INSERT INTO TB_STRING (LANGUAGE,VALUE,RESULT) VALUES ("IT","4","Comando Wake-On-Lan KO!");
INSERT INTO TB_STRING (LANGUAGE,VALUE,RESULT) VALUES ("IT","5","Errore nel comando Wake-On-Lan!");
INSERT INTO TB_STRING (LANGUAGE,VALUE,RESULT) VALUES ("IT","6","Comando Shutdown OK!");
INSERT INTO TB_STRING (LANGUAGE,VALUE,RESULT) VALUES ("IT","7","Comando Shutdown KO!");
INSERT INTO TB_STRING (LANGUAGE,VALUE,RESULT) VALUES ("IT","8","Errore nel comando Shutdown!");
INSERT INTO TB_STRING (LANGUAGE,VALUE,RESULT) VALUES ("IT","9","Comando Radio OK!");
INSERT INTO TB_STRING (LANGUAGE,VALUE,RESULT) VALUES ("IT","12","Nessuna interfaccia WiFi rilevata");
INSERT INTO TB_STRING (LANGUAGE,VALUE,RESULT) VALUES ("IT","13","Credenzilai non valide");
INSERT INTO TB_STRING (LANGUAGE,VALUE,RESULT) VALUES ("IT","14","Errore nel comando Radio!");
INSERT INTO TB_STRING (LANGUAGE,VALUE,RESULT) VALUES ("IT","16","Errore Comando Esp Rele!");
INSERT INTO TB_STRING (LANGUAGE,VALUE,RESULT) VALUES ("IT","17","Compilazione OK!");
INSERT INTO TB_STRING (LANGUAGE,VALUE,RESULT) VALUES ("IT","18","Errore nella compilazione!");
INSERT INTO TB_STRING (LANGUAGE,VALUE,RESULT) VALUES ("IT","19","Upload OK!");
INSERT INTO TB_STRING (LANGUAGE,VALUE,RESULT) VALUES ("IT","20","Errore in upload!");
INSERT INTO TB_STRING (LANGUAGE,VALUE,RESULT) VALUES ("IT","21","Questa API ha bisogno di un payload");
INSERT INTO TB_STRING (LANGUAGE,VALUE,RESULT) VALUES ("IT","22","Il payload deve essere in formato JSON");
INSERT INTO TB_STRING (LANGUAGE,VALUE,RESULT) VALUES ("IT","23","Il campo %s è obbligatorio");
INSERT INTO TB_STRING (LANGUAGE,VALUE,RESULT) VALUES ("IT","24","Il campo %s deve assumere uno dei seguenti valori: ");
INSERT INTO TB_STRING (LANGUAGE,VALUE,RESULT) VALUES ("IT","25","Devi effettuare la login per utilizzare questa API");
INSERT INTO TB_STRING (LANGUAGE,VALUE,RESULT) VALUES ("IT","26","La funzione richiesta può essere eseguita solo da un ADMIN");
INSERT INTO TB_STRING (LANGUAGE,VALUE,RESULT) VALUES ("IT","27","Per l'operazione scelta è obbligatorio il campo ");
INSERT INTO TB_STRING (LANGUAGE,VALUE,RESULT) VALUES ("IT","28","Esiste già un utente con questo nome");
INSERT INTO TB_STRING (LANGUAGE,VALUE,RESULT) VALUES ("IT","29","Deve essere sempre presente almeno un utente ADMIN");
INSERT INTO TB_STRING (LANGUAGE,VALUE,RESULT) VALUES ("IT","30","Solo gli ADMIN possono modificare i ruoli");
INSERT INTO TB_STRING (LANGUAGE,VALUE,RESULT) VALUES ("IT","31","Il campo password deve avere una lunghezza di almeno 4 caratteri");
INSERT INTO TB_STRING (LANGUAGE,VALUE,RESULT) VALUES ("IT","32","Solo l'utente propietario può modificare la sua password");
INSERT INTO TB_STRING (LANGUAGE,VALUE,RESULT) VALUES ("IT","33","Nessun campo da aggiornare, i possibili campi da aggiornare sono: ");
INSERT INTO TB_STRING (LANGUAGE,VALUE,RESULT) VALUES ("IT","34","Il campo %s non può essere valorizzato con una stringa vuota");
INSERT INTO TB_STRING (LANGUAGE,VALUE,RESULT) VALUES ("IT","35","Esiste già un dispositivo con questo codice");
INSERT INTO TB_STRING (LANGUAGE,VALUE,RESULT) VALUES ("IT","36","Username non trovato");
INSERT INTO TB_STRING (LANGUAGE,VALUE,RESULT) VALUES ("IT","37","Password errata");
INSERT INTO TB_STRING (LANGUAGE,VALUE,RESULT) VALUES ("IT","38","Nessun dispositivo collegato");
INSERT INTO TB_STRING (LANGUAGE,VALUE,RESULT) VALUES ("IT","39","È necessario l'header ");
INSERT INTO TB_STRING (LANGUAGE,VALUE,RESULT) VALUES ("IT","40","L'header %s deve contenere un ");
INSERT INTO TB_STRING (LANGUAGE,VALUE,RESULT) VALUES ("IT","41","Il token fornito non è valido");
INSERT INTO TB_STRING (LANGUAGE,VALUE,RESULT) VALUES ("IT","42","Errore nel recupero della lista dei Wi-Fi!");
COMMIT;
