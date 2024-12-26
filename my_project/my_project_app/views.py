from django.shortcuts import render

def index_page(request):
    return render(request, 'index.html')


def general_stats_page(request):
    return render(request, 'general_stats.html')


def relevance_page(request):
    return render(request, 'relevance.html')


def geography_page(request):
    return render(request, 'geography.html')


def top_skills_page(request):
    return render(request, 'top_skills.html')


def last_vacancies_page(request):
    return render(request, 'last_vacancies.html')