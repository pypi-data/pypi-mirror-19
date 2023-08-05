import os, os.path
import tornado.ioloop
import tornado.web

from ...utils import get_root_dir


class BaseApplication(tornado.web.Application):
    def __init__(self, handlers, **kw):
        base_dir = get_root_dir()
        settings = dict(template_path=os.path.join(base_dir, "./template"),
                        static_path=os.path.join(base_dir, "./static"),
                        debug=False,
                        autoescape=None
                        )
        settings.update(kw)

        super(BaseApplication, self).__init__(handlers, **settings)

    def boot(self, port):
        self.listen(port)
        print 'application start at port %s' % port
        tornado.ioloop.IOLoop.instance().start()


class BaseAuthHandler(tornado.web.RequestHandler):
    def prepare(self):
        _auth = getattr(self, "_auth", None)
        if _auth is None:
            return
        auth = self.get_argument('auth', None)
        if auth is None:
            auth = self.request.headers.get("auth", None)

        if auth is None or auth != _auth:
            self.finish("auth fail")
