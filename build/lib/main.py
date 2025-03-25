import requests
url = "https://weworkremotely.com/categories/remote-full-stack-programming-jobs#job-listings"
response = requests.get(url)
print(response.content)