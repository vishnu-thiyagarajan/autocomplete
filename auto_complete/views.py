from django.shortcuts import render
# import csv
# from django.core.cache import cache
from .models import AutoComplete
from .forms import AutoCompleteForm


def searchView(request):
    form = AutoCompleteForm(request.POST or None)
    context = {"form": form}
    context['list_text'] = AutoComplete.objects.filter(text_len__gt=2).order_by('text_len', 'count', 'text')
    return render(request, "autosearch.html", context)
