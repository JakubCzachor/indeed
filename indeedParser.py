#Indeed Job Scraper
#Input: Job, Location
#Output: Array of jobs, and corresponding salaries for the position
#Packages: Selenium for http requests, BeautifulSoup for html parsing

from selenium import webdriver
from bs4 import BeautifulSoup
import re

job = input("Enter Job Description: ")
job = "+".join(job.split(" "))
location = input("Enter City, State: ")
location = "%2C".join(location.split(","))
location = "+".join(location.split(" "))
url = f'https://www.indeed.com/jobs?q={job}&l={location}'


options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)

#Get request
driver.get(url)

page_content = driver.page_source
soup = BeautifulSoup(page_content, 'html.parser')

result_elements = soup.find_all('div', class_='result')
jobCollection = []

for result in result_elements:
    metadata_container = result.find('div', class_='metadata salary-snippet-container')
    job_title_element = result.find('span', id=re.compile(r'jobTitle-\w+'))

    if metadata_container and job_title_element:
        metadata_text = metadata_container.get_text()
        job_title_text = job_title_element.get_text()
        jobCollection.append((f"{job_title_text}", f"{metadata_text}"))

#Prints result
for job, salary in jobCollection:
    print(f"Job Title: {job} - Salary: {salary}")

driver.quit()
