import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def create_salary_by_years(df, name):
    salary_by_years = df.groupby('published_at')['salary'].mean()
    plt.figure(figsize=(10, 8))
    plt.plot(salary_by_years.index, salary_by_years.values, marker='o', linestyle='solid', color='#E8874B')
    plt.title('Динамика уровня зарплат по годам в рублях', fontsize=16)
    plt.xlabel('Год', fontsize=14)
    plt.ylabel('Средняя з/п в рублях', fontsize=14)
    min_year = salary_by_years.index.min()
    max_year = salary_by_years.index.max()
    plt.xticks(range(min_year, max_year + 1, 3))
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(name)


def create_vac_by_years(df, name):
    vac_by_years = df.groupby('published_at')['name'].count()
    plt.figure(figsize=(10, 8))
    vac_by_years.plot(kind='bar', color='#43C3EC')
    plt.title('Динамика количества вакансий по годам', fontsize=16)
    plt.xlabel('Год', fontsize=14)
    plt.ylabel('Количество вакансий', fontsize=14)
    plt.xticks(rotation=90)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(name)


def create_salary_by_area(df, name):
    total_vacancies = len(df)
    sorted_salary_by_area = (
        df
        .groupby('area_name')
        .agg({'salary': 'mean', 'name': 'count'})
        .assign(perc=lambda df: df['name'] / total_vacancies)
        .sort_values(['salary', 'area_name'], ascending=[False, True])
        .query('perc >= 0.01')
        .astype(int)
        .reset_index()
    )

    plt.figure(figsize=(10, 8))
    plt.plot(sorted_salary_by_area['area_name'], sorted_salary_by_area['salary'], marker='o', linestyle='solid', color='#925CE5')
    plt.title('Динамика уровня зарплат по городам в рублях', fontsize=16)
    plt.xlabel('Город', fontsize=14)
    plt.ylabel('Средняя з/п в рублях', fontsize=14)
    plt.xticks(rotation=90)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(name)


def create_vac_by_area(df, name):
    total_vacancies = len(df)
    sorted_vac_by_city = (
        df
        .groupby('area_name')
        .agg({'name': 'count'})
        .assign(percent=lambda df: df['name'] / total_vacancies)
        .round(4)
        .sort_values(['percent', 'area_name'], ascending=[False, True])
        .query('percent >= 0.01')
        .reset_index()
    )

    plt.figure(figsize=(10, 8))
    plt.bar(sorted_vac_by_city['area_name'], sorted_vac_by_city['percent'], color='#6DE663', width=0.7)
    plt.title('Динамика количества вакансий по городам', fontsize=16)
    plt.xlabel('Город', fontsize=14)
    plt.ylabel('Количество вакансий', fontsize=14)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(name)


def main():
    analytics_df = pd.read_csv('csv_prepared_files/analytic_prepared_vacancies_2024.csv')
    vacancies_df = pd.read_csv('csv_prepared_files/prepared_vacancies_2024.csv')
    create_salary_by_years(vacancies_df, 'all_stats/salary_by_years.png')
    create_salary_by_years(analytics_df, 'relevance_photos/salary_by_years.png')
    create_vac_by_years(vacancies_df, 'all_stats/vac_by_years.png')
    create_vac_by_years(analytics_df, 'relevance_photos/vac_by_years.png')
    create_salary_by_area(vacancies_df, 'all_stats/salary_by_area.png')
    create_salary_by_area(analytics_df, 'geography_photos/salary_by_area.png')
    create_vac_by_area(vacancies_df, 'all_stats/vac_by_area.png')
    create_vac_by_area(analytics_df, 'geography_photos/vac_by_area.png')


if __name__ == "__main__":
    main()