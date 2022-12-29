import os
from itertools import count
from pprint import pprint

import requests
from dotenv import load_dotenv


def get_vacancies(url: str, token: str, lang: str, industry: int = 48, town: str = 'Москва'):
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


def average_salary(all_salaries: list):
    summ = 0
    processed_vacancies = 0
    for salary in all_salaries:
        if not salary:
            continue
        summ += salary
        processed_vacancies += 1
    return {'salary': int(summ / processed_vacancies) if processed_vacancies else None,
            'processed': processed_vacancies}


if __name__ == '__main__':
    load_dotenv()
    sj_token = os.getenv('SUPER_JOB_SECRET_KEY')
    sj_url = 'https://api.superjob.ru/2.0/vacancies/'
    languages = ('JavaScript', 'Java', 'Python', 'Ruby', 'PHP', 'C++', 'C#', 'C', 'Go', 'Swift')

    statics = dict()
    for language in languages:
        vacancies = list()
        vacancies.extend(get_vacancies(sj_url, sj_token, language))
        salaries = [predict_rub_salary(vacancy) for vacancy in vacancies]
        salary_per_job = average_salary(salaries)
        statics[language] = {'vacancies_found': len(vacancies),
                             'vacancies_processed': salary_per_job['processed'],
                             'average_salary': salary_per_job['salary']}
    pprint(statics)
