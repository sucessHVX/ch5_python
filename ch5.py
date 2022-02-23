import csv
import requests
from bs4 import BeautifulSoup
import os

os.system("cls")


def input_company(company):
    file = open(f"{company['name']}.csv", mode="w")
    writer = csv.writer(file)
    writer.writerow(["place", "title", "time", "pay", "date"])
    for job in company["jobs"]:
        writer.writerow(list(job.values()))


url = "http://www.alba.co.kr/"
request = requests.get(url)
soup = BeautifulSoup(request.text, "html.parser")
main = soup.find("div", {"id": "MainSuperBrand"})
brand = main.find_all("li", {"class": "impact"})

for brands in brand:
    link = brands.find("a", {"class": "goodsBox-info"})
    name = brands.find("span", {"class": "company"})
    if link and name:
        link = link["href"]
        name = name.text
        name = name.replace("/", "_")
        company = {"name": name, "jobs": []}
        jobs_request = requests.get(link)
        jobs_soup = BeautifulSoup(jobs_request.text, "hteml.parser")
        tbody = jobs_soup.find("div", {"id": "NormalInfo"}).find("tbody")
        rows = tbody.find_all("tr", {"class": ["", "divide"]})
        for row in rows:
            place = row.find("td", {"class": "local"})
            if place:
                place = place.text.replace(u"\xa0", " ")

            title = row.find("td", {"class": "title"})
            if title:
                title = title.find("a").find(
                    "span", {"class": "company"}).text.strip()
                title = title.replace(u"\xa0", " ")

            time = row.find("td", {"class": "data"})
            if time:
                time = time.text.replace(u"\xa0", " ")

            pay = row.find("td", {"class": "pay"})
            if pay:
                pay = pay.text.replace(u"\xa0", " ")

            date = row.find("td", {"class": "date"})
            if date:
                date = date.text.replace(u"\xa0", " ")

            job = {
                "place": place,
                "title": title,
                "time": time,
                "pay": pay,
                "date": date,
            }
            company["jobs"].append(job)

        input_company(company)
