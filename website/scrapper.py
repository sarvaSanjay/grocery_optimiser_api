import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
driver = webdriver.Chrome()

driver.get('https://www.nofrills.ca/search?search-bar=cheese')
time.sleep(15)
source = driver.page_source


#def get_data_from_search()


soup = BeautifulSoup(source, 'lxml')

# We need to get the name, price, and quantity (in grams).

# something = soup.find_all("a")


names_selector = soup.find_all('span', class_="product-name__item product-name__item--name")
for i in names_selector:
    i.get_text()
    print(i)
#print(names_selector)




