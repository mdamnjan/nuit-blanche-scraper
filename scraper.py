from selenium import webdriver
from selenium.webdriver.common.by import By


options = webdriver.ChromeOptions()
options.add_experimental_option("detach", False)
driver = webdriver.Chrome(options=options)

# add an implicit wait to allow the exhibits to load on the page
driver.implicitly_wait(20)
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
   
def get_exhibit_details(href):
    driver.get(href)

    project_details = driver.find_element(By.CLASS_NAME, "project-details-inner")
    title = driver.find_element(By.TAG_NAME, "h1").text
    print(title)
    exhibit_number = project_details.find_element(By.TAG_NAME, "text").text
    print(exhibit_number)
    artists = driver.find_element(By.XPATH, "//li[strong[contains(text(), 'Artists')]]").text
    print(artists)
    medium = driver.find_element(By.XPATH, "//li[strong[contains(text(), 'Medium')]]").text
    print(medium)
    project_type = driver.find_element(By.XPATH, "//li[strong[contains(text(), 'Project Type')]]").text
    print(project_type)
    address = driver.find_element(By.XPATH, "//li[strong[contains(text(), 'Address')]]").text
    print(address)
    physical_access = driver.find_element(By.XPATH, "//li[strong[contains(text(), 'Physical Access')]]").text
    print(physical_access)


exhibit_links = get_exhibit_links()

# exhibit_details = []
# for link in exhibit_links:
#     exhibit_details.append(get_exhibit_details(link))


get_exhibit_details("https://www.toronto.ca/explore-enjoy/festivals-events/nuitblanche/all-art-projects/details/2023/project/translunar-formations-nathan-phillips-square/")