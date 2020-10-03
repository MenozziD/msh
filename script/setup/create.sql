BEGIN TRANSACTION;
-- CREAZIONE TABELLE
CREATE TABLE "TB_NET_DEVICE_TYPE" ( `TYPE_CODE` TEXT NOT NULL UNIQUE, `TYPE_DESCRIPTION` TEXT DEFAULT '-', `SYNC_RESPONSE` TEXT DEFAULT '' NOT NULL, `QUERY_RESPONSE` TEXT DEFAULT '' NOT NULL, `EXECUTE_REQUEST` TEXT DEFAULT '' NOT NULL, `EXECUTE_RESPONSE_OK` TEXT DEFAULT '' NOT NULL, `EXECUTE_RESPONSE_KO` TEXT DEFAULT '' NOT NULL, `MSH_COMMANDS` TEXT DEFAULT '' NOT NULL, PRIMARY KEY(`TYPE_CODE`) );
CREATE TABLE "TB_NET_DEVICE" ( `NET_CODE` TEXT NOT NULL, `NET_DESC` TEXT, `NET_TYPE` TEXT NOT NULL, `NET_LASTUPDATE` TEXT DEFAULT (datetime('now','localtime')), `NET_IP` TEXT DEFAULT '', `NET_MAC` TEXT NOT NULL DEFAULT '' UNIQUE, `NET_USER` TEXT, `NET_PSW` TEXT, `NET_MAC_INFO` TEXT DEFAULT '', PRIMARY KEY(`NET_MAC`) );
CREATE TABLE "TB_STRING" ( `LANGUAGE` TEXT NOT NULL, `VALUE` TEXT NOT NULL, `RESULT` TEXT NOT NULL, PRIMARY KEY(`LANGUAGE`,`VALUE`) );
CREATE TABLE "TB_USER" ( `USERNAME` TEXT NOT NULL, `PASSWORD` TEXT, `ROLE` TEXT, PRIMARY KEY(`USERNAME`));
CREATE TABLE "TB_WIFI" ( `SSID` TEXT NOT NULL, `PASSWORD` TEXT, PRIMARY KEY(`SSID`));
-- POPOLO TB_NET_DEVICE_TYPE
INSERT INTO TB_NET_DEVICE_TYPE (TYPE_CODE,TYPE_DESCRIPTION,SYNC_RESPONSE,QUERY_RESPONSE,EXECUTE_REQUEST,EXECUTE_RESPONSE_OK,EXECUTE_RESPONSE_KO,MSH_COMMANDS) VALUES ("NET","Generic Device",
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
}",
"{
    ""online"": ""cmd_ping(dev['net_ip'])""
}");
INSERT INTO TB_NET_DEVICE_TYPE (TYPE_CODE,TYPE_DESCRIPTION,SYNC_RESPONSE,QUERY_RESPONSE,EXECUTE_REQUEST,EXECUTE_RESPONSE_OK,EXECUTE_RESPONSE_KO,MSH_COMMANDS) VALUES ("PCWIN","PC Windows",
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
            ""online"":""True""
         }
      }
   }
}",
"{  
   ""on"":""cmd_pc('on', dev['net_mac'], dev['net_ip'], dev['net_usr'], dev['net_psw']) if parametri['on'] == 'ON' else cmd_pc('off', dev['net_mac'], dev['net_ip'], dev['net_usr'], dev['net_psw'], 'net rpc shutdown -I ' + dev['net_ip'] + ' -U ' + dev['net_usr'] + '%' + dev['net_psw'], 'succeeded')""
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
               ""online"":""True""
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
}",
"{
    ""online"": ""cmd_ping(dev['net_ip'])"",
    ""on"": ""cmd_pc('on', dev['net_mac'], dev['net_ip'], dev['net_usr'], dev['net_psw'])"",
    ""off"": ""cmd_pc('off', dev['net_mac'], dev['net_ip'], dev['net_usr'], dev['net_psw'], 'net rpc shutdown -I ' + dev['net_ip'] + ' -U ' + dev['net_usr'] + '%' + dev['net_psw'], 'succeeded')""
}");
INSERT INTO TB_NET_DEVICE_TYPE (TYPE_CODE,TYPE_DESCRIPTION,SYNC_RESPONSE,QUERY_RESPONSE,EXECUTE_REQUEST,EXECUTE_RESPONSE_OK,EXECUTE_RESPONSE_KO,MSH_COMMANDS) VALUES ("WIFI","Rete Wi-Fi",
"{
   ""id"":""dev['net_mac']"",
   ""type"":""action.devices.types.SWITCH"",
   ""traits"":[
      ""action.devices.traits.OnOff""
   ],
   ""name"":{
      ""defaultNames"":[
         ""Rete Wi-Fi""
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
            ""online"":""cmd_ping(dev['net_ip'])['result']"",
            ""on"":""cmd_radio_stato(dev['net_ip'], dev['net_usr'],  dev['net_psw'])['result']""
         }
      }
   }
}",
"{
   ""on"":""cmd_radio(dev['net_ip'], 'up', dev['net_usr'], dev['net_psw']) if parametri['on'] == 'ON' else cmd_radio(dev['net_ip'], 'down', dev['net_usr'], dev['net_psw'])""
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
               ""on"":""cmd_radio_stato(dev['net_ip'], dev['net_usr'], dev['net_psw'])['result']"",
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
}",
"{
    ""online"": ""cmd_ping(dev['net_ip'])"",
    ""stato"": ""cmd_radio_stato(dev['net_ip'], dev['net_usr'],  dev['net_psw'])"",
    ""up"": ""cmd_radio(dev['net_ip'], 'up', dev['net_usr'], dev['net_psw'])"",
    ""down"": ""cmd_radio(dev['net_ip'], 'down', dev['net_usr'], dev['net_psw'])""
}");
INSERT INTO TB_NET_DEVICE_TYPE (TYPE_CODE,TYPE_DESCRIPTION,SYNC_RESPONSE,QUERY_RESPONSE,EXECUTE_REQUEST,EXECUTE_RESPONSE_OK,EXECUTE_RESPONSE_KO,MSH_COMMANDS) VALUES ("AP","Access Point UNIX based SSH Compatible",
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
            ""on"":""cmd_ping(dev['net_ip'])['result']"",
            ""online"":""true""
         }
      }
   }
}",
"{
   ""on"":""cmd_reboot(dev['net_ip'], dev['net_usr'], dev['net_psw'])""
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
               ""online"":""true""
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
}",
"{
    ""online"": ""cmd_ping(dev['net_ip'])"",
    ""reboot"": ""cmd_reboot(dev['net_ip'], dev['net_usr'], dev['net_psw'])""
}");
INSERT INTO TB_NET_DEVICE_TYPE (TYPE_CODE,TYPE_DESCRIPTION,SYNC_RESPONSE,QUERY_RESPONSE,EXECUTE_REQUEST,EXECUTE_RESPONSE_OK,EXECUTE_RESPONSE_KO,MSH_COMMANDS) VALUES ("ESP_RELE","ESP8266 con software per rele",
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
}",
"{
    ""online"": ""cmd_ping(dev['net_ip'])"",
    ""stato"": ""cmd_esp(dev['net_ip'], 'stato')"",
    ""on"": ""cmd_esp(dev['net_ip'], 'toggle')"",
    ""off"": ""cmd_esp(dev['net_ip'], 'toggle')"",
    ""toggle"": ""cmd_esp(dev['net_ip'], 'toggle')""
}");
INSERT INTO TB_NET_DEVICE_TYPE (TYPE_CODE,TYPE_DESCRIPTION,SYNC_RESPONSE,QUERY_RESPONSE,EXECUTE_REQUEST,EXECUTE_RESPONSE_OK,EXECUTE_RESPONSE_KO,MSH_COMMANDS) VALUES ("ESP_TEMP","ESP8266 con software per temperatura",
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
			""thermostatTemperatureSetpoint"": ""float(cmd_esp(dev['net_ip'], 'read_dht')['result'].split('C;')[0][:-1])"",
            ""online"":""cmd_ping(dev['net_ip'])['result']"",
			""thermostatTemperatureAmbient"": ""float(cmd_esp(dev['net_ip'], 'read_dht')['result'].split('C;')[0][:-1])"",
			""thermostatHumidityAmbient"": ""float(cmd_esp(dev['net_ip'], 'read_dht')['result'].split('C;')[1].replace('%', ''))""
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
				""thermostatTemperatureSetpoint"": ""float(cmd_esp(dev['net_ip'], 'read_dht')['result'].split('C;')[0][:-1])"",
				""online"":""cmd_ping(dev['net_ip'])['result']"",
				""thermostatTemperatureAmbient"": ""float(cmd_esp(dev['net_ip'], 'read_dht')['result'].split('C;')[0][:-1])"",
				""thermostatHumidityAmbient"": ""float(cmd_esp(dev['net_ip'], 'read_dht')['result'].split('C;')[1].replace('%', ''))""
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
}",
"{
    ""online"": ""cmd_ping(dev['net_ip'])"",
    ""read_dht"": ""cmd_esp(dev['net_ip'], 'read_dht')""
}");
INSERT INTO TB_NET_DEVICE_TYPE (TYPE_CODE,TYPE_DESCRIPTION,SYNC_RESPONSE,QUERY_RESPONSE,EXECUTE_REQUEST,EXECUTE_RESPONSE_OK,EXECUTE_RESPONSE_KO,MSH_COMMANDS) VALUES ("PS4","Sony Playstation 4",
"{  
   ""id"":""dev['net_mac']"",
   ""type"":""action.devices.types.SETTOP"",
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
            ""on"":""cmd_ps4('stato')['result']"",
            ""online"":""cmd_ping(dev['net_ip'])['result']""
         }
      }
   }
}",
"{  
   ""on"":""cmd_ps4('toggle')""
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
               ""on"":""cmd_ps4('stato')['result']"",
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
}",
"{
    ""online"": ""cmd_ping(dev['net_ip'])"",
    ""stato"": ""cmd_ps4('stato')"",
    ""toggle"": ""cmd_ps4('toggle')""
}");
INSERT INTO TB_NET_DEVICE_TYPE (TYPE_CODE,TYPE_DESCRIPTION,SYNC_RESPONSE,QUERY_RESPONSE,EXECUTE_REQUEST,EXECUTE_RESPONSE_OK,EXECUTE_RESPONSE_KO,MSH_COMMANDS) VALUES ("ESP_SWITCH","ESP8266 con software per esecuzione CMD",
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
}",
"{
    ""online"": ""cmd_ping(dev['net_ip'])"",
    ""stato"": ""cmd_esp(dev['net_ip'], 'stato')"",
    ""toggle"": ""cmd_esp(dev['net_ip'], 'toggle')""
}");
INSERT INTO TB_NET_DEVICE_TYPE (TYPE_CODE,TYPE_DESCRIPTION,SYNC_RESPONSE,QUERY_RESPONSE,EXECUTE_REQUEST,EXECUTE_RESPONSE_OK,EXECUTE_RESPONSE_KO,MSH_COMMANDS) VALUES ("ESP_SMOKE","ESP8266 con software per temperatura",
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
}",
"{
    ""online"": ""cmd_ping(dev['net_ip'])"",
    ""read_mq2"": ""cmd_esp(dev['net_ip'], 'stato')""
}");
INSERT INTO TB_NET_DEVICE_TYPE (TYPE_CODE,TYPE_DESCRIPTION,SYNC_RESPONSE,QUERY_RESPONSE,EXECUTE_REQUEST,EXECUTE_RESPONSE_OK,EXECUTE_RESPONSE_KO,MSH_COMMANDS) VALUES ("ESP_LIGHT","ESP8266 con software per LED",
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
}",
"{
    ""online"": ""cmd_ping(dev['net_ip'])"",
    ""stato"": ""cmd_esp(dev['net_ip'], 'stato')"",
    ""toggle"": ""cmd_esp(dev['net_ip'], 'toggle')""
}");
INSERT INTO TB_NET_DEVICE_TYPE (TYPE_CODE,TYPE_DESCRIPTION,SYNC_RESPONSE,QUERY_RESPONSE,EXECUTE_REQUEST,EXECUTE_RESPONSE_OK,EXECUTE_RESPONSE_KO,MSH_COMMANDS) VALUES ("ESP_LOCK","ESP8266 con software per LOCK",
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
}",
"{
    ""online"": ""cmd_ping(dev['net_ip'])"",
    ""stato"": ""cmd_esp(dev['net_ip'], 'stato')"",
    ""toggle"": ""cmd_esp(dev['net_ip'], 'toggle')""
}");
INSERT INTO TB_NET_DEVICE_TYPE (TYPE_CODE,TYPE_DESCRIPTION,SYNC_RESPONSE,QUERY_RESPONSE,EXECUTE_REQUEST,EXECUTE_RESPONSE_OK,EXECUTE_RESPONSE_KO,MSH_COMMANDS) VALUES ("PCMAC","PC Apple",
"{
   ""id"":""dev['net_mac']"",
   ""type"":""action.devices.types.TV"",
   ""traits"":[
      ""action.devices.traits.OnOff""
   ],
   ""name"":{
      ""defaultNames"":[
         ""PC Mac""
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
            ""online"":""True""
         }
      }
   }
}",
"{
   ""on"":""cmd_pc('on', dev['net_mac'], dev['net_ip'], dev['net_usr'], dev['net_psw']) if parametri['on'] == 'ON' else cmd_pc('off', dev['net_mac'], dev['net_ip'], dev['net_usr'], dev['net_psw'], 'shutdown -s now', 'Shutdown NOW!')""
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
               ""online"":""True""
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
}",
"{
    ""online"": ""cmd_ping(dev['net_ip'])"",
    ""on"": ""cmd_pc('on', dev['net_mac'], dev['net_ip'], dev['net_usr'], dev['net_psw'])"",
    ""off"": ""cmd_pc('off', dev['net_mac'], dev['net_ip'], dev['net_usr'], dev['net_psw'], 'shutdown -s now', 'Shutdown NOW!')""
}");

