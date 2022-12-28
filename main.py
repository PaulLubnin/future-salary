import datetime
from pprint import pprint

import requests


def get_vacancies(hh_url: str, date_from: datetime, date_to: datetime, language: str):
    payload = {
        'text': f'программист {language}',
        'area': 1,
        'date_from': date_from.strftime('%Y-%m-%d'),
        'date_to': date_to.strftime('%Y-%m-%d')
    }
    response = requests.get(hh_url, params=payload)
    response.raise_for_status()
    return response.json()


def predict_rub_salary(vacancy: dict):
    pay = vacancy['salary']
    if not pay:
        return
    if pay['currency'] != 'RUR':
        return
    if pay['from'] and pay['to']:
        return (pay['from'] + pay['to']) / 2
    if not pay['to']:
        return pay['from'] * 1.2
    if not pay['from']:
        return pay['to'] * 0.8


def average_salary(salary_job: list):

    summ = 0
    count = 0
    for integer in salary_job:
        if not integer:
            continue
        summ += integer
        count += 1
    return {'salary': int(summ / count),
            'processed': count}


if __name__ == '__main__':
    today = datetime.datetime.today()
    month_ago = today - datetime.timedelta(days=30)
    hh_url = 'https://api.hh.ru/vacancies'
    languages = ('JavaScript', 'Java', 'Python', 'Ruby', 'PHP', 'C++', 'C#', 'C', 'Go', 'Swift')

    statics = dict()
    for language in languages:
        vacancies = get_vacancies(hh_url, month_ago, today, language)
        salary = [predict_rub_salary(vacancy) for vacancy in vacancies['items']]
        salary_per_job = average_salary(salary)
        statics[language] = {'vacancies_found': vacancies['found'],
                             'vacancies_processed': salary_per_job['processed'],
                             'average_salary': salary_per_job['salary']}
    pprint(statics)
