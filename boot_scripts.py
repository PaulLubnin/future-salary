from __future__ import print_function

from terminaltables import SingleTable

LANGUAGES = ('JavaScript', 'Java', 'Python', 'Ruby', 'PHP', 'C++', 'C#', 'C', 'Go', 'Swift')


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


def create_table(job_stats: dict, stats_from: str):
    title = stats_from
    statistics_table = [
        ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата'],
    ]
    for language, stats in job_stats.items():
        statistics_table.append([language, stats['vacancies_found'], stats['vacancies_processed'], stats['average_salary']]),
    table_instance = SingleTable(statistics_table, title)
    for column in range(4):
        table_instance.justify_columns[column] = 'right'
    return table_instance.table
