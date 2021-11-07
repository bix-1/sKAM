#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os
from datetime import datetime
import difflib
import numpy as np
import warnings
import argparse
from random import randint
from selenium.common.exceptions import NoSuchElementException

warnings.filterwarnings("ignore", category=DeprecationWarning)


class sKAM:
    a04 = ["a04-" + str(floor*100 + room) for floor in range(1,10) for room in range(1,41)]
    a05 = ["a05-" + str(floor*100 + room) for floor in range(2,10) for room in range(1,41)]
    a05 += ["a05-" + str(x) for x in list(range(109,115)) + list(range(127, 135))]
    targets = a04 + a05

    def __init__(self, username, password, rnd, drv="./chromedriver", url="https://www.kn.vutbr.cz/is2/", folder="data"):
        self.username = username
        self.password = password
        self.rnd = rnd
        self.folder = folder
        self.driver = webdriver.Chrome(drv)
        self.driver.get(url)


    def __del__(self):
        self.driver.close()


    def login(self):
        self.driver.find_element(By.NAME, "AUTH_LOGIN").send_keys(self.username)
        self.driver.find_element(By.NAME, "AUTH_PW").send_keys(self.password)
        self.driver.find_element(By.NAME, "odeslat").click()
        self.driver.get("https://www.kn.vutbr.cz/is2/index_ssl.html?volba=hledam_lidi")


    def find_room(self, room):
        self.driver.find_element(By.NAME, "str").clear()
        self.driver.find_element(By.NAME, "str").send_keys(room)
        self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(4) input").click()

        try:
            table = self.driver.find_element(By.XPATH, "/html/body/div/table[1]/tbody/tr[1]/td/table[3]/tbody/tr[2]/td/form[2]/table[2]")
            rows = table.find_elements(By.TAG_NAME, "tr")
            status = len(rows) // 5
        except NoSuchElementException:
            status = 0
        return room + ": " + str(status) + "\n"

    def fetch_targets(self):
        data = ""
        for t in self.targets:
            data += self.find_room(t)
            if self.rnd:
                time.sleep(randint(5,25) * 0.1)
            else:
                time.sleep(0.5)
        self.save_data(data)


    def save_data(self, data):
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)

        time = datetime.now()
        filename = self.folder + "/" + time.strftime("%Y-%m-%d_%H.%M.%S")
        with open(filename, "w") as file:
            file.write(data)

    def get_updates(self):
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)

        files = os.listdir(self.folder)
        if len(files) < 2:
            print("No updates to report\n")
            return

        files.sort()
        with open(self.folder + "/" + files[-1]) as new_file:
            new = np.array([x[:-1].split(" ") for x in new_file.readlines()]).T
        with open(self.folder + "/" + files[-2]) as old_file:
            old = np.array([x[:-1].split(" ") for x in old_file.readlines()]).T
        result = [i for i in range(len(new[1,:])) if old[1,i] != new[1,i]]

        if len(result) == 0:
            print("No updates to report\n")
        else:
            print("Found", len(result), "new changes!\n")
            for r in result:
                print(old[0,r] + "    " + old[1,r], ">>", new[1,r])
                if (new[1,r] == "0"):
                    print("\t\t\t[[[[[[[[[[[[[[BINGO]]]]]]]]]]]]]]")


def get_args():
    # specify default credentials here
    aparser = argparse.ArgumentParser(description="Interprets XML representation of IPPcode21 & generates outputs.")
    aparser.add_argument(
        "-u",
        "--username",
        default = "",
        required = False,
        help="specify username")
    aparser.add_argument(
        "-p",
        "--password",
        default = "",
        required = False,
        help="specify password")
    aparser.add_argument(
        "-r",
        "--random",
        default = False,
        required = False,
        help="toggle random delay between requests")

    args = aparser.parse_args()
    return args.username, args.password, args.random


if __name__ == "__main__":
    # get credentials -- in case of use outside of KolejNet
    username, password, rnd = get_args()
    ss = sKAM(username, password, rnd)

    try:
        ss.login()
    except NoSuchElementException:
        pass    # no login needed

    ss.fetch_targets()
    ss.get_updates()
