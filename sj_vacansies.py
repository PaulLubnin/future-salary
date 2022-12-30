import os
from itertools import count

import requests
from dotenv import load_dotenv

from boot_scripts import LANGUAGES, create_table, average_salary


def get_vacancies(url: str, token: str, lang: str = '', industry: int = 48, town: str = 'Москва'):
    for page in count():
        header = {
            'X-Api-App-Id': token
        }
        payload = {
            'catalogues': industry,
            'town': town,
            'keyword': lang,
            'page': page
        }
        response = requests.get(url, headers=header, params=payload)
        response.raise_for_status()
        page_payload = response.json()
        yield from page_payload['objects']
        if not page_payload['more']:
            break


def predict_rub_salary(job: dict):
    pay_from, pay_to = job['payment_from'], job['payment_to']
    if not pay_from and not pay_to:
        return None
    if pay_from and pay_to:
        return (pay_from + pay_to) / 2
    if not pay_to:
        return pay_from * 1.2
    if not pay_from:
        return pay_to * 0.8


if __name__ == '__main__':
    load_dotenv()
    stats_from = ' SuperJob Moscow '
    sj_token = os.getenv('SUPER_JOB_SECRET_KEY')
    sj_url = 'https://api.superjob.ru/2.0/vacancies/'

    statics = dict()
    for language in LANGUAGES:
        vacancies = list()
        vacancies.extend(get_vacancies(sj_url, sj_token, lang=language))
        salaries = [predict_rub_salary(vacancy) for vacancy in vacancies]
        salary_per_job = average_salary(salaries)
        statics[language] = {'vacancies_found': len(vacancies),
                             'vacancies_processed': salary_per_job['processed'],
                             'average_salary': salary_per_job['salary']}
    print(create_table(statics, stats_from))
