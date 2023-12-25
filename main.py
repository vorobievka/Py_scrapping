import requests
from bs4 import BeautifulSoup
import json
from fake_headers import Headers


def print_to_file(list_data):
    with open('vacancy.json', 'w', encoding='utf-8') as f:
        json.dump(list_data, f, ensure_ascii=False, indent=4)


headers_generator = Headers(os="win", browser="chrome", headers=True)
response = requests.get("https://spb.hh.ru/search/vacancy?text=python&area=1&area=2",
                        headers=headers_generator.generate())
main_html_data = response.text
main_soup = BeautifulSoup(main_html_data, "lxml")
vacancy_list = main_soup.find("main", class_="vacancy-serp-content")
vacancies = vacancy_list.findAll("div", class_="serp-item")

vacancy_data = []

for article_tag in vacancies:
    company_name_tag = article_tag.find("a", class_="bloko-link bloko-link_kind-tertiary")
    vacancy_link_tag = article_tag.find("a", class_="serp-item__title")
    vacancy_address_tag = article_tag.find("div", {'data-qa': 'vacancy-serp__vacancy-address'})
    vacancy_compensation_tag = article_tag.find("span", {'data-qa': 'vacancy-serp__vacancy-compensation'})
    company_name = company_name_tag.text.strip()
    vacancy_link = vacancy_link_tag["href"]
    vacancy_title = vacancy_link_tag.text.strip()
    vacancy_address = vacancy_address_tag.text.strip()

    if vacancy_compensation_tag:
        vacancy_compensation = vacancy_compensation_tag.text.strip()
    else:
        vacancy_compensation = ""

    description = requests.get(vacancy_link, headers=headers_generator.generate())
    description_html_data = description.text

    if "Django" in description_html_data or "Flask" in description_html_data:
        vacancy_data.append(
            {
                "vacancy_title": vacancy_title,
                "company_name": company_name,
                "vacancy_address": vacancy_address,
                "vacancy_compensation": vacancy_compensation,
                "vacancy_link": vacancy_link
            }
        )
print_to_file(vacancy_data)
