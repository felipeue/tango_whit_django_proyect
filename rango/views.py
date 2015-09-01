from django.shortcuts import render
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm
# from django.http import HttpResponse

# request BDD simple


def index(request):
    list = {}
    category_list = Category.objects.order_by('likes')[:5]
    page_list = Page.objects.order_by('views')[:5]
    list['categories'] = category_list
    list['pages'] = page_list
    return render(request, 'index.html', list)

# simple template html


def about(request):
    context_dict = {'text': "Testing my first template"}
    return render(request, 'about.html', context_dict)

# multiple bdd query


def category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name
        context_dict['category_slug'] = category.slug
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category

    except Category.DoesNotExist:
        pass

    return render(request, 'category.html', context_dict)

# simple create to bdd


def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print form.errors
    else:
        form = CategoryForm()

    return render(request, 'add_category.html', {'form': form})

# Form to bdd whit data


def add_page(request, category_name_slug):

    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
                cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                # probably better to use a redirect here.
                return category(request, category_name_slug)
        else:
            print form.errors
    else:
        form = PageForm()

    context_dict = {'form':form, 'category': cat}

    return render(request, 'add_page.html', context_dict)






