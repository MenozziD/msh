import webapp2
import time
from webapp2 import WSGIApplication, Route
from paste import httpserver
import os #added
import jinja2
from jinja2 import FileSystemLoader, Environment
from PIL import Image, ImageFilter
from os import system
from S import s


class check(webapp2.RequestHandler):
    sw_name = 'APP'
    def get(self):
        db=None
        result="OK"
        self.response.headers.add('Access-Control-Allow-Origin', '*')  # PER PROBLEMA CORS
        self.response.write(result)

class nrf24cmd_list(webapp2.RequestHandler):
    sw_name = 'APP'
    def get(self):
        db=None
        result=''
        key=self.request.GET['k']
        result=s.nrf24cmdlist(key,self.sw_name)
        self.response.headers.add('Access-Control-Allow-Origin', '*')  # PER PROBLEMA CORS
        self.response.write(result)

#http://192.168.1.111:65177/nrf?c=off&k=M7ItIvutHpNqc17
class nrf24cmd(webapp2.RequestHandler):
    sw_name = 'APP'
    def get(self):
        db=None
        result=''
        key=self.request.GET['k']
        cmd = self.request.GET['s']
        result=s.nrf24cmd(key,self.sw_name,cmd)
        self.response.headers.add('Access-Control-Allow-Origin', '*')  # PER PROBLEMA CORS
        self.response.write(result)

class service_list(webapp2.RequestHandler):
    sw_name = 'APP'
    def get(self):
        db=None
        result=''
        key=self.request.GET['k']
        result=s.servicelist(key,self.sw_name)
        self.response.headers.add('Access-Control-Allow-Origin', '*')  # PER PROBLEMA CORS
        self.response.write(result)

#http://192.168.1.111:65177/servicecmd?s=on&c=status&k=M7ItIvutHpNqc17
class servicecmd(webapp2.RequestHandler):
    sw_name = 'APP'
    def get(self):
        db=None
        result=''
        key=self.request.GET['k']
        service = self.request.GET['s']
        cmd = self.request.GET['c']
        result=s.servicecmd(service,cmd,key,self.sw_name)
        self.response.headers.add('Access-Control-Allow-Origin', '*')  # PER PROBLEMA CORS
        self.response.write(result)

#http://snjsys.ddns.net:65207/pcctrl?c=on&k=g9yyULXKIHWmiXY
class pcctrl(webapp2.RequestHandler):
    sw_name = 'APP'
    def get(self):
        result=''
        url = self.request.url
        k = self.request.GET['k']
        c = self.request.GET['c']
        result=s.pcctrl(k,self.sw_name,c)
        self.response.headers.add('Access-Control-Allow-Origin', '*')  # PER PROBLEMA CORS
        self.response.write(result)

#http://192.168.1.111:65177/apwifictrl?c=off&k=M7ItIvutHpNqc17
class apwifictrl(webapp2.RequestHandler):
    sw_name = 'APP'
    def get(self):
        result=''
        url = self.request.url
        k = self.request.GET['k']
        c = self.request.GET['c']
        result=s.apwifictrl(k,self.sw_name,c)
        self.response.headers.add('Access-Control-Allow-Origin', '*')  # PER PROBLEMA CORS
        self.response.write(result)

#http://192.168.1.111:65177/presenze_all?k=M7ItIvutHpNqc17
class presenze_all(webapp2.RequestHandler):
    sw_name = 'APP'
    def get(self):
        db=None
        result=''
        key=self.request.GET['k']
        result=s.viewAllPresence(key,self.sw_name)
        self.response.headers.add('Access-Control-Allow-Origin', '*')  # PER PROBLEMA CORS
        self.response.write(result)

#http://192.168.1.111:65177/yds?u=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DmDPul7F3otI&k=M7ItIvutHpNqc17
class youtube_download(webapp2.RequestHandler):
    sw_name = 'APP'
    def get(self):
        result=''
        key=self.request.GET['k']
        url=self.request.GET['u']
        result=s.youtube_download(key,self.sw_name,url)
        self.response.headers.add('Access-Control-Allow-Origin', '*')  # PER PROBLEMA CORS
        self.response.write(result)

#http://192.168.1.111:65177/netscan?k=M7ItIvutHpNqc17
class net_scan(webapp2.RequestHandler):
    sw_name = 'APP'
    def get(self):
        result=''
        key=self.request.GET['k']
        result=s.nmapScan(key,self.sw_name)
        self.response.headers.add('Access-Control-Allow-Origin', '*')  # PER PROBLEMA CORS
        self.response.write(result)

