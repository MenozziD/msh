from webapp3 import RequestHandler
from logging import info, exception
from json import loads
from oauth2client.client import OAuth2WebServerFlow
from module.xml_reader import XmlReader
from urllib import request
from module.dbmanager import DbManager


class Login(RequestHandler):
    def get(self):
        info("%s %s", self.request.method, self.request.url)
        flow = OAuth2WebServerFlow(client_id=XmlReader.settings['oauth_google']['client_id'],
                                   client_secret=XmlReader.settings['oauth_google']['client_secret'],
                                   scope="https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email",
                                   redirect_uri=XmlReader.settings['oauth_google']['url_callback'])
        code = self.request.get("code")
        try:
            if code != "":
                credentials = flow.step2_exchange(code)
                url = "https://www.googleapis.com/oauth2/v1/userinfo?access_token=" + credentials.access_token
                response = request.urlopen(url)
                res = str(response.read())[2:-3].replace("\\n", "")
                info(res)
                data = loads(res)
                nome = data['given_name']
                cognome = data['family_name']
                mail = data['email']
                info("Tentaivo di login da %s %s %s", nome, cognome, mail)
                DbManager()
                user = DbManager.select_tb_user_from_mail(mail)
                if len(user) == 1:
                    info("Utente presente sul database")
                    DbManager.update_tb_user(mail, token_google=credentials.access_token)
                    self.redirect("/")
                else:
                    info("Utente non presente sul database")
            else:
                auth_url = flow.step1_get_authorize_url()
                self.redirect(auth_url)
        except Exception:
            exception("Exception")
