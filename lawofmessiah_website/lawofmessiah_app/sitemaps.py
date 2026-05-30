from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from lawofmessiah_app.models import LawOfMessiah


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return [
            'commandments:index',
            'commandments:law_of_messiah_listing',
            'commandments:legalism',
        ]

    def location(self, item):
        return reverse(item)


class LawOfMessiahSitemap(Sitemap):
    priority = 0.9
    changefreq = 'monthly'

    def items(self):
        return LawOfMessiah.objects.all()

    def location(self, item):
        return reverse('commandments:law_of_messiah_detail', args=[item.pk])
