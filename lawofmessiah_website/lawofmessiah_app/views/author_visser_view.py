from django.shortcuts import render
from django.views import View


class AuthorVisserView(View):
    def get(self, request):
        return render(request, 'authors/jenske_visser.html')