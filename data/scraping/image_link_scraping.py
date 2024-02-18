from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from time import sleep
import os

# webscraping globals
options = Options()
options.add_argument("--headless")
ser = Service('./chromedriver')
driver = Chrome(service=ser, options=options)
url = "https://mangasee123.com/manga/Solo-Leveling"


def display_all_images(chapter):
    url = "https://mangasee123.com{}".format(chapter['href'])
    driver.get(url)

    # clicking the "long strip" button to display all images
    loop = True
    while(loop):
        try:
            wait = WebDriverWait(driver, 30)
            wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[1]/div/div[4]/button"))).click()
        except:
            print("didn't finish in time, retrying")
            continue
        else:
            loop = False


def scrape_image_links(dest='image_links.txt'):
    driver.get(url)


    # clicking the "Show All Chapters" button
    driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div/div/div[2]/div").click()
    sleep(5)

    # getting html from driver and giving it to soup
    soup = BeautifulSoup(driver.page_source, "lxml")
    chapters = soup.find_all("a", class_="list-group-item ChapterLink ng-scope")
    print(len(chapters))

    # the file to write output to
    file = open(dest, "w")

    for chapter in chapters:

        # displaying all images in the html
        display_all_images(chapter)

        soup = BeautifulSoup(driver.page_source, "lxml")
        image = soup.find_all("img", class_="img-fluid")
        print(len(image))
        for img in image:
            # adding link to image to file
            file.write("{}\n".format(img['src']))
            print(img['src'])
        print()

    file.close()
    print(f"successfully scraped links to images to file {dest}")