from django.shortcuts import render
from django.views import View


SOURCE_URL = 'https://tikkunamerica.org/halachah/intro-mr3c.php'


class LegalismView(View):
    def get(self, request):
        return render(
            request,
            'pages/legalism.html',
            {
                'legalism_source_url': SOURCE_URL,
            },
        )

