import pandas as pd
import matplotlib.pyplot as plt
import re


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
    plt.pie(sorted_vac_by_city['percent'],
            labels=sorted_vac_by_city['area_name'],
            autopct='%1.1f%%',
            startangle=90,
            wedgeprops={"edgecolor": "0", 'linewidth': 1, 'linestyle': 'solid',
                        'antialiased': True})
    plt.title('Распределение вакансий по городам', fontsize=16)
    plt.tight_layout()
    plt.savefig(name)


import pandas as pd
import re
import matplotlib.pyplot as plt


def prepare_skills_df(df):
    df.loc[:, 'key_skills'] = df['key_skills'].fillna('')

    def split_skills(skills_str):
        if not skills_str:
            return []
        remade_skills = re.split(r',|\n', skills_str)
        return [skill.strip() for skill in remade_skills if skill.strip()]

    df.loc[:, 'key_skills'] = df['key_skills'].apply(split_skills)

    def count_skills(skills_lists):
        all_skills = []
        for current_skills_list in skills_lists:
            if isinstance(current_skills_list, list):
                all_skills.extend(current_skills_list)
        return pd.Series(all_skills).value_counts()

    skills_by_year = (df.groupby('published_at')['key_skills']
                      .apply(count_skills)
                      .unstack(fill_value=0))

    top_skill_by_year = pd.DataFrame(columns=['published_at', 'top_skill', 'count'])

    for year in skills_by_year.index:
        if not skills_by_year.loc[year].empty:
            top_skill = skills_by_year.loc[year].idxmax()
            count = skills_by_year.loc[year].max()
            top_skill_by_year = pd.concat(
                [top_skill_by_year, pd.DataFrame([{'published_at': year, 'top_skill': top_skill, 'count': count}])],
                ignore_index=True)
        else:
            top_skill_by_year = pd.concat(
                [top_skill_by_year, pd.DataFrame([{'published_at': year, 'top_skill': None, 'count': 0}])],
                ignore_index=True)

    return top_skill_by_year


def create_top_skills(df, name):
    top_skills_by_year = prepare_skills_df(df)
    plt.figure(figsize=(10, 8))
    x_values = top_skills_by_year['published_at'].astype(int)
    y_values = top_skills_by_year['count']
    skills = top_skills_by_year['top_skill']
    plt.title('Топ навыков по годам', fontsize=16)
    plt.xlabel('Год', fontsize=14)
    plt.ylabel('Количество использований навыка', fontsize=14)
    elements = plt.bar(x_values, y_values, color='#23b32a')

    plt.grid(axis='y')
    plt.xticks(ticks=x_values, labels=x_values, rotation=90, fontsize=10)
    plt.yticks(fontsize=10)

    for bar, skill in zip(elements, skills):
        value = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, value / 4 + 0.05,
                 skill, ha='center', va='bottom', rotation=90, fontsize=10)

    plt.tight_layout()
    plt.savefig(name)



def main():
    analytics_df = pd.read_csv('csv_prepared_files/analytic_prepared_vacancies_2024.csv')
    vacancies_df = pd.read_csv('csv_prepared_files/prepared_vacancies_2024.csv')
    #create_salary_by_years(vacancies_df, 'all_stats/salary_by_years.png')
    #create_salary_by_years(analytics_df, 'relevance_photos/salary_by_years.png')
    #create_vac_by_years(vacancies_df, 'all_stats/vac_by_years.png')
    #create_vac_by_years(analytics_df, 'relevance_photos/vac_by_years.png')
    #create_salary_by_area(vacancies_df, 'all_stats/salary_by_area.png')
    #create_salary_by_area(analytics_df, 'geography_photos/salary_by_area.png')
    #create_vac_by_area(vacancies_df, 'all_stats/vac_by_area.png')
    #create_vac_by_area(analytics_df, 'geography_photos/vac_by_area.png')
    #create_top_skills(vacancies_df, 'all_stats/top_skills.png')
    #create_top_skills(analytics_df, 'top-skills_photos/top_skills.png')


if __name__ == "__main__":
    main()