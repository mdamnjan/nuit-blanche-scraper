from selenium import webdriver
from selenium.webdriver.common.by import By


options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

# add an implicit wait to allow the exhibits to load on the page
driver.implicitly_wait(10)
driver.get("https://www.toronto.ca/explore-enjoy/festivals-events/nuitblanche/all-art-projects/")

