import collections
from framepy import logs
from framepy import beans
from framepy import web
from framepy import _configuration
import logging
import cherrypy
import pkgutil

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 8000
Mapping = collections.namedtuple('Mapping', ['bean', 'path'])

log = logging.getLogger('framepy_logger')


class Context(object):
    def __init__(self, entries):
        self.__dict__.update(entries)


class BaseBean(object):
    def __init__(self):
        self.context = None

    def initialize(self, context):
        self.context = context


def _setup_server_config(load_properties):
    cherrypy.config.update(
        {
            'server.socket_port': load_properties.get('server_port', DEFAULT_PORT),
            'server.socket_host': load_properties.get('server_host', DEFAULT_HOST),
            'tools.encode.on': True,
            'tools.encode.encoding': 'utf-8'
        }
    )


def _setup_modules(loaded_properties, modules, kwargs):
    beans = {}
    for module in modules:
        module.before_setup(loaded_properties, kwargs, beans)

    return Context(beans)


def _after_setup(context, modules, kwargs, properties, beans_initializer):
    beans_initializer.initialize_all(context)
    for module in modules:
        module.after_setup(properties, kwargs, context, beans_initializer)


def _create_context(beans_initializer, kwargs, loaded_properties, modules):
    context = _setup_modules(loaded_properties, modules, kwargs)
    _after_setup(context, modules, kwargs, loaded_properties, beans_initializer)


def _finish_system_initialization(loaded_properties):
    _setup_server_config(loaded_properties)
    logs.setup_logging(log)


def scan_packages(packages_filter=lambda _: True):
    for modname in (modname for importer, modname, ispkg in pkgutil.walk_packages('.')
                    if '.' in modname and packages_filter(modname)):
        __import__(modname)


def init_context(properties_file,
                 modules=(),
                 **kwargs):
    beans_initializer = beans.BeansInitializer()
    modules = (web.Module(),) + modules

    properties = _configuration.create_configuration(properties_file)

    _finish_system_initialization(properties)
    _create_context(beans_initializer, kwargs, properties, modules)

    return cherrypy.tree


def start_standalone_application():
    cherrypy.engine.start()
    cherrypy.engine.block()
