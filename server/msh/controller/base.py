from webapp3 import RequestHandler, cached_property
from webapp3_extras import sessions


class BaseHandler(RequestHandler):
    def dispatch(self):
        self.session_store = sessions.get_store(request=self.request)
        try:
            RequestHandler.dispatch(self)
        finally:
            self.session_store.save_sessions(self.response)

    @cached_property
    def session(self):
        return self.session_store.get_session()
