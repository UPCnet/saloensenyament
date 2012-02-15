from pyramid.config import Configurator
from repoze.zodbconn.finder import PersistentApplicationFinder
from salo2011.models import appmaker

from pyramid.session import UnencryptedCookieSessionFactoryConfig

from pyramid_who.whov2 import WhoV2AuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from pyramid_mailer.mailer import Mailer

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    my_session_factory = UnencryptedCookieSessionFactoryConfig('itsaseekreet')

    whoconfig_file = 'who.ini'
    identifier_id = 'auth_tkt'
    authn_policy = WhoV2AuthenticationPolicy(whoconfig_file, identifier_id)
    authz_policy = ACLAuthorizationPolicy()    
    
    zodb_uri = settings.get('zodb_uri')
    if zodb_uri is None:
        raise ValueError("No 'zodb_uri' in application configuration.")

    finder = PersistentApplicationFinder(zodb_uri, appmaker)
    def get_root(request):
        return finder(request.environ)
    config = Configurator(root_factory=get_root,
                          settings=settings,
                          session_factory = my_session_factory,
                          authentication_policy=authn_policy,
                          authorization_policy=authz_policy)
    
    config.registry['mailer'] = Mailer.from_settings(settings)
    
    config.add_static_view('static', 'salo2011:static')
    config.add_static_view('css', 'salo2011:css')
    config.add_static_view('js', 'salo2011:js')
    
    config.add_route('login', '/login',
                     view='salo2011.views.login.login',
                     view_renderer='salo2011:templates/login.pt')
    config.add_view('salo2011.views.login.login',
                     renderer='salo2011:templates/login.pt',
                     context='pyramid.exceptions.Forbidden')
    config.add_route('logout', '/logout',
                     view='salo2011.views.login.logout')
    config.scan('salo2011')
    return config.make_wsgi_app()
