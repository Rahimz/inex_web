from django.shortcuts import render
from django.utils.translation import gettext_lazy as _


def HomeView(request):
    context = dict(
        page_title=_("Home")
    )
    return render(
        request,
        'home.html',
        context
    )
