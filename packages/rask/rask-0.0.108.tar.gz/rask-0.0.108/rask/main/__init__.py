from rask.base import Base
from rask.options import define,options,parse_command_line
from rask.parser.utcode import UTCode
from tornado.web import Application

__all__ = ['Main']

class Main(Base):
    __http__ = None
    __http_routes__ = []
    __options__ = {
        'rmq':{
            'channel':{
                'prefetch':10
            }
        }
    }

    def __init__(self):
        self.before()
        self.setup()
        self.ioengine.loop.add_callback(self.after)
        self.ioengine.loop.add_callback(self.http)
        self.ioengine.start()

    @property
    def services(self):
        try:
            assert self.__services
        except (AssertionError,AttributeError):
            self.__services = {}
        except:
            raise
        return self.__services

    @property
    def utcode(self):
        try:
            assert self.__utcode
        except (AssertionError,AttributeError):
            self.__utcode = UTCode()
        except:
            raise
        return self.__utcode

    def after(self):
        pass

    def before(self):
        pass

    def http(self):
        try:
            assert self.__http_routes__
        except AssertionError:
            return False
        except:
            raise
        else:
            self.__http__ = Application(self.__http_routes__,autoreload=options.autoreload)
            self.ioengine.loop.add_callback(
                self.__http__.listen,
                port=options.http_port,
                xheaders=True
            )
            self.log.info('HTTP Server - %s' % options.http_port)
        return True

    def setup(self):
        define('autoreload',default=False)
        define('http_port',default=8088)
        define('rask',default=self.__options__)
        define('raven_color',default=True)
        define('raven_color_fmt',default='%(log_color)s%(levelname)1.1s %(asctime)s %(name)s%(reset)s %(message)s')
        define('raven_no_color_fmt',default='%(levelname)1.1s %(asctime)s %(name)s %(message)s')

        parse_command_line()
        return True
