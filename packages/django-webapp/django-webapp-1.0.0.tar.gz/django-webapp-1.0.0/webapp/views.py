import os
try:
	from urllib.parse import unquote
except ImportError:
	from urllib import unquote

from django.conf import settings
from django.contrib.staticfiles import finders
from django.http import Http404
from django.views.static import serve

def webapp_serve(request, path, document_root=None):
	"""View for debugging (runwebapp), adds index.html to whatever path if needed. Will try to resolve static files when STATIC_URL prefix is missing."""
	index = settings.WEBAPP_INDEX if hasattr(settings, 'WEBAPP_INDEX') else 'index.html'
	if path.endswith('/'):
		return serve(request, path + index, document_root)
	else:
		# Determine if path is directory
		path = os.path.normpath(unquote(path))
		path = path.lstrip('/')
		fullpath = os.path.join(document_root, path)
		if os.path.isdir(fullpath):
			return serve(request, path + '/' + index, document_root)
		else:
			try:
				return serve(request, path, document_root)
			except Http404 as e:
				result = finders.find(path)
				if not result:
					raise e
				else:
					result = result[0] if isinstance(result, (list, tuple)) else result
					return serve(request, path, result[:-len(path)])
