from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import csv

p = sync_playwright().start()

browser = p.chromium.launch(headless=False)

page = browser.new_page()

page.goto("https://www.wanted.co.kr/")

# page.screenshot(path = "screenshot.png")
page.click("button.Aside_searchButton__Ib5Dn.Aside_isNotMobileDevice__ko_mZ")
time.sleep(3)

# class 보다는 placeholder가 덜 수정되기 때문에 placeholder 사용
page.get_by_placeholder("검색어를 입력해 주세요.").fill("python")
time.sleep(3)

page.keyboard.down("Enter")
time.sleep(3)

page.click("a#search_tab_position.SearchTabMenu_item__nN_RV")
time.sleep(5)

for _ in range(5):
    time.sleep(5)
    page.keyboard.down("End")

content = page.content()
p.stop()

soup = BeautifulSoup(content, "html.parser")

jobs = soup.find_all("div", class_="JobCard_container__zQcZs JobCard_container--variant-card___dlv1")

jobs_db = []
for job in jobs:
    link = f"https://www.wanted.co.ker{job.find('a')['href']}"

    title = job.find("strong", class_="JobCard_title___kfvj").text
    company_name = job.find("span", class_="JobCard_companyName__kmtE0").text
    reward = job.find("span", class_="JobCard_reward__oCSIQ").text
    
    job = {
        "title": title,
        "company_name": company_name,
        "reward": reward,
        "link": link
    }
    jobs_db.append(job)

file = open("jobs.csv","w")
writer = csv.writer(file)
writer.writerow(["Title", "CompanyName", "Reward", "Link"])

for job in jobs_db:
    writer.writerow(job.values())
