from unittest import TestCase
from unittest.mock import Mock, patch

from bible_lib.bible_api.api_bible import ApiBible
from bible_lib.bible_api.bible_api_client import BibleApiClient
from bible_lib.bible_books import BibleBooks
from bible_lib.tests.dummy_responses import DummyResponses


class TestBible(TestCase):
    @staticmethod
    def _make_bible():
        return ApiBible(api_key='test-api-key', bible_id='ead7b4cc5007389c-01')

    def test_get_verse(self):
        bible = self._make_bible()
        bible.client.get = Mock(return_value=DummyResponses().verses())
        verse = bible.verse(BibleBooks.John, 1, 51)

        bible.client.get.assert_called_with(
            'https://api.scripture.api.bible/v1/bibles/ead7b4cc5007389c-01/passages/JHN.1.51-JHN.1.51?content-type=text')
        self.assertIn('En Hij sprak tot hem: Voorwaar, voorwaar, Ik zeg u:', verse)

    def test_get_single_verse_from_minimal_api_bible_response(self):
        bible = self._make_bible()
        bible.client.get = Mock(return_value='{"data":{"content":"[1] For God so loved the world, that he gave his only Son.","copyright":"Test copyright"}}')

        verse = bible.verse(BibleBooks.John, 3, 16)

        bible.client.get.assert_called_with(
            'https://api.scripture.api.bible/v1/bibles/ead7b4cc5007389c-01/passages/JHN.3.16-JHN.3.16?content-type=text')
        self.assertIn('For God so loved the world', verse)
        self.assertEqual(bible.copyright, 'Test copyright')

    def test_get_verses_spanning_multiple_chapters(self):
        bible = self._make_bible()
        bible.client.get = Mock(return_value=DummyResponses().verses())
        verses = bible.verses(BibleBooks.John, 1, 51, 2, 1)

        bible.client.get.assert_called_with(
            'https://api.scripture.api.bible/v1/bibles/ead7b4cc5007389c-01/passages/JHN.1.51-JHN.2.1?content-type=text')
        # Part of verse 51
        self.assertIn('En Hij sprak tot hem: Voorwaar, voorwaar, Ik zeg u:', verses)
        # Part of verse 1
        self.assertIn('En de derde dag werd er een bruiloft gevierd te Kana van Galilea', verses)


class TestBibleApiClient(TestCase):
    @patch('bible_lib.bible_api.bible_api_client.requests.get')
    def test_get_sets_timeout_and_returns_text(self, mock_get):
        mock_response = Mock()
        mock_response.ok = True
        mock_response.text = '{"data":{"content":"[1] Let every soul be subject unto the higher powers."}}'
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        client = BibleApiClient(api_key='test-api-key')
        text = client.get('https://api.scripture.api.bible/v1/bibles/87f620660790371b-01/passages/ROM.13.1-ROM.13.1?content-type=text')

        self.assertEqual(text, mock_response.text)
        mock_get.assert_called_once_with(
            'https://api.scripture.api.bible/v1/bibles/87f620660790371b-01/passages/ROM.13.1-ROM.13.1?content-type=text',
            headers={'api-key': 'test-api-key'},
            timeout=20,
        )
