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
    artists = artists.split(':')[1].strip()
    medium = driver.find_element(By.XPATH, "//li[strong[contains(text(), 'Medium')]]").text
    medium = medium.split(':')[1].strip()
    address = driver.find_element(By.XPATH, "//li[strong[contains(text(), 'Address')]]").text.split('\n')[0]
    address = address.split(':')[1].strip()
    physical_access = driver.find_element(By.XPATH, "//li[strong[contains(text(), 'Physical Access')]]").text
    physical_access = physical_access.split(':')[1].strip()

    # optional information that may or may not exist
    project_type = None
    try: 
        project_type = driver.find_element(By.XPATH, "//li[strong[contains(text(), 'Project Type')]]").text
        project_type = project_type.split(':')[1].strip()

    except NoSuchElementException:
        pass
    
    # This exhibit is missing the address on the detail page
    if title == "Avian":
        address = "The Bentway"
    if title == "Assemblies":
        address = "Hagerman St. Parking Lot"

    return {"Title": title, "Exhibit Number": exhibit_number, "Address": address + " ON", "Link": link, "Artists": artists, "Medium": medium, "Physical Access": physical_access, "Project Type": project_type}

def get_exhibit_data(exhibit_links):
    exhibits = []
    for link in exhibit_links:
        data = get_exhibit_details(link)
        exhibits.append(data)

    # sort by exhibit number
    return sorted(exhibits, key=lambda x: int(x["Exhibit Number"]))


def write_exhibits_to_csv(exhibits):
    header = ['Title', 'Exhibit Number', 'Address', 'Link', 'Artists', 'Medium', 'Physical Access', 'Project Type']

    with open('exhibits.csv', 'w', encoding='UTF8') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(exhibits)


exhibit_links = get_exhibit_links()
exhibits = get_exhibit_data(exhibit_links)
write_exhibits_to_csv(exhibits)