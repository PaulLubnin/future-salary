import os
from itertools import count

import requests
from dotenv import load_dotenv

from boot_scripts import LANGUAGES, create_table, calculation_salary, create_statistics


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
    return calculation_salary(pay_from, pay_to)


if __name__ == '__main__':
    load_dotenv()
    stats_from = ' SuperJob Moscow '
    sj_token = os.getenv('SUPER_JOB_SECRET_KEY')
    sj_url = 'https://api.superjob.ru/2.0/vacancies/'

    statics = dict()
    for language in LANGUAGES:
        vacancies = list()
        vacancies.extend(get_vacancies(sj_url, sj_token, lang=language))
        statics.update(create_statistics(language, vacancies, predict_rub_salary))
    print(create_table(statics, stats_from))
