import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", False)
driver = webdriver.Chrome(options=options)

# add an implicit wait to allow the exhibits to load on the page
driver.implicitly_wait(10)
driver.get("https://www.toronto.ca/explore-enjoy/festivals-events/nuitblanche/all-art-projects/")

def get_exhibit_links():
    exhibits = []
    has_more_pages = True
    while has_more_pages:
        new_exhibits = driver.find_elements(By.XPATH, "//a[contains(@class, 'moreInfo')]")

        for exhibit in new_exhibits:
            exhibits.append(exhibit.get_attribute('href'))

        next_page_button = driver.find_element(By.CLASS_NAME, "nextPageButton")
        
        # the 'next' button on the last page isn't actually disabled for whatever reason
        # but it has the aria-disabled label
        if next_page_button.get_attribute('aria-disabled'):
            has_more_pages = False
            break
        next_page_button.click()

    return exhibits
   
def get_exhibit_details(link):
    driver.get(link)

    project_details = driver.find_element(By.CLASS_NAME, "project-details-inner")

    title = driver.find_element(By.TAG_NAME, "h1").text
    exhibit_number = project_details.find_element(By.TAG_NAME, "text").text
    artists = driver.find_element(By.XPATH, "//li[strong[contains(text(), 'Artist')]]").text
    medium = driver.find_element(By.XPATH, "//li[strong[contains(text(), 'Medium')]]").text
    address = driver.find_element(By.XPATH, "//li[strong[contains(text(), 'Address')]]").text.split('\n')[0]
    physical_access = driver.find_element(By.XPATH, "//li[strong[contains(text(), 'Physical Access')]]").text

    # optional information that may or may not exist
    project_type = None
    try: 
        project_type = driver.find_element(By.XPATH, "//li[strong[contains(text(), 'Project Type')]]").text
    except NoSuchElementException:
        pass

    return [title, exhibit_number, address, link, artists, medium, physical_access, project_type]


exhibit_links = get_exhibit_links()


def write_exhibits_to_csv():
    header = ['title', 'exhibit_number', 'address', 'link', 'artists', 'medium', 'physical_access', 'project_type']

    with open('exhibits.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)

        for link in exhibit_links:
            data = get_exhibit_details(link)

            writer.writerow(data)


write_exhibits_to_csv()