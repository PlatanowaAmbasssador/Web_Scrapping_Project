#### Importing Libraries ####

import io
import pickle
import time

import numpy as np
import pandas as pd
import requests
from tqdm import tqdm 

from bs4 import BeautifulSoup  # for processing html structure of website

import selenium  # Python Selenium
from selenium import webdriver  # for specifying webdriver
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.support import expected_conditions as EC  # for checking visibility of an element
from selenium.webdriver.support.ui import WebDriverWait  # this three enable waiting until sth is displayed on website
from selenium.webdriver.common.by import By  # for checking element visibility by XPath
from webdriver_manager.chrome import ChromeDriverManager  # chromedriver for automatized access to Chrome
from selenium.common.exceptions import NoSuchElementException, TimeoutException

class CarLeasingScraper:
    def __init__(self, stan, period, oplata_na_start, mileage_limit):
        self.stan = stan
        self.period = period
        self.oplata_na_start = oplata_na_start
        self.mileage_limit = mileage_limit
        self.website_url = f"https://automarket.pl/samochody/{self.stan}/leasing?is_company=0&period={self.period}&ow_proc={self.oplata_na_start}&mileage_limit={self.mileage_limit}&"
        self.driver_chrome = self.setup_driver()

    def setup_driver(self):
        if not hasattr(ChromeDriverManager, 'installed'):
            chromepath = ChromeDriverManager().install()
            print(chromepath)

        service_chrome = Service(executable_path=chromepath) 
        options_chrome = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=service_chrome, options=options_chrome)  # opens Chrome
        driver.maximize_window()  # maximizes browser's window
        driver.get(self.website_url)  # opens a website
        return driver

    def accept_privacy_policy(self):
        xpath_polityka_prywtnosci_button = '''//*[@id="onetrust-accept-btn-handler"]'''
        WebDriverWait(self.driver_chrome, 120).until(EC.visibility_of_element_located((By.XPATH, xpath_polityka_prywtnosci_button))) 
        polityka_prywtnosci_button = self.driver_chrome.find_element("xpath", xpath_polityka_prywtnosci_button)  # finds the button
        polityka_prywtnosci_button.click()  # clicks the button

    def collect_links(self):
        self.accept_privacy_policy()
        # Select '90' for 'Ofert na Stronie'
        xpath_oferty_na_stronie_90_button = '''//*[@id="__nuxt"]/div/main/div/div/div/div/div[2]/div[2]/div[4]/div[1]/div/div[3]'''
        WebDriverWait(self.driver_chrome, 30).until(EC.visibility_of_element_located((By.XPATH, xpath_oferty_na_stronie_90_button))) 
        oferty_na_stronie_90_button = self.driver_chrome.find_element("xpath", xpath_oferty_na_stronie_90_button)  # finds the button
        oferty_na_stronie_90_button.click()  # clicks the button

        # add some time to load the page 
        time.sleep(30)

        # Finding the number of maximum Pages Button
        xpath_page_number_button = '//*[@id="__nuxt"]/div/main/div/div/div/div/div[2]/div[2]/div[4]/div[2]/nav'
        WebDriverWait(self.driver_chrome, 30).until(EC.visibility_of_element_located((By.XPATH, xpath_page_number_button)))
        pagination_nav = self.driver_chrome.find_element(By.XPATH, xpath_page_number_button)

        page_buttons = pagination_nav.find_elements(By.XPATH, ".//a[@aria-current='page']")
        max_page = 1  # Initialize max_page

        # We use try/except because some buttons are not numbers - ValueError: invalid literal for int() with base 10: ''
        for button in page_buttons:
            try:
                page_numbers = int(button.text)
                if page_numbers > 1:
                    max_page = page_numbers
            except ValueError:
                continue

        # Saving links by iterating through all pages
        page_links = {}
        for i in range(1, max_page + 1):
            # Extract links from the current page
            xpath_link = '''//*[@id="__nuxt"]/div/main/div/div/div/div/div[2]/div[2]'''
            WebDriverWait(self.driver_chrome, 30).until(EC.visibility_of_element_located((By.XPATH, xpath_link)))

            # Div containing the car listings
            car_listing_div = self.driver_chrome.find_element(By.XPATH, xpath_link)
            # All <a> tags inside the div container with href containing "/oferta/"
            car_links = car_listing_div.find_elements(By.XPATH, './/a[contains(@href, "/oferta/")]')

            page_i_links = [link.get_attribute('href') for link in car_links]
            page_links[i] = page_i_links

            print(f"Page Number '{i}' - DONE")
            
            if i < max_page:  # Only click the next button if we are not at the last page
                next_button_xpath = "//a[contains(@name, 'Następna strona')]"
                WebDriverWait(self.driver_chrome, 30).until(EC.element_to_be_clickable((By.XPATH, next_button_xpath)))
                next_button = self.driver_chrome.find_element(By.XPATH, next_button_xpath)
                next_button.click()

                # Wait for page to load
                time.sleep(10)

        df_page_links = pd.DataFrame([(page_number, link) for page_number, links in page_links.items() for link in links], columns=['Page Number', 'Links'])
        df_page_links.to_pickle(f'Outputs/{self.stan}/df_page_links.pkl')

    def access_links_and_collect_data(self):
        df_page_links = pd.read_pickle(f'Outputs/{self.stan}/df_page_links.pkl')
        
        data = []
        for i, link in enumerate(df_page_links['Links']):
            webpage_html = requests.get(link)  # request for a webpage structure
            soup = BeautifulSoup(webpage_html.text, 'html.parser')  # one need to format it into a BeautifulSoup object before proceeding
            
            # Numer Oferty, Price, Lokalizacja
            numer_oferty = soup.find('p', class_='text-base text-pko-secondary mt-5 text-center mb-8 md:ml-5 md:my-0 leading-4').text.split(': ')[1]
            
            try:
                price = soup.find('p', class_='text-2xl lg:text-[32px] leading-8 font-semibold text-pko-primary') or soup.find('p', class_='text-2xl lg:text-[32px] leading-8 font-semibold !text-pko-red-500 text-pko-primary')
                if price:
                    price = price.text.replace('\xa0', ' ')
                else:
                    price = None  # Handle the case where neither class is found
            except Exception as e:
                price = None  # Handle any exceptions that occur
            
            lokalizacja_samochodu = soup.find('p', class_='text-sm leading-sm py-3 md:py-0 text-pko-grey-1000 leading-[14px]').find('span').text.strip()

            # Car Model
            whole_model = soup.find('h1')
            car_model = whole_model.find_all('span')[0].text.strip()
            car_model_type = whole_model.find_all('span')[1].text.strip()

            # Informajce Podstawowe
            informacje_podstawowe = soup.find('h2').find_next().find_all('span')
            rok_produkcji = informacje_podstawowe[1].text
            przebieg = informacje_podstawowe[3].text
            naped = informacje_podstawowe[5].text
            skrzynia_biegow = informacje_podstawowe[7].text

            # More Informajce Podstawowe
            attributes = ["Pojemność silnika", "Moc silnika", "Kolor", "Typ nadwozia", "Liczba miejsc", "Kraj pochodzenia"]
            pojazd_info = {attr: soup.find(string=lambda text: text and attr in text).find_next().text for attr in attributes}

            pojemnosc_silnika = pojazd_info["Pojemność silnika"]
            moc_silnika = pojazd_info["Moc silnika"]
            kolor = pojazd_info["Kolor"]
            typ_nadwozia = pojazd_info["Typ nadwozia"]
            liczba_miejsc = pojazd_info["Liczba miejsc"]
            kraj_pochodzenia = pojazd_info["Kraj pochodzenia"]

            # Wymiary
            dimensions = ["Długość", "Szerokość", "Wysokość", "Rozstaw osi", "Masa całkowita"]
            dimension_values = {dim: soup.find(string=lambda text: text and dim in text).find_next().text for dim in dimensions}

            dlugosc = dimension_values["Długość"]
            szerokosc = dimension_values["Szerokość"]
            wysokosc = dimension_values["Wysokość"]
            rozstaw_osi = dimension_values["Rozstaw osi"]
            masa_calkowita = dimension_values["Masa całkowita"]

            # Append the collected data to the list
            data.append({
                'Numer Oferty': numer_oferty,
                'Price': price,
                'Lokalizacja': lokalizacja_samochodu,
                'Car Model': car_model,
                'Car Model Type': car_model_type,
                'Rok Produkcji': rok_produkcji,
                'Przebieg': przebieg,
                'Naped': naped,
                'Skrzynia Biegow': skrzynia_biegow,
                'Pojemnosc Silnika': pojemnosc_silnika,
                'Moc Silnika': moc_silnika,
                'Kolor': kolor,
                'Typ Nadwozia': typ_nadwozia,
                'Liczba Miejsc': liczba_miejsc,
                'Kraj Pochodzenia': kraj_pochodzenia,
                'Dlugosc': dlugosc,
                'Szerokosc': szerokosc,
                'Wysokosc': wysokosc,
                'Rozstaw Osi': rozstaw_osi,
                'Masa Calkowita': masa_calkowita
            })

            print(f"link_{i} DONE")

        # Create a DataFrame from the collected data
        df_car_scrapped_data = pd.DataFrame(data)
        df_car_scrapped_data.to_pickle(f'Outputs/{self.stan}/df_car_scrapped_data.pkl')