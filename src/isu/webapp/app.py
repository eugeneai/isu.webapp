# Web UI module
# encoding: utf-8
from pyramid.config import Configurator
from isu.enterprise.configurator import createConfigurator
from zope.interface import directlyProvides
from isu.webapp.interfaces import IConfigurationEvent, IApplication
from isu.webapp.views import View
from zope.i18nmessageid import MessageFactory
from zope.component import getSiteManager, getGlobalSiteManager

_ = _N = MessageFactory("isu.webapp")


class HomeView(View):
    title = _N("ISU Enterprise WebApplication Platform")


def hello_world(request):
    return {
        "view": HomeView(),
        "request": request,
        "response": request.response,
        "default": True,
    }


def configurator(global_config, **settings):

    gsm = getGlobalSiteManager()
    config = Configurator(registry=gsm, settings=settings)
    config.setup_registry(settings=settings)

    createConfigurator(global_config["__file__"],
                       registry=config.registry,
                       name="configuration")
    return config

def includeme(global_config, **settings): # Default webapp setup. DEMO

    global_config.include('pyramid_zcml')
    global_config.load_zcml('isu.webapp:configure.zcml')
    global_config.include('pyramid_chameleon')

    return global_config


def create_application(config):

    directlyProvides(config, IConfigurationEvent)
    config.registry.notify(config)

    app = config.make_wsgi_app()
    config.registry.registerUtility(app, IApplication, name="application")
    config.registry.notify(app)

    return app


def main(global_config, **settings):
    # config.hook_zca()

    config = configurator(global_config, **settings)
    return create_application(config)


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    app = main(None)
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
