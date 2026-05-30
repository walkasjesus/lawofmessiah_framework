from django.shortcuts import render
from django.views import View


class AuthorJusterView(View):
    def get(self, request):
        return render(request, 'authors/daniel_juster.html')
