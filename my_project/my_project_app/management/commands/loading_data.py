from django.core.management.base import BaseCommand
from django.conf import settings
import pandas as pd
from my_project_app.models import *
from my_project_app.py_scripts.script_for_table import *
import os



class Command(BaseCommand):
    help = 'Загрузка данных в таблицы'

    def handle(self, *args, **options):
        vac_df = pd.read_csv(os.path.join(settings.PATH_TO_CSV, 'prepared_vacancies_2024.csv'))
        analytic_df = pd.read_csv(os.path.join(settings.PATH_TO_CSV, 'analytic_prepared_vacancies_2024.csv'))

        all_stats_salary_year = prepare_salary_by_years(vac_df)
        all_stats_vac_year = prepare_vac_by_years(vac_df)
        all_stats_salary_area = prepare_salary_by_area(vac_df)
        all_stats_vac_area = prepare_vac_by_area(vac_df)
        all_stats_skills = prepare_skills_df(vac_df)

        analytic_salary_year = prepare_salary_by_years(analytic_df)
        analytic_vac_year = prepare_vac_by_years(analytic_df)
        analytic_salary_area = prepare_salary_by_area(analytic_df)
        analytic_vac_area = prepare_vac_by_area(analytic_df)
        analytic_skills = prepare_skills_df(analytic_df)

        AllStatsSalaryCity.objects.all().delete()
        AllStatsSalaryYear.objects.all().delete()
        AllStatsVacanciesCity.objects.all().delete()
        AllStatsVacanciesYear.objects.all().delete()
        AllStatsTopSkills.objects.all().delete()
        GeographySalaryCity.objects.all().delete()
        GeographyVacanciesCity.objects.all().delete()
        RelevanceSalaryYear.objects.all().delete()
        RelevanceVacanciesYear.objects.all().delete()
        SkillsTopSkills.objects.all().delete()

        for index, row in all_stats_salary_year.iterrows():
            AllStatsSalaryYear.objects.create(
                salary = row['salary'],
                date = row['published_at'],
            )

        for index, row in all_stats_vac_year.iterrows():
            AllStatsVacanciesYear.objects.create(
                vacancies_count = row['name'],
                date = row['published_at'],
            )

        for index, row in all_stats_salary_area.iterrows():
            AllStatsSalaryCity.objects.create(
                salary = row['salary'],
                city = row['area_name'],
            )

        for index, row in all_stats_vac_area.iterrows():
            AllStatsVacanciesCity.objects.create(
                vacancies_count = row['percent'],
                city = row['area_name'],
            )

        for index, row in all_stats_skills.iterrows():
            AllStatsTopSkills.objects.create(
                current_skill = row['top_skill'],
                skill_count = row['count'],
                date = row['published_at'],
            )


        for index, row in analytic_salary_year.iterrows():
            RelevanceSalaryYear.objects.create(
                salary = row['salary'],
                date = row['published_at'],
            )

        for index, row in analytic_vac_year.iterrows():
            RelevanceVacanciesYear.objects.create(
                vacancies_count = row['name'],
                date = row['published_at'],
            )

        for index, row in analytic_salary_area.iterrows():
            GeographySalaryCity.objects.create(
                salary = row['salary'],
                city = row['area_name'],
            )

        for index, row in analytic_vac_area.iterrows():
            GeographyVacanciesCity.objects.create(
                vacancies_count = row['percent'],
                city = row['area_name'],
            )

        for index, row in analytic_skills.iterrows():
            SkillsTopSkills.objects.create(
                current_skill = row['top_skill'],
                skill_count = row['count'],
                date = row['published_at'],
            )

