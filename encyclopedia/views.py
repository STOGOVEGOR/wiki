import re
import markdown
import random

from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponse
from random import choice

from . import util

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'size':76}))
    content = forms.CharField(label="Content", widget=forms.Textarea())

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    if content == None:
        return render(request, "encyclopedia/404.html")
    return render(request, "encyclopedia/entry.html", {
        "content": markdown.markdown(content),
        "title": title
    })

def search(request):
    entries = util.list_entries()
    query = request.GET.get("q", "")
    if query in entries:
        return redirect(entry, query)
    results = [entry for entry in entries if query.lower() in entry.lower()]
    return render(request, "encyclopedia/index.html", {
            "entries": results,
    })

def newentry(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            entries = util.list_entries()
            for entry in entries:
                if title.lower() == entry.lower():
                    return render(request, "encyclopedia/error.html", {
                    "title": title
                    })
            util.save_entry(title, content)
            return render(request, "encyclopedia/entry.html", {
            "content": markdown.markdown(util.get_entry(title)),
            "title": title
            })
        else:
            return render(request, "encyclopedia/newentry.html", {
            "form": form
            })
    return render(request, "encyclopedia/newentry.html", {
        "form": NewEntryForm()
    })

def editentry(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return render(request, "encyclopedia/entry.html", {
            "content": markdown.markdown(util.get_entry(title)),
            "title": title
            })
    title = request.GET.get("q", "")
    return render(request, "encyclopedia/editentry.html", {
        "content_edit": util.get_entry(title),
        "title_edit": title
    })

def random_page(request):
    entries = util.list_entries()
    title = random.choice(entries)
    return render(request, "encyclopedia/entry.html", {
        "content": markdown.markdown(util.get_entry(title)),
        "title": title
        })
