import selenium as se
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
from pprint import pprint
import time
import argparse
from dataclasses import dataclass
import json
import datetime as dt
import re

from digikey_component import DigikeyComponent

DETAILED_DESC_XPATH = "//div[@id='__next']/div[1]/main[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/table[1]/tbody[1]/tr[7]/td[2]/div[1]/div[1]"


class DigikeyScraper:
    def __init__(self, url) -> None:
        options = Options()
        options.add_argument("--headless")
        self.driver = se.webdriver.Firefox(options=options)
        self.driver.get(url)
        self.actions = ActionChains(self.driver)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        self.driver.quit()

    def ensure_load(self):
        print("Loading", end="")
        try:
            while True:
                self.driver.find_element(By.ID, "dkDialogSpinner")
                time.sleep(1)
                print(".", end="")
        except se.common.exceptions.NoSuchElementException:
            print("\n Done loading.")

    def find_cart_rows(self):
        rows = self.driver.find_elements(
            By.XPATH, "//table[@id='cartDetails']/tbody[1]/tr"
        )
        filteredRows = []
        for r in rows:
            if r.get_attribute("class") != "detailRow subRow":
                filteredRows.append(r)
        return filteredRows

    def get_component_details(self, rowElement):
        lineNumber = int(
            rowElement.find_element(
                By.XPATH, "td[@class='detailRow_index']/div[1]"
            ).text
        )
        partNumberElem = rowElement.find_element(
            By.XPATH,
            "td[@class='detailRow_productDetails']/div[@class='cart-partNumber dk-ltr']/a[1]",
        )
        partNumber = partNumberElem.text
        link = partNumberElem.get_attribute("href")
        description = rowElement.find_element(
            By.XPATH,
            "td[@class='detailRow_productDetails']/div[@class='cart-description dk-ltr']",
        ).text
        quantity = int(
            rowElement.find_element(
                By.XPATH,
                "td[@class='detailRow_qtyInput']/div[@class='cart-qtyInput']/input[1]",
            ).get_attribute("value")
        )
        unitPrice = float(
            re.search(
                r"\d*\.\d*",
                rowElement.find_element(
                    By.XPATH,
                    "td[@class='detailRow_unitPrice']/div[@class='cart-unitPrice']",
                ).text,
            ).group()
        )

        return DigikeyComponent(
            lineNumber=lineNumber,
            partNumber=partNumber,
            link=link,
            description=description,
            quantity=quantity,
            unitPrice=unitPrice,
        )


def argparse_setup():
    parser = argparse.ArgumentParser()

    parser.add_argument("--cartlink", "-c", help="url to digikey cart")

    return parser.parse_args()


def main():

    args = argparse_setup()

    with DigikeyScraper(args.cartlink) as scraper:
        rows = scraper.find_cart_rows()
        # pprint([r.get_attribute("class") for r in rows])
        componentList = []
        for r in rows:
            componentList.append(scraper.get_component_details(r))
        pprint(componentList)
        with open(
            f"component_lists/component_list_{dt.datetime.now().strftime("%b-%d-%Y")}.txt",
            mode="w",
            encoding="utf-8",
        ) as f:
            f.write(json.dumps([c.to_dict() for c in componentList]))


if __name__ == "__main__":
    main()
