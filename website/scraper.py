from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
service = ChromeService(executable_path="/usr/lib/chromium-browser/chromedriver")
driver = webdriver.Chrome(service=service, options=options)


def get_data(store: int, search: str) -> list[dict]:
    # Gets data for the store represented by an integer "store" and for the search "search".
    # 0 for nofrills
    # 1 for loblaws
    # 2 for metro
    if store == 0:
        return get_nofrills_data(search)
    elif store == 1:
        return get_loblaws_data(search)
    elif store == 2:
        return get_metro_data(search)
    else:
        raise Exception("Error. There is no store associated with that number!")


def get_nofrills_data(search: str) -> list[dict]:
    # Given a search, returns a list of dictionaries. The dictionaries are written with three entries:
    # ["name": name[str], "price": price[float], "unit": unit[str]]
    # "name" is name of item
    # If no price can be found, then the price is 0.0.
    # If no units can be found, then unit is "No Units"
    driver.get('https://www.nofrills.ca/search?search-bar=' + search)
    time.sleep(10)
    source = driver.page_source

    # def get_data_from_search()

    soup = BeautifulSoup(source, 'lxml')

    # We need to get the name, price, and quantity (in grams).

    # something = soup.find_all("a")

    item_selector = soup.find_all('div', class_="product-tracking")

    name_classes = []
    price_classes = []
    unit_classes = []
    for i in item_selector:
        soup = BeautifulSoup(str(i), 'lxml')
        name_class = soup.find_all('span', class_='product-name__item product-name__item--name')
        price_class = soup.find_all('span', class_='price__value comparison-price-list__item__price__value')
        unit_class = soup.find_all('span', class_='price__unit comparison-price-list__item__price__unit')
        name_classes.append(name_class)
        price_classes.append(price_class)
        unit_classes.append(unit_class)

    names = []
    price_per_100grams = []
    units = []
    for i in name_classes:
        soup = BeautifulSoup(str(i), 'lxml')
        names.append(soup.get_text())
    for i in price_classes:
        soup = BeautifulSoup(str(i), 'lxml')
        price_per_100grams.append(soup.get_text())
    for i in unit_classes:
        soup = BeautifulSoup(str(i), 'lxml')
        units.append(soup.get_text())
    print(price_per_100grams)

    # This code is to deal with cases when no price or units can be found.

    finalprice_per_100grams = []

    for i in price_per_100grams:
        i = i.replace("[", " ")
        i = i.replace("]", " ")
        i = i.replace("$", " ")
        i = i.replace(",", " ")
        CANNOT = True
        try:
            float(i)
        except:
            finalprice_per_100grams.append('0')
            CANNOT = False
        if CANNOT:
            finalprice_per_100grams.append(i)

    finalunits = []
    for i in units:
        if '100g' not in i and not "100ml" in i:
            finalunits.append('No Units')
        else:
            finalunits.append(i)

    final_list = []
    for i in range(0, len(names)):
        final_list.append({"name": names[i].strip("[]"), "price": float(finalprice_per_100grams[i]),
                           "units": finalunits[i].strip("[]/")})

    return final_list


