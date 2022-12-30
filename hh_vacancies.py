import datetime
from itertools import count

import requests

from boot_scripts import average_salary, LANGUAGES, create_table


def get_vacancies(url: str, date_from: datetime, lang: str = '', area: int = 1):
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


def predict_rub_salary(job: dict):
    pay = job['salary']
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


if __name__ == '__main__':
    today = datetime.datetime.today()
    per_month = today - datetime.timedelta(days=30)
    stats_from = ' HeadHunter Moscow '
    hh_url = 'https://api.hh.ru/vacancies'

    statics = dict()
    for language in LANGUAGES:
        vacancies = list()
        vacancies.extend(get_vacancies(hh_url, per_month, lang=language))
        salaries = [predict_rub_salary(vacancy) for vacancy in vacancies]
        salary_per_job = average_salary(salaries)
        statics[language] = {'vacancies_found': len(vacancies),
                             'vacancies_processed': salary_per_job['processed'],
                             'average_salary': salary_per_job['salary']}
    print(create_table(statics, stats_from))
