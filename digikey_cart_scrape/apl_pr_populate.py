import selenium as se
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
from pprint import pprint
import argparse
import time
from digikey_component import DigikeyComponent
import json


class PRFiller:
    def __init__(self, url) -> None:
        options = Options()
        # options.add_argument("--headless")
        self.driver = se.webdriver.Firefox(options=options)
        self.driver.get(url)
        self.actions = ActionChains(self.driver)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        self.driver.quit()

    def addRows(self, numRows):
        buttons = self.driver.find_elements(By.XPATH, "//button")
        for b in buttons:
            if b.text == "Update":
                updateButton = b
                break
        additionalRows = self.driver.find_element(By.ID, "additionalItemRows")
        additionalRows.send_keys(str(numRows))
        self.actions.click(updateButton).perform()

    def fillRows(self, componentList):
        table = self.driver.find_element(
            By.XPATH, "//table[@class='ContentTable itemsViewTable']"
        )
        for c in componentList:
            self.inputRow(table.find_element(By.XPATH, f"tbody/tr[{c.lineNumber}]"), c)

    def inputRow(self, tr, component):
        qtyField = tr.find_element(By.NAME, "PR_Item_Quantity")
        unitPriceField = tr.find_element(By.NAME, "PR_Item_UnitPrice")
        partNumberField = tr.find_element(By.NAME, "PR_Item_PartNbr")
        descriptionField = tr.find_element(By.NAME, "PR_Item_Description")
        linkField = tr.find_element(By.NAME, "PR_Item_Link")

        qtyField.send_keys(Keys.BACK_SPACE, str(component.quantity))
        unitPriceField.send_keys(
            Keys.BACK_SPACE,
            Keys.BACK_SPACE,
            Keys.BACK_SPACE,
            Keys.BACK_SPACE,
            str(component.unitPrice),
        )
        partNumberField.send_keys(str(component.partNumber))
        descriptionField.send_keys(str(component.description))
        linkField.send_keys(str(component.link))

    def fillTable(self, componentList):
        self.addRows(len(componentList) - 1)
        self.fillRows(componentList)


def argparse_setup():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--infile", "-i", help="componnet list input filename (json format)"
    )

    return parser.parse_args()


def rebuild_component_list(file):
    componentList = []

    with open(file, mode="r", encoding="utf-8") as f:
        componentListJSON = json.load(f)

    for c in componentListJSON:
        componentList.append(DigikeyComponent.from_dict(c))

    return componentList


def main():

    args = argparse_setup()

    componentList = rebuild_component_list(args.infile)

    URL = "https://apl-app1.s.uw.edu/WD_PurchaseRequest/"

    with PRFiller(URL) as pr:
        input(
            "Login and open request to 'Item Description' page. Press enter when ready to fill item details."
        )
        pr.fillTable(componentList)
        input("Save and then press enter in the terminal when done.")


if __name__ == "__main__":
    main()
