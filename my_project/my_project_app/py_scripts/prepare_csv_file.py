import pandas as pd
import numpy as np


def remake_to_rub(vacancy, currency_df):
    vacancy_currency = vacancy['salary_currency']
    if vacancy_currency == 'RUR':
        return vacancy['salary']

    vacancy_date = vacancy['date']
    if vacancy_date in currency_df.index and vacancy_currency in currency_df.columns:
        return vacancy['salary'] * currency_df.at[vacancy_date, vacancy_currency]
    return None


def prepare_vacancies(currency_df, vacancies_df):
    vacancies_df['date'] = pd.to_datetime(vacancies_df['published_at'], errors='coerce', utc=True).dt.strftime('%Y-%m')
    print('date')
    vacancies_df['salary'] = vacancies_df.apply(lambda x: x[['salary_from', 'salary_to']].mean(), axis=1)
    print('sal')
    vacancies_df['salary'] = vacancies_df.apply(lambda x: remake_to_rub(x, currency_df), axis=1)
    print('sal2')
    vacancies_df['key_skills'] = (vacancies_df['key_skills'].apply
                                  (lambda sk: ', '.join([one_skill.strip() for one_skill in str(sk).split('\n')])
                                                                  if isinstance(sk, str) else np.nan))
    print('keys')
    vacancies_df['published_at'] = pd.to_datetime(vacancies_df['published_at'],
                                                  errors='coerce', utc=True).dt.strftime('%Y')
    return vacancies_df


def save_file(remade_vacancies, filename):
    remade_vacancies = remade_vacancies[['name', 'key_skills', 'salary', 'area_name', 'published_at']]
    filtered_vacancies = remade_vacancies[(remade_vacancies['salary'] <= 10000000) | (remade_vacancies['salary'].isna())]
    filtered_vacancies.to_csv(filename, index=False)


def main():
    currency_df = pd.read_csv('csv_prepared_files/currency_values.csv', index_col = 'date')
    vacancies_df = pd.read_csv('csv_prepared_files/vacancies_2024.csv')
    analytics_keys = ['analytic', 'аналитик', 'analyst', 'аналітик']

    remade_vacancies = prepare_vacancies(currency_df, vacancies_df)
    origin_filename = 'csv_prepared_files/prepared_vacancies_2024.csv'
    save_file(remade_vacancies, origin_filename)

    analytic_remade_vacancies = remade_vacancies[remade_vacancies['name'].str.contains('|'.join(analytics_keys), case=False)]
    analytic_filename = 'csv_prepared_files/analytic_prepared_vacancies_2024.csv'
    save_file(analytic_remade_vacancies, analytic_filename)


if __name__ == "__main__":
    main()