#http://192.168.1.111:65177/net_scan_db?k=M7ItIvutHpNqc17
class net_scan_db(webapp2.RequestHandler):
    sw_name = 'APP'
    def get(self):
        result=''
        key=self.request.GET['k']
        result=s.netscan(key,self.sw_name)
        self.response.headers.add('Access-Control-Allow-Origin', '*')  # PER PROBLEMA CORS
        self.response.write(result)
'''

class loadCard(webapp2.RequestHandler):

    def get(self):
        SUBNAME = "loadCard_get"
        path="/home/pi/Desktop/BotSonja/GreyMatter/memory/card/"
        try:
            print "Image"
            nfile = self.request.GET['file']
            file = open(path+nfile+".jpg", "rb")
            html= file.read()
            file.close()
            self.response.headers['Content-Type'] = 'image/jpeg'
            self.response.body_file.write(html)
            file.close()
        except Exception as e:
            print "Error-%s:%s " % (SUBNAME, e)

class bulbToggle(webapp2.RequestHandler):
    def get(self):
        SUBNAME = "bulbToggle_get"

        try:
            bulb.cmd_toggle()

        # ERRORE!
        except Exception as e:
            print "Error-%s:%s " % (SUBNAME, e)


class KeyValue(webapp2.RequestHandler):

    def get(self):
        db = None
        SUBNAME = "getKeyValue"
        db = DB_Manager.openDB(db, 'system.db')
        result = ''
        try:
            print "Key-Value"
            s = self.request.GET['key']
            result = DB_Manager.SELECT_ONE_TB_SONJA_KEY_VALUE(db, s)

        except Exception as e:
            print "Error-%s:%s " % (SUBNAME, e)

        finally:
            # PREPARO E INVIO RESPONSE
            self.response.headers.add('Access-Control-Allow-Origin', '*')  # PER PROBLEMA CORS
            self.response.write(result)
            DB_Manager.closeDB(db)

class KeyAdd(webapp2.RequestHandler):

    def get(self):
        db = None
        SUBNAME = "getKeyAdd"
        db = DB_Manager.openDB(db, 'system.db')
        result = ''
        try:
            print "Key-Value"
            n = self.request.GET['n']
            v = self.request.GET['v']
            result = DB_Manager.insert_TB_SONJA_KEY(db, n, v)
            if result == "":
                result = "Chiave " + n + " salvata"

        except Exception as e:
            print "Error-%s:%s " % (SUBNAME, e)

        finally:
            # PREPARO E INVIO RESPONSE
            self.response.headers.add('Access-Control-Allow-Origin', '*')  # PER PROBLEMA CORS
            self.response.write(result)
            DB_Manager.closeDB(db)


class KeyList(webapp2.RequestHandler):

    def get(self):
        db = None
        SUBNAME = "getKeyList"
        db = DB_Manager.openDB(db, 'system.db')
        result = ''
        rows = ''
        try:
            print "Key-List"
            rows = DB_Manager.SELECT_TB_SONJA_KEY_NOME(db)
            if rows != "":
                for row in rows:
                    result = result + row[0] + ";"

        except Exception as e:
            print "Error-%s:%s " % (SUBNAME, e)

        finally:
            # PREPARO E INVIO RESPONSE
            self.response.headers.add('Access-Control-Allow-Origin', '*')  # PER PROBLEMA CORS
            self.response.write(result)
            DB_Manager.closeDB(db)


class HomeList(webapp2.RequestHandler):

    def get(self):
        db = None
        SUBNAME = "getHomeList"
        db = DB_Manager.openDB(db, 'system.db')
        result = ''
        rows = ''
        try:
            print "Home-List"
            rows = DB_Manager.select_TB_NRF_DIZ_CMD_LIST(db)
            if rows != "":
                for row in rows:
                    result = result + row[0] + ";"

        except Exception as e:
            print "Error-%s:%s " % (SUBNAME, e)

        finally:
            # PREPARO E INVIO RESPONSE
            self.response.headers.add('Access-Control-Allow-Origin', '*')  # PER PROBLEMA CORS
            self.response.write(result)
            DB_Manager.closeDB(db)


'''

routes=[
    Route('/check',check),
    Route('/nrf',nrf24cmd),
    Route('/nrf24cmdlist',nrf24cmd_list),
    Route('/servicelist',service_list),
    Route('/servicecmd',servicecmd),
    Route('/pcctrl',pcctrl),
    Route('/presenze_all',presenze_all),
    Route('/yds',youtube_download),
    Route('/netscan',net_scan),
    Route('/apwifictrl',apwifictrl),
    Route('/netscandb',net_scan_db)
  ]


app = webapp2.WSGIApplication(routes, debug=True)


def main():
    httpserver.serve(app, host='192.168.1.111', port='65177')

if __name__ == '__main__':
    main()
