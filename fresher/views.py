from django.shortcuts import get_object_or_404, render

from .models import Category, Recipe


def recipe_all(request):
    recipes = Recipe.recipes.all()
    return render(request, 'fresher/index.html', {'recipes': recipes})


def category_list(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    recipes = Recipe.recipes.filter(category=category)
    return render(request, 'fresher/category.html', {'category': category, 'recipes': recipes})


def recipe_detail(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug, in_stock=True)
    return render(request, 'fresher/single.html', {'recipe': recipe})