INSERT INTO TB_NET_DEVICE_TYPE (TYPE_CODE,TYPE_DESCRIPTION,SYNC_RESPONSE,QUERY_RESPONSE,EXECUTE_REQUEST,EXECUTE_RESPONSE_OK,EXECUTE_RESPONSE_KO,MSH_COMMANDS) VALUES ("SCENA","Tipo Scena",
"{
   ""id"":""dev['net_mac']"",
   ""type"":""action.devices.types.SCENE"",
   ""traits"":[
      ""action.devices.traits.Scene""
   ],
   ""name"":{
      ""defaultNames"":[
         ""Scena""
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
            ""online"":""True""
         }
      }
   }
}",
"{
   ""deactivate"":""cmd_ping(dev['net_ip'])['result']""
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
            ""states"":{}
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
}",
"{}");

INSERT INTO TB_NET_DEVICE_TYPE (TYPE_CODE,TYPE_DESCRIPTION,SYNC_RESPONSE,QUERY_RESPONSE,EXECUTE_REQUEST,EXECUTE_RESPONSE_OK,EXECUTE_RESPONSE_KO,MSH_COMMANDS) VALUES ("PCLINUX","PC Linux",
"{
   ""id"":""dev['net_mac']"",
   ""type"":""action.devices.types.TV"",
   ""traits"":[
      ""action.devices.traits.OnOff""
   ],
   ""name"":{
      ""defaultNames"":[
         ""PC Mac""
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
            ""online"":""True""
         }
      }
   }
}",
"{
   ""on"":""cmd_pc('on', dev['net_mac'], dev['net_ip'], dev['net_usr'], dev['net_psw']) if parametri['on'] == 'ON' else cmd_pc('off', dev['net_mac'], dev['net_ip'], dev['net_usr'], dev['net_psw'], 'shutdown -h now', 'ORA')""
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
               ""online"":""True""
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
}",
"{
    ""online"": ""cmd_ping(dev['net_ip'])"",
    ""on"": ""cmd_pc('on', dev['net_mac'], dev['net_ip'], dev['net_usr'], dev['net_psw'])"",
    ""off"": ""cmd_pc('off', dev['net_mac'], dev['net_ip'], dev['net_usr'], dev['net_psw'], 'shutdown -h now', 'ORA')""
}");
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
INSERT INTO TB_STRING (LANGUAGE,VALUE,RESULT) VALUES ("IT","43","Comando ps4-waker OK!");
INSERT INTO TB_STRING (LANGUAGE,VALUE,RESULT) VALUES ("IT","44","Comando ps4-waker KO!");
COMMIT;
