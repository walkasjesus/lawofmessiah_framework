from django.shortcuts import render
from django.views import View


class AuthorRudolphView(View):
    def get(self, request):
        return render(request, 'authors/michael_rudolph.html')
