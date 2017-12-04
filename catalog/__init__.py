import os
import logging

from pyramid.config import Configurator
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid import renderers

from .security import groupfinder


def main(global_config, **settings):
	my_session_factory = UnencryptedCookieSessionFactoryConfig('itsaseekreet')
	authn_policy = AuthTktAuthenticationPolicy(settings['secret'], callback=groupfinder,
        hashalg='sha512')
	authz_policy = ACLAuthorizationPolicy()                                    
	config = Configurator(settings=settings,session_factory=my_session_factory)
	config.include('pyramid_flash_message')
	config.include('pyramid_jinja2')
	config.include('pyramid_storage')
	json_renderer = renderers.JSON()
	config.add_renderer('json', json_renderer)
	config.add_jinja2_renderer('.html')
	config.add_static_view('static', 'static', cache_max_age=3600)
	config.add_static_view('templates/assets','templates/assets',cache_max_age=3600)
	config.add_static_view('templates/rejs','templates/rejs',cache_max_age=3600)
	config.set_authentication_policy(authn_policy)
	config.set_authorization_policy(authz_policy)
	config.add_route('login','/login')
	config.add_route('logout','/logout')
	config.add_route('home1','/home1')
	config.add_route('home','/home')
	config.add_route('hello','/hello')
	config.add_route('itemfetch','/itemfetch')
	config.add_route('vendor','/vendor')
	config.add_route('itemtype','/itemtype')
	config.add_route('category', '/category')
	config.add_route('material', '/material')
	config.add_route('fabric', '/fabric')
	config.add_route('catalog', '/catalog')
	config.add_route('quotation','/quotation')
	config.add_route('addquote','/addquote')
	config.add_route('itemdetails','/itemdetails')
	config.add_route('editdetails','/editdetails')
	config.add_route('vendoredit','/vendoredit')
	config.add_route('search','/searchres')
	config.add_route('filter','/filter')
	config.add_route('createlist','/createlist')
	config.add_route('itemadded','/itemadded')
	config.add_route('presentation','/presentation/{p_id}')
	config.add_route('addpre','/addpre')
	config.add_route('addslide','/addslide')
	config.add_route('saveslide','/saveslide')
	config.add_route('viewlist','/viewlist')
	config.add_route('subviewlist','/subviewlist')
	config.add_route('download','/download')
	config.add_route('submit','/submitvendor')
	config.add_route('submitcat','/submitcat')
	config.add_route('submitcatalog','/submitcatalog')
	config.add_route('submitmat','/submitmaterial')
	config.add_route('submitfab','/submitfab')
	config.add_route('submitquot','/submitquotation')
	config.add_route('submitaddquote','/submitaddquote')
	config.add_route('submititem','/submititem')
	config.add_route('submitedititem','/submitedititem')
	config.add_route('submiteditquote','/submiteditquote')
	config.add_route('submitaddlist','/submitaddlist')
	config.add_route('uploadimage','/uploadimage')
	config.add_route('slide','/slide/{p_id}/{s_id}')
	config.scan()
	return config.make_wsgi_app()