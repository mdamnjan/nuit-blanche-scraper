from selenium import webdriver
from selenium.webdriver.common.by import By


options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
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
   
def get_exhibit_details(href):
    driver.get(href)


exhibit_links = get_exhibit_links()
