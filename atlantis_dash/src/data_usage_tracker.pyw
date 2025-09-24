import selenium as se
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
from pprint import pprint
from time import sleep

import plotly.graph_objects as go
import cv2

URL = "https://128.128.252.4:4443"
USERNAME = "sci7"
PASSWORD = "whatWorldsEnd"


class DataUsageWatcher:
    def __init__(self) -> None:
        options = Options()
        options.add_argument("--headless")
        self.driver = se.webdriver.Firefox(options=options)
        self.driver.get(URL)
        self.actions = ActionChains(self.driver)

        self.login()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        self.driver.quit()

    def login(self):
        unameInput = self.driver.find_element(By.ID, "username")
        passInput = self.driver.find_element(By.ID, "password")

        self.actions.click(unameInput).send_keys_to_element(
            unameInput, USERNAME
        ).perform()
        self.actions.click(passInput).send_keys_to_element(
            passInput, PASSWORD
        ).send_keys(Keys.ENTER).perform()
        sleep(2)

    def fetch_usage(self):
        self.driver.refresh()
        sleep(0.5)
        tablePath = "//div[@id='content']/div[@id='content3']/div[2]/table/tbody/tr/td/table/tbody/"
        usageDict = {}

        usageDict["totalRemaining"] = self.driver.find_element(
            By.XPATH, tablePath + "tr[5]/td[6]"
        ).text[:-3]
        usageDict["currentSessionUsed"] = self.driver.find_element(
            By.XPATH, tablePath + "tr[5]/td[4]"
        ).text[:-3]
        usageDict["uploadTotal"] = self.driver.find_element(
            By.XPATH, tablePath + "tr[3]/td[5]"
        ).text[:-3]
        usageDict["uploadCurrent"] = self.driver.find_element(
            By.XPATH, tablePath + "tr[3]/td[4]"
        ).text[:-3]
        usageDict["downloadTotal"] = self.driver.find_element(
            By.XPATH, tablePath + "tr[4]/td[5]"
        ).text[:-3]
        usageDict["downloadCurrent"] = self.driver.find_element(
            By.XPATH, tablePath + "tr[4]/td[4]"
        ).text[:-3]

        return usageDict


class DataUsagePlotter:
    def __init__(self, driver) -> None:
        self.driver = driver

    def make_ring_chart(self):
        usageDict = self.driver.fetch_usage()
        pprint(usageDict)
        basicUsageLabels = ["Used", "Current session", "Remaining"]
        basicUsageValues = [
            int(
                5000
                - int(float(usageDict["totalRemaining"]))
                - int(float(usageDict["currentSessionUsed"]))
            ),
            int(float(usageDict["currentSessionUsed"])),
            int(float(usageDict["totalRemaining"])),
        ]
        basicUsageText = []
        for v in basicUsageValues:
            basicUsageText.append(str(v) + " MB")

        basicUsageFig = go.Figure(
            data=[
                go.Pie(
                    labels=basicUsageLabels,
                    values=basicUsageValues,
                    hole=0.6,
                    textinfo="none",
                    # textinfo="text",
                    # texttemplate="%{value} MB",
                    # textfont=dict(family="Tahoma", weight="bold"),
                    # insidetextorientation="horizontal",
                    direction="clockwise",
                    sort=False,
                    showlegend=False,
                )
            ]
        )
        basicUsageFig.update_traces(
            marker=dict(colors=["Crimson", "DarkOrange", "ForestGreen"])
        )
        basicUsageFig.update_layout(paper_bgcolor="#87cefa")
        # basicUsageFig.show()
        img = basicUsageFig.write_image(
            file="basic_usage_chart.png", width=600, height=600
        )
        # print(f"current sesh: {basicUsageValues[1]}")


# with DataUsageWatcher() as dataWatch:
#     pprint(dataWatch.fetch_usage())
