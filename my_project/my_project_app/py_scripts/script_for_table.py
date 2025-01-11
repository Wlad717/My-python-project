import pandas as pd
import re


def prepare_salary_by_years(df):
    salary_by_years = df.groupby('published_at')['salary'].mean().reset_index().astype(int)
    return salary_by_years


def prepare_vac_by_years(df):
    vac_by_years = df.groupby('published_at')['name'].count().reset_index()
    return vac_by_years


def prepare_salary_by_area(df):
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
    return sorted_salary_by_area


def prepare_vac_by_area(df):
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
    return sorted_vac_by_city


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
