"""
Custom middleware to force Russian as default language
"""
from django.utils import translation


class ForceRussianLanguageMiddleware:
    """
    Middleware that forces Russian language for users accessing the site
    without a language prefix. This ensures / redirects to /ru/ not /en/
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # If no language is set in session, force Russian
        if not request.session.get('django_language'):
            translation.activate('ru')
            request.LANGUAGE_CODE = 'ru'
        
        response = self.get_response(request)
        return response
