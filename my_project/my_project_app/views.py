from django.shortcuts import render
import requests
from datetime import datetime, timedelta
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
    professions = ['analytic', 'аналитик', 'analyst', 'аналітик']
    url = 'https://api.hh.ru/vacancies'
    vacancies = []
    total_vacancies_loaded = 0  # Счетчик загруженных вакансий

    for profession in professions:
        params = {
            'text': profession,
            'per_page': 10,  # Запрашиваем 10 вакансий для каждой профессии
            'order_by': 'publication_time',
            'date_from': (datetime.now() - timedelta(days=1)).isoformat(),
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            for item in data['items']:
                if total_vacancies_loaded >= 10:  # Проверка, если уже загружено 10 вакансий
                    break  # Выходим из цикла, если достигли лимита

                vacancy_details = fetch_vacancy_details(item['id'])
                if vacancy_details:
                    skills = vacancy_details.get('key_skills', [])
                    skills_string = ', '.join([skill['name'] for skill in skills]) if skills else ''
                    published_at_str = item.get('published_at')
                    if published_at_str:
                        published_at = datetime.fromisoformat(
                            published_at_str.replace('Z', '+00:00'))  # Исправленная строка
                    else:
                        published_at = None

                    vacancies.append({
                        'name': item['name'],
                        'description': vacancy_details.get('description', 'Описание отсутствует'),
                        'skills': skills_string,
                        'company': item['employer']['name'] if item.get('employer') else "Не указано",
                        'salary': get_salary_string(item.get('salary', {})),
                        'area': item['area']['name'],
                        'published_at': published_at,  # Исправленная строка
                    })
                    total_vacancies_loaded += 1  # Увеличиваем счетчик

    return render(request, 'last_vacancies.html', {'vacancies': vacancies})


def fetch_vacancy_details(vacancy_id):
    url = f'https://api.hh.ru/vacancies/{vacancy_id}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None


def get_salary_string(salary_data):
    if not salary_data:
        return 'Не указан'

    salary_from = salary_data.get('from')
    salary_to = salary_data.get('to')
    currency = salary_data.get('currency')

    salary_str = ''

    if salary_from:
        salary_str += f'от {salary_from} '
    if salary_to:
        salary_str += f'до {salary_to} '
    if currency:
        salary_str += currency

    if not salary_str:
        salary_str = "Не указан"

    return salary_str
