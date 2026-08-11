from django.shortcuts import render
from django.views import View


class WalkAsJesusView(View):
    def get(self, request):
        return render(request, 'pages/walk_as_jesus.html')