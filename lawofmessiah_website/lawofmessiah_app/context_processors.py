from django.conf import settings
from django.utils import translation

from lawofmessiah_app.lib.access_policy import cjb_bible_id, is_bible_id_visible_for_request
from lawofmessiah_app.lib.media_cache_version import get_media_cache_version
from lawofmessiah_app.models import BibleTranslation, UserPreferences


def bible_translation(request):
    return {
        'bible_translation': BibleTranslation(),
        'cjb_bible_id': cjb_bible_id(),
        'cjb_bible_visible': is_bible_id_visible_for_request(request, cjb_bible_id()),
    }


def user_preferences(request):
    return {
        'user_preferences': UserPreferences(request.session),
    }


def cache_settings(request):
    return {
        'cache_timeout': 3600,
        'cache_on_language': UserPreferences(request.session).language,
        'cache_on_multi_language': UserPreferences(request.session).languages,
        'cache_on_bible': translation.get_language() + '_' + UserPreferences(request.session).bible.id,
        'cache_on_kids_mode': 'kids' if request.COOKIES.get('jc_kids_mode') else 'default',
        'cache_on_media_version': get_media_cache_version(),
        'commentary_cache_timeout_seconds': int(getattr(settings, 'COMMENTARY_CACHE_TIMEOUT_SECONDS', 60 * 60 * 24 * 30 * 6)),
    }
