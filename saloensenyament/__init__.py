from pyramid.config import Configurator
from repoze.zodbconn.finder import PersistentApplicationFinder
from saloensenyament.models import appmaker

from pyramid.session import UnencryptedCookieSessionFactoryConfig
from pyramid_who.whov2 import WhoV2AuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from models import Root
from pyramid_mailer.mailer import Mailer

def main(global_config, **settings):
    """ This function returns a WSGI application.
    """
    # security
    my_session_factory = UnencryptedCookieSessionFactoryConfig('itsaseekreet')
    whoconfig_file = settings['whoconfig_file']
    identifier_id = 'auth_tkt'
    authn_policy = WhoV2AuthenticationPolicy(whoconfig_file, identifier_id)
    authz_policy = ACLAuthorizationPolicy()    
    
    config = Configurator(root_factory=Root,
                          settings=settings,
                          session_factory = my_session_factory,
                          authentication_policy=authn_policy,
                          authorization_policy=authz_policy)
    
    config.registry['mailer'] = Mailer.from_settings(settings)
    
    config.add_static_view('static', 'saloensenyament:static')
    config.add_static_view('css', 'saloensenyament:css')
    config.add_static_view('images', 'saloensenyament:images')
    config.add_static_view('js', 'saloensenyament:js')
    
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

    config.add_view('saloensenyament.views.login.login', route_name='login',
                     renderer='saloensenyament:templates/login.pt')
    config.add_view('saloensenyament.views.login.logout', route_name='logout')
    
    config.add_view('saloensenyament.views.login.login',
                    context='pyramid.httpexceptions.HTTPForbidden',
                    renderer='saloensenyament:templates/login.pt')

    config.scan('saloensenyament')


    return config.make_wsgi_app()
