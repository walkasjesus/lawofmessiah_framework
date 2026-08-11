from django.conf import settings
from django.urls import path
from django.utils import translation
from django.utils.translation import gettext_lazy as _

# Import all your views and other necessary modules
from lawofmessiah_app.views.admin.admin_enable_bible import AdminEnableBible
from lawofmessiah_app.views.admin.admin_persist_bible_cache import AdminPersistBibleCache
from lawofmessiah_app.views.admin.admin_reset_bibles import AdminResetBibles
from lawofmessiah_app.views.legalism_view import LegalismView
from lawofmessiah_app.views.termsandconditions_view import TermsView
from lawofmessiah_app.views.privacy_view import PrivacyView
from lawofmessiah_app.views.index_view import IndexView
from lawofmessiah_app.views.author_rudolph_view import AuthorRudolphView
from lawofmessiah_app.views.author_juster_view import AuthorJusterView
from lawofmessiah_app.views.author_visser_view import AuthorVisserView
from lawofmessiah_app.views.walk_as_jesus_view import WalkAsJesusView
from lawofmessiah_app.views.law_of_messiah_view import (
    LawOfMessiahListingView,
    LawOfMessiahDetailView,
    LawOfMessiahBibleVersesView,
)
from lawofmessiah_app.views.user_preferences import UserPreferencesLanguagesView, UserPreferencesBibleView, BibleTranslationsForLanguageView
from lawofmessiah_app.views.user_preferences import (
    CommentaryTranslationView,
    ScripturaCommentaryProxyView,
    UserPreferencesLanguageSwitchView,
)
from lawofmessiah_app.views.maimonides_view import MaimonidesBibleVersesView, MaimonidesList

app_name = 'commandments'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('language-switch/', UserPreferencesLanguageSwitchView.as_view(), name='language_switch'),
    path(_('bible/'), UserPreferencesBibleView.as_view(), name='bible'),
    path(_('languages/'), UserPreferencesLanguagesView.as_view(), name='languages'),
    path(_('bible-translations/'), BibleTranslationsForLanguageView.as_view(), name='bible_translations_for_language'),
    path(_('commentary-translate/'), CommentaryTranslationView.as_view(), name='commentary_translate'),
    path(_('commentary-scriptura/'), ScripturaCommentaryProxyView.as_view(), name='commentary_scriptura'),
    path(_('walk-as-jesus/'), WalkAsJesusView.as_view(), name='walk_as_jesus'),
    path(_('authors/michael-rudolph/'), AuthorRudolphView.as_view(), name='author_rudolph'),
    path(_('authors/daniel-juster/'), AuthorJusterView.as_view(), name='author_juster'),
    path(_('authors/jenske-visser/'), AuthorVisserView.as_view(), name='author_visser'),
    path(_('maimonides/'), MaimonidesList.as_view(), name='maimonides_listing'),
    path(_('maimonides/<str:maimonides_id>/verses/'), MaimonidesBibleVersesView.as_view(), name='maimonides_verses'),
    path(_('law_of_messiah/'), LawOfMessiahListingView.as_view(), name='law_of_messiah_listing'),
    path(_('law_of_messiah/<str:law_id>/'), LawOfMessiahDetailView.as_view(), name='law_of_messiah_detail'),
    path(_('law_of_messiah/<str:law_id>/verses/'), LawOfMessiahBibleVersesView.as_view(), name='law_of_messiah_verses'),
    path(_('legalism/'), LegalismView.as_view(), name='legalism'),
    path(_('termsandconditions/'), TermsView.as_view(), name='termsandconditions'),
    path(_('privacy/'), PrivacyView.as_view(), name='privacy'),
    path(_('admin/reset_bibles/'), AdminResetBibles.as_view(), name='admin_reset_bibles'),
    path(_('admin/persist_bible_cache/'), AdminPersistBibleCache.as_view(), name='admin_persist_bible_cache'),
    path(_('admin/enable_bible/'), AdminEnableBible.as_view(), name='admin_enable_bible'),
]


def _build_localized_aliases():
    """Build URL aliases for all non-default languages using .po file translations."""
    default_lang = settings.LANGUAGE_CODE.split('-')[0].lower()
    aliases = []

    with translation.override(default_lang):
        default_routes = {
            id(p): str(p.pattern._route)
            for p in urlpatterns
            if hasattr(p, 'pattern') and hasattr(p.pattern, '_route')
        }

    for lang_code, _ in settings.LANGUAGES:
        lang_code = str(lang_code).split('-')[0].lower()
        if lang_code == default_lang:
            continue
        with translation.override(lang_code):
            for p in urlpatterns:
                pid = id(p)
                if pid not in default_routes:
                    continue
                localized = str(p.pattern._route)
                if localized != default_routes[pid]:
                    aliases.append(path(localized, p.callback, name=p.pattern.name))

    return aliases


# Prepend localized aliases so named English patterns overwrite them in reverse().
urlpatterns = _build_localized_aliases() + urlpatterns