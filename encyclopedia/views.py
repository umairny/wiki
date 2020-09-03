from django.shortcuts import render
from django import forms
from . import util
from random import randint
import re


from markdown2 import Markdown

markdowner = Markdown()
entries = util.list_entries()

class Post(forms.Form):
    title = forms.CharField(label= "Title")
    textarea = forms.CharField(widget=forms.Textarea(), label='')

class Edit(forms.Form):
    textarea = forms.CharField(widget=forms.Textarea(), label='')


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# Search logic
def search(request):
    query = request.GET.get('q').lower()
    entry = [item.lower() for item in entries]
    searchlist = []

    if query:
        if query in entry:
            page = util.get_entry(query)
            page_converted = markdowner.convert(page)
            context = {
                'page': page_converted,
                'title': query,
                }
            return render(request, "encyclopedia/entry.html", context)
            if query in entry:
                searchlist.append(entry)
                context = {
                    'searchlist': searchlist
                }
                return render(request, "encyclopedia/search.html", context)
        else:
            return render(request, "encyclopedia/error.html", {"message": "The search result not found Try again"})
    else:
        return render(request, "encyclopedia/error.html", {"message": "Type some thing in search"})

# Entry page 
def entry(request, title):
    if title in entries:
        page = util.get_entry(title)
        page_converted = markdowner.convert(page)
        context = {
            'page': page_converted,
            'title': title,
        }
        return render(request, "encyclopedia/entry.html", context)
    else:
        return render(request, "encyclopedia/error.html", {"message": "The requested page was not found."})

#Creat New page entry
def add_page(request):
    if request.method == 'POST':
        form = Post(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            textarea = form.cleaned_data["textarea"]
            if title in entries:
                return render(request, "encyclopedia/error.html", {"message": "Page already exist"})
            else:
                util.save_entry(title, textarea)
                page = util.get_entry(title)
                page_converted = markdowner.convert(page)

                context = {
                    'page': page_converted,
                    'title': title
                }

                return render(request, "encyclopedia/entry.html", context)
    else:
        return render(request, "encyclopedia/add_page.html", {"post": Post()})

def edit(request, title):
    if request.method == 'GET':
        page = util.get_entry(title)
        
        context = {
            
            'edit': Edit(initial={'textarea': page}),
            'title': title
        }

        return render(request, "encyclopedia/edit.html", context)
    else:
        form = Edit(request.POST) 
        if form.is_valid():
            textarea = form.cleaned_data["textarea"]
            util.save_entry(title,textarea)
            page = util.get_entry(title)
            page_converted = markdowner.convert(page)

            context = {
                'page': page_converted,
                'title': title
            }

            return render(request, "encyclopedia/entry.html", context)

def random(request):

    num = randint(0, len(entries) - 1)
    page_random = entries[num]
    
    page = util.get_entry(page_random)
    page_converted = markdowner.convert(page)
    context = {
        'page': page_converted,
        'title': page_random,
        }
    return render(request, "encyclopedia/entry.html", context)
