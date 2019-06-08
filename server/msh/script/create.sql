BEGIN TRANSACTION;
-- CREAZIONE TABELLE
CREATE TABLE "TB_NET_DEVICE_TYPE" ( `TYPE_CODE` TEXT NOT NULL UNIQUE, `TYPE_DESCRIPTION` TEXT DEFAULT '-', PRIMARY KEY(`TYPE_CODE`) );
CREATE TABLE "TB_NET_DEVICE" ( `NET_CODE` TEXT NOT NULL, `NET_DESC` TEXT, `NET_TYPE` TEXT NOT NULL, `NET_STATUS` TEXT DEFAULT '', `NET_LASTUPDATE` TEXT DEFAULT (datetime('now','localtime')), `NET_IP` TEXT DEFAULT '', `NET_MAC` TEXT NOT NULL DEFAULT '' UNIQUE, `NET_USER` TEXT, `NET_PSW` TEXT, `NET_MAC_INFO` TEXT DEFAULT '', PRIMARY KEY(`NET_MAC`) );
CREATE TABLE "TB_NET_DIZ_CMD" ( `CMD_STR` TEXT NOT NULL, `CMD_NET_TYPE` TEXT NOT NULL, `CMD_RESULT` TEXT );
CREATE TABLE "TB_RES_DECODE" ( `RES_DEVICE_TYPE` TEXT NOT NULL, `RES_COMMAND` TEXT NOT NULL, `RES_LANG` TEXT NOT NULL, `RES_VALUE` TEXT NOT NULL, `RES_RESULT` TEXT NOT NULL, `RES_STATE` TEXT NOT NULL, PRIMARY KEY(`RES_DEVICE_TYPE`,`RES_COMMAND`,`RES_LANG`,`RES_VALUE`) );
CREATE TABLE "TB_USER" ( `USERNAME` TEXT NOT NULL, `PASSWORD` TEXT, `ROLE` TEXT, PRIMARY KEY(`USERNAME`));
-- POPOLO TB_NET_DEVICE_TYPE
INSERT INTO TB_NET_DEVICE_TYPE (TYPE_CODE,TYPE_DESCRIPTION) VALUES ("NET","Generic Device");
INSERT INTO TB_NET_DEVICE_TYPE (TYPE_CODE,TYPE_DESCRIPTION) VALUES ("PCWIN","PC Windows");
INSERT INTO TB_NET_DEVICE_TYPE (TYPE_CODE,TYPE_DESCRIPTION) VALUES ("AP","Access Point UNIX based SSH Compatible");
INSERT INTO TB_NET_DEVICE_TYPE (TYPE_CODE,TYPE_DESCRIPTION) VALUES ("PS4","Sony Playstation 4");
INSERT INTO TB_NET_DEVICE_TYPE (TYPE_CODE,TYPE_DESCRIPTION) VALUES ("XBULB","Xiaomi Yeelight Bulb");
INSERT INTO TB_NET_DEVICE_TYPE (TYPE_CODE,TYPE_DESCRIPTION) VALUES ("ESP_RELE","ESP8266 con software per rele");
-- POPOLO TB_NET_DIZ_CMD
INSERT INTO TB_NET_DIZ_CMD (CMD_STR,CMD_NET_TYPE, CMD_RESULT) VALUES ("stato","NET","100");
INSERT INTO TB_NET_DIZ_CMD (CMD_STR,CMD_NET_TYPE, CMD_RESULT) VALUES ("stato","PCWIN","100");
INSERT INTO TB_NET_DIZ_CMD (CMD_STR,CMD_NET_TYPE, CMD_RESULT) VALUES ("on","PCWIN","102");
INSERT INTO TB_NET_DIZ_CMD (CMD_STR,CMD_NET_TYPE, CMD_RESULT) VALUES ("off","PCWIN","201");
INSERT INTO TB_NET_DIZ_CMD (CMD_STR,CMD_NET_TYPE, CMD_RESULT) VALUES ("stato","AP","100");
INSERT INTO TB_NET_DIZ_CMD (CMD_STR,CMD_NET_TYPE, CMD_RESULT) VALUES ("on","AP","102");
INSERT INTO TB_NET_DIZ_CMD (CMD_STR,CMD_NET_TYPE, CMD_RESULT) VALUES ("radio_stato","AP","300");
INSERT INTO TB_NET_DIZ_CMD (CMD_STR,CMD_NET_TYPE, CMD_RESULT) VALUES ("radio_up","AP","300");
INSERT INTO TB_NET_DIZ_CMD (CMD_STR,CMD_NET_TYPE, CMD_RESULT) VALUES ("radio_down","AP","300");
INSERT INTO TB_NET_DIZ_CMD (CMD_STR,CMD_NET_TYPE, CMD_RESULT) VALUES ("stato","ESP_RELE","100");
INSERT INTO TB_NET_DIZ_CMD (CMD_STR,CMD_NET_TYPE, CMD_RESULT) VALUES ("on","ESP_RELE","130");
INSERT INTO TB_NET_DIZ_CMD (CMD_STR,CMD_NET_TYPE, CMD_RESULT) VALUES ("off","ESP_RELE","130");
INSERT INTO TB_NET_DIZ_CMD (CMD_STR,CMD_NET_TYPE, CMD_RESULT) VALUES ("toggle","ESP_RELE","130");
INSERT INTO TB_NET_DIZ_CMD (CMD_STR,CMD_NET_TYPE, CMD_RESULT) VALUES ("stato_rele","ESP_RELE","130");
-- POPOLO TB_RES_DECODE
INSERT INTO TB_RES_DECODE (RES_DEVICE_TYPE,RES_COMMAND,RES_LANG,RES_VALUE,RES_RESULT,RES_STATE) VALUES ("NET","100","IT","-1","Errore nel comando Ping!","ERR");
INSERT INTO TB_RES_DECODE (RES_DEVICE_TYPE,RES_COMMAND,RES_LANG,RES_VALUE,RES_RESULT,RES_STATE) VALUES ("NET","100","IT","0","Ping OK!","ON");
INSERT INTO TB_RES_DECODE (RES_DEVICE_TYPE,RES_COMMAND,RES_LANG,RES_VALUE,RES_RESULT,RES_STATE) VALUES ("NET","100","IT","1","Ping KO!","OFF");
INSERT INTO TB_RES_DECODE (RES_DEVICE_TYPE,RES_COMMAND,RES_LANG,RES_VALUE,RES_RESULT,RES_STATE) VALUES ("NET","102","IT","0","Comando Wake-On-Lan OK!","Accensione");
INSERT INTO TB_RES_DECODE (RES_DEVICE_TYPE,RES_COMMAND,RES_LANG,RES_VALUE,RES_RESULT,RES_STATE) VALUES ("NET","102","IT","1","Comando Wake-On-Lan KO!","ERR");
INSERT INTO TB_RES_DECODE (RES_DEVICE_TYPE,RES_COMMAND,RES_LANG,RES_VALUE,RES_RESULT,RES_STATE) VALUES ("NET","102","IT","-1","Comando Wake-On-Lan Errore!","ERR");
INSERT INTO TB_RES_DECODE (RES_DEVICE_TYPE,RES_COMMAND,RES_LANG,RES_VALUE,RES_RESULT,RES_STATE) VALUES ("NET","201","IT","-1","Errore nel comando Shutdown!","ERR");
INSERT INTO TB_RES_DECODE (RES_DEVICE_TYPE,RES_COMMAND,RES_LANG,RES_VALUE,RES_RESULT,RES_STATE) VALUES ("NET","201","IT","0","Comando Shutdown OK!","Spegnimento");
INSERT INTO TB_RES_DECODE (RES_DEVICE_TYPE,RES_COMMAND,RES_LANG,RES_VALUE,RES_RESULT,RES_STATE) VALUES ("NET","201","IT","1","Comando Shutdown KO!","ERR");
INSERT INTO TB_RES_DECODE (RES_DEVICE_TYPE,RES_COMMAND,RES_LANG,RES_VALUE,RES_RESULT,RES_STATE) VALUES ("NET","300","IT","-2","No Interfaccia WiFi","ON Wifi ERR");
INSERT INTO TB_RES_DECODE (RES_DEVICE_TYPE,RES_COMMAND,RES_LANG,RES_VALUE,RES_RESULT,RES_STATE) VALUES ("NET","300","IT","-1","Errore nel comando Radio!","ERR");
INSERT INTO TB_RES_DECODE (RES_DEVICE_TYPE,RES_COMMAND,RES_LANG,RES_VALUE,RES_RESULT,RES_STATE) VALUES ("NET","300","IT","0","Comando Radio OK!","ON Wifi OFF");
INSERT INTO TB_RES_DECODE (RES_DEVICE_TYPE,RES_COMMAND,RES_LANG,RES_VALUE,RES_RESULT,RES_STATE) VALUES ("NET","300","IT","1","Comando Radio OK!","ON Wifi ON");
INSERT INTO TB_RES_DECODE (RES_DEVICE_TYPE,RES_COMMAND,RES_LANG,RES_VALUE,RES_RESULT,RES_STATE) VALUES ("NET","300","IT","2","Credenziali Invalide","ON Wifi ERR");
INSERT INTO TB_RES_DECODE (RES_DEVICE_TYPE,RES_COMMAND,RES_LANG,RES_VALUE,RES_RESULT,RES_STATE) VALUES ("NET","130","IT","0","Comando Esp Rele OK","ON");
INSERT INTO TB_RES_DECODE (RES_DEVICE_TYPE,RES_COMMAND,RES_LANG,RES_VALUE,RES_RESULT,RES_STATE) VALUES ("NET","130","IT","1","Comando Esp Rele OK","OFF");
INSERT INTO TB_RES_DECODE (RES_DEVICE_TYPE,RES_COMMAND,RES_LANG,RES_VALUE,RES_RESULT,RES_STATE) VALUES ("NET","130","IT","-1","Comando Esp Rele ERR","ERR");
COMMIT;









