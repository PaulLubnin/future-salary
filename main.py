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


if __name__ == '__main__':
    today = datetime.datetime.today()
    month_ago = today - datetime.timedelta(days=30)
    hh_url = 'https://api.hh.ru/vacancies'
    languages = ('JavaScript', 'Java', 'Python', 'Ruby', 'PHP', 'C++', 'C#', 'C', 'Go', 'Swift')
    vacancies = {language: get_vacancies(hh_url, month_ago, today, language) for language in languages}

    python_jobs = vacancies['Python']['items']
    python_salary = [job['salary'] for job in python_jobs]

    pprint(python_salary)

    # offer_count = {language: get_vacancies(hh_url, language).get("found") for language in languages}
    # pprint(offer_count)
