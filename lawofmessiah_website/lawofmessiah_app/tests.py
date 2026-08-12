import json
import os
from unittest.mock import Mock, patch

from django.contrib.sessions.middleware import SessionMiddleware
from django.test import override_settings
from django.test import RequestFactory, SimpleTestCase, TestCase

from lawofmessiah_app.models.bibles import BibleTranslationMetaData, BibleTranslation
from lawofmessiah_app.context_processors import cache_settings
from lawofmessiah_app.views.legalism_view import LegalismView
from lawofmessiah_app.views.user_preferences import ScripturaCommentaryProxyView


class BibleTranslationTestCase(TestCase):
    # Checking the exact number is not working because it can change over time.
    # This just gives an indication.
    approximate_bible_count = 100

    def _require_bibles(self):
        if len(BibleTranslation().all()) == 0:
            self.skipTest('No Bible translations available in local test environment.')

    def test_all(self):
        self._require_bibles()
        all_bibles = BibleTranslation().all()
        self.assertGreaterEqual(len(all_bibles), self.approximate_bible_count)

    def test_all_in_supported_languages(self):
        self._require_bibles()
        all_bibles = len(BibleTranslation().all())
        all_in_supported_languages = len(BibleTranslation().all_in_supported_languages())
        self.assertGreater(all_in_supported_languages, 10)
        self.assertLess(all_in_supported_languages, all_bibles)

    def test_all_enabled_with_no_explicit_disabled_ones(self):
        self._require_bibles()
        all_bibles = len(BibleTranslation().all())
        all_enabled = len(BibleTranslation().all_enabled())
        self.assertEqual(all_enabled, all_bibles)

    def test_all_enabled_with_disabled_one(self):
        self._require_bibles()
        all_bibles = len(BibleTranslation().all())
        self.assertGreaterEqual(all_bibles, self.approximate_bible_count)
        self._disable('de4e12af7f28f599-01')
        all_enabled = len(BibleTranslation().all_enabled())
        self.assertEqual(all_enabled, all_bibles-1)

    @override_settings(DISABLED_BIBLE_TRANSLATIONS=['de4e12af7f28f599-01'])
    def test_all_enabled_respects_settings_disabled_ids(self):
        self._require_bibles()
        enabled_ids = {b.id for b in BibleTranslation().all_enabled()}
        self.assertNotIn('de4e12af7f28f599-01', enabled_ids)

    def test_all_disabled(self):
        self._require_bibles()
        before_count = len(BibleTranslation().all_disabled())
        self._disable('de4e12af7f28f599-01')
        after_count = len(BibleTranslation().all_disabled())
        self.assertEqual(before_count+1, after_count)

    def _disable(self, bible_id: str):
        meta_data = BibleTranslationMetaData()
        meta_data.is_enabled = False
        meta_data.bible_id = bible_id
        meta_data.save()


class KidsModeCacheSettingsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_cache_settings_include_default_mode_key(self):
        request = self.factory.get('/')
        request.session = self.client.session

        self.assertEqual(cache_settings(request)['cache_on_kids_mode'], 'default')

    def test_cache_settings_include_kids_mode_key(self):
        request = self.factory.get('/', HTTP_COOKIE='jc_kids_mode=true')
        request.session = self.client.session
        request.COOKIES['jc_kids_mode'] = 'true'

        self.assertEqual(cache_settings(request)['cache_on_kids_mode'], 'kids')


class CommentaryProxyViewTestCase(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_missing_required_params_returns_400(self):
        request = self.factory.get('/commentary-scriptura/', {'book': 'John'})
        response = ScripturaCommentaryProxyView.as_view()(request)

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', json.loads(response.content.decode('utf-8')))

    @patch('lawofmessiah_app.views.user_preferences.requests.get')
    def test_proxy_calls_configured_bijbelapi_endpoint(self, mock_get):
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {'16': 'For God so loved the world'}
        mock_get.return_value = mock_response

        request = self.factory.get(
            '/commentary-scriptura/',
            {
                'source': 'matthew-henry',
                'book': 'John',
                'chapter': '3',
                'verse': '16',
            },
        )

        with self.settings(
            COMMENTARY_API_URL='https://www.bijbelapi.com/api/commentary',
            BIJBEL_API_KEY='test-key',
        ):
            response = ScripturaCommentaryProxyView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content.decode('utf-8')), {'16': 'For God so loved the world'})
        mock_get.assert_called_once_with(
            'https://www.bijbelapi.com/api/commentary',
            params={
                'source': 'matthew-henry',
                'book': 'John',
                'chapter': '3',
                'verse': '16',
            },
            headers={'x-api-key': 'test-key'},
            timeout=20,
        )

    @patch('lawofmessiah_app.views.user_preferences.requests.get')
    def test_proxy_omits_api_key_header_when_not_configured(self, mock_get):
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {'0': 'intro'}
        mock_get.return_value = mock_response

        request = self.factory.get(
            '/commentary-scriptura/',
            {'source': 'matthew-henry', 'book': 'John', 'chapter': '3'},
        )

        with self.settings(BIJBEL_API_KEY=''):
            response = ScripturaCommentaryProxyView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        mock_get.assert_called_once()
        self.assertEqual(mock_get.call_args.kwargs['headers'], {})

    @patch('lawofmessiah_app.views.user_preferences.requests.get')
    def test_upstream_error_returns_502(self, mock_get):
        mock_get.side_effect = Exception('upstream failed')

        request = self.factory.get(
            '/commentary-scriptura/',
            {'source': 'matthew-henry', 'book': 'John', 'chapter': '3'},
        )

        response = ScripturaCommentaryProxyView.as_view()(request)

        self.assertEqual(response.status_code, 502)
        self.assertIn('error', json.loads(response.content.decode('utf-8')))


class GeoLocationRedirectMiddlewareTestCase(TestCase):
    @override_settings(
        ALLOWED_HOSTS=['testserver', 'acc.lawofmessiah.org', 'acc.wetvanchristus.nl'],
        GEO_REDIRECT_ENABLED=True,
        GEO_REDIRECT_NL_DOMAIN='acc.wetvanchristus.nl',
        GEO_REDIRECT_EN_DOMAIN='acc.lawofmessiah.org',
    )
    def test_accept_language_without_cookie_or_geo_does_not_redirect_domains(self):
        previous_env = os.environ.get('GEO_REDIRECT_ENABLED')
        os.environ['GEO_REDIRECT_ENABLED'] = 'true'
        try:
            response = self.client.get(
                '/',
                HTTP_HOST='acc.lawofmessiah.org',
                HTTP_ACCEPT_LANGUAGE='nl',
            )
        finally:
            if previous_env is None:
                os.environ.pop('GEO_REDIRECT_ENABLED', None)
            else:
                os.environ['GEO_REDIRECT_ENABLED'] = previous_env

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.headers.get('Location'))


class LegalismViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def _attach_session(self, request):
        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(request)
        request.session.save()
        return request

    def test_legalism_page_renders_static_sections(self):
        request = self._attach_session(self.factory.get('/legalism/'))
        response = LegalismView.as_view()(request)
        content = response.content.decode('utf-8')

        self.assertEqual(response.status_code, 200)
        self.assertIn('id="A-0"', content)
        self.assertIn('id="L-5"', content)
        self.assertIn('href="#L-5"', content)
        self.assertNotIn('[Comment]', content)
        self.assertNotIn('Times New Roman', content)
        self.assertNotIn('{{ legalism_html }}', content)
