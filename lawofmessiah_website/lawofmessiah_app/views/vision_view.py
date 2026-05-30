from django.shortcuts import render
from django.views import View

from lawofmessiah_app.models import UserPreferences
from bible_lib.bible_books import BibleBooks


class VisionView(View):
    def get(self, request):

        selected_bible = UserPreferences(request.session).bible

        context = {
            'bible': selected_bible,
            'verse_1john_2_6': selected_bible.verses(BibleBooks.JohnFirstBook, 2, 6, 2, 6),
            'verse_1john_2_3_6': selected_bible.verses(BibleBooks.JohnFirstBook, 2, 3, 2, 6),
            'verse_john_15_10': selected_bible.verses(BibleBooks.John, 15, 10, 15, 10),
            'verse_hebrews_13_20_21': selected_bible.verses(BibleBooks.Hebrews, 13, 20, 13, 21),
        }
        return render(request, 'pages/vision.html', context)
