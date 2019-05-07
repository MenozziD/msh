import webapp2
from webapp2 import WSGIApplication, Route
from paste import httpserver
import time
import os  # added
import json
import jinja2
from jinja2 import FileSystemLoader, Environment
from PIL import Image, ImageFilter
from os import system
from S import s

''' HOMEPAGE'''

class loadImage(webapp2.RequestHandler):

    def get(self):
        SUBNAME = "loadImage_get"
        path=str(os.path.dirname(os.path.abspath(__file__)))+"/webui/image/"
        try:
            print "Image"
            nfile = self.request.GET['file']
            file = open(path+nfile, "rb")
            html= file.read()
            file.close()
            self.response.headers['Content-Type'] = 'image/jpeg'
            self.response.body_file.write(html)
            file.close()
        except Exception as e:
            print "Error-%s:%s " % (SUBNAME, e)


class loadStyle(webapp2.RequestHandler):

    def get(self):
        SUBNAME = "loadStyle_get"
        path = str(os.path.dirname(os.path.abspath(__file__))) + "/webui/style/"
        try:
            print "Style"
            nfile = self.request.GET['file']
            file = open(path+nfile, "r")
            html= file.read()
            file.close()
            self.response.headers['Content-Type'] = 'text/css'
            self.response.write(html)
        except Exception as e:
            print "Error-%s:%s " % (SUBNAME, e)

''' PAGINE'''
class Home(webapp2.RequestHandler):
    def render_from_template(self):
        loader = FileSystemLoader(str(os.path.dirname(os.path.abspath(__file__))) + "/webui/")
        env = Environment(loader=loader)
        template = env.get_template('index.html')
        return template.render()

    def get(self):
        SUBNAME = "home_get"
        try:
            self.response.out.write(self.render_from_template())
        except Exception as e:
            print "Error-%s:%s " % (SUBNAME, e)


class Realtime(webapp2.RequestHandler):

    def render_from_template(self):
        loader = FileSystemLoader(str(os.path.dirname(os.path.abspath(__file__))) + "/webui/")
        env = Environment(loader=loader)
        template = env.get_template('realtime.html')
        return template.render()

    def get(self):
        SUBNAME = "realtime_get"
        try:
            self.response.out.write(self.render_from_template())
        except Exception as e:
            print "Error-%s:%s " % (SUBNAME, e)

class RealtimeUpdate(webapp2.RequestHandler):
    def get(self):
        SUBNAME = "realtimeupd_get"
        result = ''
        try:
            result = s.realtimeupd()
        # ERRORE!
        except Exception as e:
            print "Error-%s:%s " % (SUBNAME, e)

        finally:
            # PREPARO E INVIO RESPONSE
            self.response.headers.add('Access-Control-Allow-Origin', '*')  # PER PROBLEMA CORS
            self.response.write(result)

class rtNRF(webapp2.RequestHandler):
    def get(self):
        SUBNAME = "rtNRF_get"
        result = ''
        try:
            result = s.rtNRF()
        # ERRORE!
        except Exception as e:
            print "Error-%s:%s " % (SUBNAME, e)

        finally:
            # PREPARO E INVIO RESPONSE
            self.response.headers.add('Access-Control-Allow-Origin', '*')  # PER PROBLEMA CORS
            self.response.write(result)

class rtService(webapp2.RequestHandler):
    def get(self):
        SUBNAME = "rtNRFService_get"
        result = ''
        try:
            result = s.rtService()
        # ERRORE!
        except Exception as e:
            print "Error-%s:%s " % (SUBNAME, e)

        finally:
            # PREPARO E INVIO RESPONSE
            self.response.headers.add('Access-Control-Allow-Origin', '*')  # PER PROBLEMA CORS
            self.response.write(result)

class rtNET(webapp2.RequestHandler):
    def get(self):
        SUBNAME = "rtNET_get"
        result = ''
        try:
            result = s.rtNET()
        # ERRORE!
        except Exception as e:
            print "Error-%s:%s " % (SUBNAME, e)

        finally:
            # PREPARO E INVIO RESPONSE
            self.response.headers.add('Access-Control-Allow-Origin', '*')  # PER PROBLEMA CORS
            self.response.write(result)

