import requests
from pprint import pprint


def get_vacancies(hh_url: str, language: str = 'Python', ):

    payload = {
        'text': f'программист',
        'area': 1,
        'date_from': '2022-11-25',
        'date_to': '2022-12-25'
    }
    response = requests.get(hh_url, params=payload)
    response.raise_for_status()
    return response.json()


if __name__ == '__main__':
    hh_url = 'https://api.hh.ru/vacancies'
    languages = ('JavaScript', 'Java', 'Python', 'Ruby', 'PHP', 'C++', 'C#', 'C', 'Go', 'Swift')

    vacancies = get_vacancies(hh_url)
    pprint(vacancies)
