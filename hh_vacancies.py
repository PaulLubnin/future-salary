import datetime
from itertools import count
from pprint import pprint

import requests


def get_vacancies(url: str, date_from: datetime, lang: str, area: int = 1):
    for page in count():
        payload = {
            'text': f'программист {lang}',
            'area': area,
            'date_from': date_from.strftime('%Y-%m-%d'),
            'page': page
        }
        response = requests.get(url, params=payload)
        response.raise_for_status()
        page_payload = response.json()
        yield from page_payload['items']
        if page >= 99:
            break


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


def average_salary(all_salaries: list):
    summ = 0
    processed_vacancies = 0
    for salary in all_salaries:
        if not salary:
            continue
        summ += salary
        processed_vacancies += 1
    return {'salary': int(summ / processed_vacancies),
            'processed': processed_vacancies}


if __name__ == '__main__':
    today = datetime.datetime.today()
    per_month = today - datetime.timedelta(days=30)
    hh_url = 'https://api.hh.ru/vacancies'
    languages = ('JavaScript', 'Java', 'Python', 'Ruby', 'PHP', 'C++', 'C#', 'C', 'Go', 'Swift')

    statics = dict()
    for language in languages:
        vacancies = list()
        vacancies.extend(get_vacancies(hh_url, per_month, language))
        salaries = [predict_rub_salary(vacancy) for vacancy in vacancies]
        salary_per_job = average_salary(salaries)
        statics[language] = {'vacancies_found': len(vacancies),
                             'vacancies_processed': salary_per_job['processed'],
                             'average_salary': salary_per_job['salary']}
    pprint(statics)
