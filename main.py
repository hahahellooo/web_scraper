import requests
from bs4 import BeautifulSoup

def scrape_page(url):
    response = requests.get(url)
    soup  = BeautifulSoup(response.content, "html.parser")

    jobs = soup.find("section", class_="jobs").find_all("li")[:-1]

    all_jobs = []
    for job in jobs:
        title = job.find("h4", class_="new-listing__header__title").text
        region = job.find("p", class_="new-listing__company-headquarters")
        if region: # NONE 같이 나오는 문제 해결해야함
            region = region.text.replace('"','').strip()
        company = job.find("p", class_="new-listing__company-name")
        if company:
            company = company.text.replace('"','').strip()
        positions = job.find_all("p", class_="new-listing__categories__category")
        position_list = ["Full-Time", "Contract"]
        for position in positions:
            position_text = position.text.strip()
            if position_text in position_list:
                position = position_text
                break
            else:
                continue
        
        # next_sibling을 이용하여 div 속성에 있는 href말고 그 아래줄에 있는 href 링크를 추출할 수 있다. 
        link = job.find("div", class_ = "tooltip--flag-logo").next_sibling["href"]
       
        url = f'https://weworkremotely.com{link}'
        job_data = {
             "title": title,
             "company": company,
             "position": position,
             "region": region,
             "url": url
        }
        all_jobs.append(job_data)
    print(all_jobs)
   

 

  

url = "https://weworkremotely.com/categories/remote-full-stack-programming-jobs#job-listings"
scrape_page(url)  