def get_loblaws_data(search: str) -> list[dict]:
    # Given a search, returns a list of dictionaries. The dictionaries are written with three entries:
    # ["name": name[str], "price": price[float], "unit": unit[str]]
    # "name" is name of item
    # If no price can be found, then the price is 0.0.
    # If no units can be found, then unit is "No Units"

    driver.get('https://www.loblaws.ca/search?search-bar=' + search)
    time.sleep(10)
    source = driver.page_source

    # def get_data_from_search()

    soup = BeautifulSoup(source, 'lxml')

    # We need to get the name, price, and quantity (in grams).

    # something = soup.find_all("a")

    item_selector = soup.find_all('div', class_="product-tile product-tile--marketplace")
    # print(item_selector)

    name_classes = []
    price_classes = []
    unit_classes = []
    for i in item_selector:
        soup = BeautifulSoup(str(i), 'lxml')
        name_class = soup.find_all('span', class_='product-name__item product-name__item--name')
        price_class = soup.find_all('span', class_='price__value comparison-price-list__item__price__value')
        unit_class = soup.find_all('span', class_='price__unit comparison-price-list__item__price__unit')
        name_classes.append(name_class)
        price_classes.append(price_class)
        unit_classes.append(unit_class)
    # print(price_classes)
    # print(name_classes)

    names = []
    price_per_100grams = []
    units = []
    for i in name_classes:
        soup = BeautifulSoup(str(i), 'lxml')
        names.append(soup.get_text())
    for i in price_classes:
        soup = BeautifulSoup(str(i), 'lxml')
        price_per_100grams.append(soup.get_text())
    for i in unit_classes:
        soup = BeautifulSoup(str(i), 'lxml')
        units.append(soup.get_text())

    # This code is to deal with cases when no price or units can be found.

    finalprice_per_100grams = []

    for i in price_per_100grams:
        i = i.replace("[", " ")
        i = i.replace("]", " ")
        i = i.replace("$", " ")
        i = i.replace(",", " ")
        CANNOT = True
        try:
            float(i)
        except:
            finalprice_per_100grams.append('0')
            CANNOT = False
        if CANNOT:
            finalprice_per_100grams.append(i)

    finalunits = []
    for i in units:
        if '100g' not in i and not "100ml" in i:
            finalunits.append('No Units')
        else:
            finalunits.append(i)

    final_list = []
    for i in range(0, len(names)):
        final_list.append({"name": names[i].strip("[]"), "price": float(finalprice_per_100grams[i]),
                           "units": finalunits[i].strip("[]/")})

    return final_list


def get_metro_data(search: str) -> list[dict]:
    # Given a search, returns a list of dictionaries. The dictionaries are written with three entries:
    # ["name": name[str], "price": price[float], "unit": unit[str]]
    # "name" is name of item
    # If no price can be found, then the price is 0.0.
    # If no units can be found, then unit is "No Units"
    driver.get('https://www.metro.ca/en/online-grocery/search?filter=' + search)
    time.sleep(10)
    source = driver.page_source

    # def get_data_from_search()

    soup = BeautifulSoup(source, 'lxml')

    # We need to get the name, price, and quantity (in grams).

    # something = soup.find_all("a")

    item_selector = soup.find_all('div', class_="default-product-tile tile-product item-addToCart")

    name_classes = []
    price_classes = []
    # unit_classes = []
    for i in item_selector:
        soup = BeautifulSoup(str(i), 'lxml')
        name_class = soup.find_all('div', class_='head__title')
        price_class = soup.find_all('div', class_='pricing__secondary-price')
        # unit_class = soup.find_all('span', class_='price__unit comparison-price-list__item__price__unit')
        name_classes.append(name_class)
        price_classes.append(price_class)
        # unit_classes.append(unit_class)

    names = []
    price_per_100grams = []
    # units = []
    for i in name_classes:
        soup = BeautifulSoup(str(i), 'lxml')
        names.append(soup.get_text())
    for i in price_classes:
        soup = BeautifulSoup(str(i), 'lxml')
        price_per_100grams.append(soup.get_text())

    # for i in unit_classes:
    #     soup = BeautifulSoup(str(i), 'lxml')
    #     units.append(soup.get_text())

    # This code is to deal with cases when no price or units can be found.

    # Separating prices and units
    fixed_price_per100grams = []
    fixed_units = []
    for element in price_per_100grams:
        item = element.replace("[\n", "").replace("\n]", "").replace("/", "").split(" ")
        fixed_price_per100grams.append(item[0])
        fixed_units.append(item[1])

    finalprice_per_100grams = []

    for i in fixed_price_per100grams:
        i = i.replace("[", " ")
        i = i.replace("]", " ")
        i = i.replace("$", " ")
        i = i.replace(",", " ")

        CANNOT = True
        try:
            float(i)
        except:
            finalprice_per_100grams.append('0')
            CANNOT = False
        if CANNOT:
            finalprice_per_100grams.append(i)

    finalunits = []
    for i in fixed_units:
        if '100g' not in i and not "100ml" in i:
            finalunits.append('No Units')
        else:
            finalunits.append(i)

    final_list = []
    for i in range(0, len(names)):
        final_list.append({"name": names[i].strip("[]"), "price": float(finalprice_per_100grams[i]),
                           "units": finalunits[i]})

    return final_list
