from django.shortcuts import render
from my_project_app.models import *


def index_page(request):
    return render(request, 'index.html')


def general_stats_page(request):
    salary_year = AllStatsSalaryYear.objects.all()
    remade_salary_year = [{'date': int(float(row.date)), 'salary': int(row.salary)} for row in salary_year]

    vacancies_year = AllStatsVacanciesYear.objects.all()
    remade_vacancies_year = [{'date': int(float(row.date)), 'vacancies_count': row.vacancies_count} for row in vacancies_year]

    salary_city = AllStatsSalaryCity.objects.all()
    remade_salary_city = [{'city': row.city, 'salary': int(row.salary)} for row in salary_city]

    vacancies_city = AllStatsVacanciesCity.objects.all()
    remade_vacancies_city = [{'city': row.city, 'vacancies_count': row.vacancies_count} for row in vacancies_city]

    top_skills = AllStatsTopSkills.objects.all()
    remade_top_skills = [{'current_skill': row.current_skill, 'skill_count': row.skill_count,
                          'date': int(float(row.date))} for row in top_skills]

    photo_salary_year = GraphPicture.objects.get(graph_name = 'Динамика уровня зарплат по годам')
    photo_vacancies_year = GraphPicture.objects.get(graph_name = 'Динамика количества вакансий по годам')
    photo_salary_city = GraphPicture.objects.get(graph_name = 'Уровень зарплат по городам')
    photo_vacancies_city = GraphPicture.objects.get(graph_name = 'Доля вакансий по городам')
    photo_top_skills = GraphPicture.objects.get(graph_name = 'ТОП-20 навыков по годам')

    return render(request, 'general_stats.html', {
        'salary_year': remade_salary_year,
        'vacancies_year': remade_vacancies_year,
        'salary_city': remade_salary_city,
        'vacancies_city': remade_vacancies_city,
        'top_skills': remade_top_skills,
        'photo_salary_year': photo_salary_year,
        'photo_vacancies_year': photo_vacancies_year,
        'photo_salary_city': photo_salary_city,
        'photo_vacancies_city': photo_vacancies_city,
        'photo_top_skills': photo_top_skills
    })


def relevance_page(request):
    salary_year = RelevanceSalaryYear.objects.all()
    remade_salary_year = [{'date': int(float(row.date)), 'salary': int(row.salary)} for row in salary_year]

    vacancies_year = RelevanceVacanciesYear.objects.all()
    remade_vacancies_year = [{'date': int(float(row.date)), 'vacancies_count': row.vacancies_count} for row in vacancies_year]

    photo_salary_year_analytics = GraphPicture.objects.get(graph_name='Динамика уровня зарплат по годам для профессии аналитика')
    photo_vacancies_year_analytics = GraphPicture.objects.get(graph_name='Динамика количества вакансий по годам для профессии аналитика')
    return render(request, 'relevance.html', {
        'salary_year': remade_salary_year,
        'vacancies_year': remade_vacancies_year,
        'photo_salary_year': photo_salary_year_analytics,
        'photo_vacancies_year': photo_vacancies_year_analytics
    })


def geography_page(request):
    salary_city = GeographySalaryCity.objects.all()
    remade_salary_city = [{'city': row.city, 'salary': int(row.salary)} for row in salary_city]

    vacancies_city = GeographyVacanciesCity.objects.all()
    remade_vacancies_city = [{'city': row.city, 'vacancies_count': row.vacancies_count} for row in vacancies_city]

    photo_salary_city_analytics = GraphPicture.objects.get(graph_name='Уровень зарплат по городам для профессии аналитика')
    photo_vacancies_city_analytics = GraphPicture.objects.get(graph_name='Доля вакансий по городам для профессии аналитика')
    return render(request, 'geography.html',{
        'salary_city': remade_salary_city,
        'vacancies_city': remade_vacancies_city,
        'photo_salary_city': photo_salary_city_analytics,
        'photo_vacancies_city': photo_vacancies_city_analytics
    })


def top_skills_page(request):
    top_skills = SkillsTopSkills.objects.all()
    remade_top_skills = [{'current_skill': row.current_skill, 'skill_count': row.skill_count,
                          'date': int(float(row.date))} for row in top_skills]

    photo_top_skills_analytics = GraphPicture.objects.get(graph_name='ТОП-20 навыков по годам для профессии аналитика')
    return render(request, 'top_skills.html', {
        'top_skills': remade_top_skills,
        'photo_skills': photo_top_skills_analytics
    })


def last_vacancies_page(request):
    return render(request, 'last_vacancies.html')