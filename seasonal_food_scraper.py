from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True

driver = webdriver.Chrome(options=options)

url = "https://www.seasonalfoodguide.org/veg/asian-pears/alabama"
driver.get(url)

driver.implicitly_wait(5)

produce_name = driver.find_element(By.CSS_SELECTOR, "h3.card_title").text

months_elements = driver.find_elements(By.CSS_SELECTOR, "div.col.m7.s7.xs12 p.card-content")

months = [month.text for month in months_elements]

print(produce_name, months)

driver.quit()
