from controller import BaseHandler
from logging import info, exception
from mimetypes import MimeTypes


class Index(BaseHandler):
    def get(self):
        info("%s %s", self.request.method, self.request.url)
        self.redirect('/static/page/index.html')
        info("RESPONSE CODE: %s to %s", self.response.status, self.response.headers['Location'])


class Icon(BaseHandler):
    def get(self):
        info("%s %s", self.request.method, self.request.url)
        self.redirect('/static/image/hub.png')
        info("RESPONSE CODE: %s to %s", self.response.status, self.response.headers['Location'])


class Static(BaseHandler):
    def get(self, filename):
        try:
            if self.session.get('user') is not None or filename.find("login") > 0 or filename.find("hub.png") > 0:
                path_ui = 'webui/'
                info("%s %s", self.request.method, self.request.url)
                f = open(path_ui + filename, 'rb')
                self.response.body = f.read()
                f.close()
                self.response.headers['Content-Type'] = MimeTypes().guess_type(filename)[0]
                info("RESPONSE CODE: %s", self.response.status)
                info("RESPONSE PAYLOAD: %s%s", path_ui, filename)
            else:
                self.redirect('/static/page/login.html')
                info("RESPONSE CODE: %s to %s", self.response.status, self.response.headers['Location'])
        except Exception:
            exception("Exception")


def handle_error(request, response, excep):
    try:
        path_error = 'webui/page/error/'
        error_code = '500'
        class_error = {
            '404': '<class \'webob.exc.HTTPNotFound\'>',
            '405': '<class \'webob.exc.HTTPMethodNotAllowed\'>'
        }
        for code, value in class_error.items():
            if str(value) == str(type(excep)):
                error_code = code
        if error_code != '500':
            info("%s %s", request.method, request.url)
        exception(excep)
        f = open(path_error + error_code + '.html', 'r')
        response.write(f.read())
        response.set_status(int(error_code))
        f.close()
        info("RESPONSE CODE: %s", response.status)
        info("RESPONSE PAYLOAD: %s%s.html", path_error, error_code)
    except Exception:
        exception("Exception")
