# Web UI module
# encoding: utf-8
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.view import view_config

from icc.mvw.interfaces import IView
from isu.enterprise.interfaces import ICreditSlip
from zope.interface import implementer
from zope.component import adapter

from isu.enterprise.components import CreditSlip
from isu.enterprise.configurator import createConfigurator

createConfigurator("development.ini")


def _N(x):
    return x


@implementer(IView)
class DefaultView(object):

    def __init__(self, model=None):
        self.model = model


class HomeView(DefaultView):
    title = _N("ISU Enterprise Platform")


@view_config(route_name='home', renderer="isu.enterprise:templates/index.pt")
def hello_world(request):
    return {
        "view": HomeView(),
        "request": request,
        "response": request.response,
        "default": True,
    }


@adapter(ICreditSlip)
class CreditSlipView(DefaultView):
    title = _N("Credit Slip")
    body = "<strong>11111</strong>"
    style_css = """"""

    @property
    def date(self):
        return str(self.model.date).split(" ")[0]


@view_config(route_name="credit-slip", renderer="isu.enterprise:templates/credit-slip.pt")
def credit_slip_test(request):
    cs = CreditSlip(42, reason="Зарплата директору")
    #response = request.response
    # response.headerlist.append(("Content-Type","text/html"))
    view = CreditSlipView(cs)
    return {
        "view": view,
        "request": request,
        "response": request.response,
        "context": cs,
        "model": cs,
        "default": True
    }


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_zcml')
    #config.load_zcml('isu.enterprise:configure.zcml')
    config.include('pyramid_chameleon')
    # Static assets configuration
    config.add_static_view(
        name='bootstrap', path='isu.enterprise:admin-lte/bootstrap')
    config.add_static_view(name='documentation',
                           path='isu.enterprise:admin-lte/documentation')
    config.add_static_view(name='pages', path='isu.enterprise:admin-lte/pages')
    config.add_static_view(
        name='plugins', path='isu.enterprise:admin-lte/plugins')
    config.add_static_view(name='dist', path='isu.enterprise:admin-lte/dist')
    # End of static assets
    config.add_route('home', '/')
    config.add_route('credit-slip', '/CS')
    config.add_subscriber('isu.enterprise.subscribers.add_base_template',
                          'pyramid.events.BeforeRender')
    config.scan()
    app = config.make_wsgi_app()
    return app


if __name__ == '__main__':
    app = main(None)
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
