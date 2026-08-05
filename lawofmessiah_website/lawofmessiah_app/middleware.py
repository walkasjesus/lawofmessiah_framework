from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import NoReverseMatch, Resolver404, resolve, reverse
from django.utils import translation
from django.utils.translation import get_language


class LocalizedUrlRedirectMiddleware:
    """Redirect default-language URL slugs to localized equivalents."""

    def __init__(self, get_response):
        self.get_response = get_response
        self._default_lang_prefix = settings.LANGUAGE_CODE[:2].lower()

    def __call__(self, request):
        language = get_language()
        if language and language[:2].lower() != self._default_lang_prefix:
            match = None
            with translation.override(settings.LANGUAGE_CODE):
                try:
                    match = resolve(request.path)
                except Resolver404:
                    pass

            if match is not None and match.view_name:
                with translation.override(language):
                    try:
                        localized = reverse(
                            match.view_name, args=match.args, kwargs=match.kwargs
                        )
                    except NoReverseMatch:
                        localized = request.path

                if localized != request.path:
                    query = request.META.get('QUERY_STRING', '')
                    return HttpResponseRedirect(localized + ('?' + query if query else ''))

        return self.get_response(request)


class PermissionsPolicyMiddleware:
    """Set a permissive policy for features needed by embedded media players."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['Permissions-Policy'] = (
            'picture-in-picture=(self "https://www.youtube.com" "https://www.youtube-nocookie.com")'
        )
        return response