class test_syn(webapp2.RequestHandler):

    def render_from_template(self):
        loader = FileSystemLoader(str(os.path.dirname(os.path.abspath(__file__))) + "/webui/")
        env = Environment(loader=loader)
        template = env.get_template('syn.html')
        return template.render()

    def get(self):
        SUBNAME = "home_get"
        try:
            self.response.out.write(self.render_from_template())
        except Exception as e:
            print "Error-%s:%s " % (SUBNAME, e)

'''
html=
<!DOCTYPE html>
<html>
   <head>
      <title>HTML area Tag</title>
   </head>

   <body>

      <map name = "lessons">
         <area shape = "poly" coords = "74,0,113,29,98,72,52,72,38,27"
            href = "/perl/index.htm" alt = "Perl Tutorial" target = "_blank" />
         <area shape = "rect" coords = "22,83,126,125" alt = "HTML Tutorial"
            href = "/html/index.htm" target = "_blank" />
         <area shape = "circle" coords = "73,168,32" alt = "PHP Tutorial"
            href = "/php/index.htm" target = "_blank" />
      </map>






class page_nrf24(webapp2.RequestHandler):

    def render_from_template(self):
        loader = FileSystemLoader(s.getPathWEBUI())
        env = Environment(loader=loader)
        template = env.get_template('nrf24.html')
        return template.render()

    def get(self):
        SUBNAME = "page_nrf24_get"
        try:
            self.response.out.write(self.render_from_template())
        except Exception as e:
            print "Error-%s:%s " % (SUBNAME, e)



class nrf24cmd(webapp2.RequestHandler):

    def get(self):
        key = self.request.GET['k']
        cmd = self.request.GET['s']
        self.response.headers.add('Access-Control-Allow-Origin', '*')  # PER PROBLEMA CORS
        self.response.write(s.nrf24cmd(key, cmd))


class realtimeupd(webapp2.RequestHandler):
    def get(self):
        SUBNAME = "realtimeupd_get"

        db = None
        rows = ""
        row = ""
        strHtml = ""
        # ESEGUO SCRIPT RT.PY
        system("python /home/pi/Desktop/BotSonja/rt.py")
        try:
            # LEGGO ELENCO TB_REALTIME
            db = DB_Manager.openDB(db, 'system.db')
            rows = DB_Manager.SELECT_TB_SYS_REALTIME_INFO(db)
            # CREO HTML DA INVIARE
            if rows != "":
                for row in rows:
                    strHtml = strHtml + "<tr>"
                    strHtml = strHtml + "<td><a onclick='loadPanel(createPanel," + chr(34) + row[1] + chr(34) + ")'> " + "<b>" + row[1] + "</b>" + " </a></td>"
                    strHtml = strHtml + "<td>%s</td> " % row[2]
                    strHtml = strHtml + "<td>%s</td> " % row[4]
                    strHtml = strHtml + "</tr>"

        # ERRORE!
        except Exception as e:
            print "Error-%s:%s " % (SUBNAME, e)

        finally:
            # PREPARO E INVIO RESPONSE
            self.response.headers.add('Access-Control-Allow-Origin', '*')  # PER PROBLEMA CORS
            self.response.write(strHtml)
            DB_Manager.closeDB(db)


class httpcmd(webapp2.RequestHandler):
    def get(self):
        try:
            mex = self.request.GET['comando'] + chr(10)
            mex = mex + "Hello"
            self.response.write(mex)
        except Exception as e:
            print e


class serviceCommand(webapp2.RequestHandler):

    def get(self):
        db = None
        res = '-'
        r = ''
        r2 = ''
        url = self.request.url
        s = self.request.GET['s']
        c = self.request.GET['c']
        system("sudo service %s %s" % (s, c))


class serviceCommandApp(webapp2.RequestHandler):

    def get(self):
        url = self.request.url
        service = self.request.GET['s']
        command = self.request.GET['c']
        # PREPARO E INVIO RESPONSE
        self.response.headers.add('Access-Control-Allow-Origin', '*')  # PER PROBLEMA CORS
        self.response.write(s.servicecmd(service, command))


class scriptCommand(webapp2.RequestHandler):

    def get(self):
        SUBNAME = "scriptCommand_get"
        db = None
        res = '-'
        r = ''
        r2 = ''
        url = self.request.url
        s = self.request.GET['s']
        c = self.request.GET['c']
        cmd = "bash /home/pi/Desktop/BotSonja/support/%s.sh %s >o.txt" % (s, c)
        print cmd
        system(cmd)
        path = "/home/pi/Desktop/BotSonja/support/o.txt"
        try:
            file = open(path, "r")
            res = file.read()
            file.close()
        except Exception as e:
            print "Error-%s:%s " % (SUBNAME, e)

        self.response.headers.add('Access-Control-Allow-Origin', '*')  # PER PROBLEMA CORS
        self.response.write(res)


class servicePanel(webapp2.RequestHandler):

    def get(self):
        SUBNAME = "servicePanel"

        db = None
        rows = ""
        strHtml = ""
        try:

            url = self.request.url
            servizio = self.request.GET['s']

            # LEGGO ELENCO TB_REALTIME
            db = DB_Manager.openDB(db, 'system.db')
            rows = DB_Manager.SELECT_ONE_TB_SYS_REALTIME_INFO(db, servizio)
            for row in rows:
                # CREO HTML DA INVIARE
                strHtml = strHtml + "<div class ='panel panel-default' >"
                strHtml = strHtml + "<div id='nomeServizio' class='panel-heading'><font size='5'><b>%s</b></font></div>" % \
                          row[1]
                strHtml = strHtml + "<div class='panel-body' align='left'>"
                strHtml = strHtml + "<h4>STATO: %s</h4>" % row[2]
                strHtml = strHtml + "<h5>ULTIMO AGGIORNAMENTO: %s</h5>" % row[3]
                strHtml = strHtml + "<input type='button' onclick='sendCommand(1)' value='START' style='margin:2%;' />"
                strHtml = strHtml + "<input type='button' onclick='sendCommand(2)' value='STOP' style='margin:2%;' />"
                strHtml = strHtml + "<input type='button' onclick='sendCommand(3)' value='RESTART' style='margin:2%;' />"

            strHtml = strHtml + "</div>"
            strHtml = strHtml + "</div>"

        # ERRORE!
        except Exception as e:
            print "Error-%s:%s " % (SUBNAME, e)

        finally:
            # PREPARO E INVIO RESPONSE
            self.response.headers.add('Access-Control-Allow-Origin', '*')  # PER PROBLEMA CORS
            self.response.write(strHtml)
            DB_Manager.closeDB(db)
routes = [
    Route('/', page_home),  # HOMEPAGE
    Route('/realtime', page_realtime),
    Route('/realtimeupd', realtimeupd),
    Route('/nrf24', page_nrf24),
    Route('/nrfcmd', nrf24cmd),
    Route('/httpcmd', httpcmd),
    Route('/style', loadStyle),
    Route('/image', loadImage),
    Route('/servicecmd', serviceCommand),
    Route('/scriptcmd', scriptCommand),
    Route('/servicepanel', servicePanel),
]

'''

class panel(webapp2.RequestHandler):

    def get(self):
        SUBNAME = "servicePanel"

        db = None
        rows = ""
        strHtml = ""
        try:

            url = self.request.url
            tipo = self.request.GET['t'] #nrf;net;sys
            servizio = self.request.GET['s']
            strHtml=s.createPanel(tipo,servizio)

        # ERRORE!
        except Exception as e:
            print "Error-%s:%s " % (SUBNAME, e)

        finally:
            # PREPARO E INVIO RESPONSE
            self.response.headers.add('Access-Control-Allow-Origin', '*')  # PER PROBLEMA CORS
            self.response.write(strHtml)



routes = [
    Route('/', Home),  # HOMEPAGE
    Route('/style', loadStyle),
    Route('/image', loadImage),
    Route('/realtime', Realtime),
    Route('/realtimeupd', RealtimeUpdate),
    Route('/tsvg', test_syn),
    Route('/rtnrf', rtNRF),
    Route('/rtnet', rtNET),
    Route('/rtservice', rtService),
    Route('/panel', panel)

]
app = webapp2.WSGIApplication(routes, debug=True)


def main():
    httpserver.serve(app, host='192.168.1.111', port='65265')


if __name__ == '__main__':
    main()

