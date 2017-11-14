from pyramid.config import Configurator
from pyramid.session import UnencryptedCookieSessionFactoryConfig

def main(global_config, **settings):
	my_session_factory = UnencryptedCookieSessionFactoryConfig('itsaseekreet')
	config = Configurator(settings=settings,session_factory=my_session_factory)
	config.include('pyramid_flash_message')
	config.include('pyramid_jinja2')
	config.include('pyramid_storage')
	config.add_jinja2_renderer('.html')
	config.add_static_view('static', 'static', cache_max_age=3600)
	config.add_static_view('templates/assets','templates/assets',cache_max_age=3600)
	config.add_static_view('templates/rejs','templates/rejs',cache_max_age=3600)
	config.add_route('login','/login')
	config.add_route('submitlogin','/submitlogin')
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
	config.add_route('presentation','/presentation')
	config.add_route('addpre','/addpre')
	config.add_route('addslide','/addslide')
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
	config.scan()
	return config.make_wsgi_app()
