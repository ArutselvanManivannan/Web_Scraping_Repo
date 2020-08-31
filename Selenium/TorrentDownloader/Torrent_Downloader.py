import time
import subprocess
from plyer import notification
from collections import defaultdict

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tkinter import *
from tkinter import ttk, filedialog


class Interface:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title = "Torrent Downloader"

        self.seriesLabel = ttk.Label(self.parent, text="Name").grid(row=0)
        self.seriesEntry = ttk.Entry(self.parent)
        self.seriesEntry.grid(row=0, columnspan=3)

        self.seasonLabel = ttk.Label(self.parent, text="Season").grid(row=1)
        self.seasonEntry = ttk.Entry(self.parent)
        self.seasonEntry.grid(row=1, column=1)

        self.fromEpisodeLabel = ttk.Label(self.parent, text="From Episode").grid(row=2)
        self.fromEpisodeEntry = ttk.Entry(self.parent)
        self.fromEpisodeEntry.grid(row=2, column=1)

        self.toEpisodeLabel = ttk.Label(self.parent, text="To Episode").grid(
            row=2, column=2
        )
        self.toEpisodeEntry = ttk.Entry(self.parent)
        self.toEpisodeEntry.grid(row=2, column=3)

        self.download = ttk.Button(
            self.parent, text="Download", command=self.extract
        ).grid(row=4, columnspan=3)

    def extract(self):
        global series, season, fromEpisode, toEpisode

        series = self.seriesEntry.get()
        season = self.seasonEntry.get()
        fromEpisode = self.fromEpisodeEntry.get()
        toEpisode = self.toEpisodeEntry.get()

        self.parent.quit()


class Torrent:
    PATH = ""  # path to chrome web driver
    VPN = ""  # path to psiphon vpn

    def __init__(self):
        global driver, vpn_handler
        vpn_handler = subprocess.Popen(self.VPN)
        time.sleep(10)
        driver = webdriver.Chrome(self.PATH)
        driver.maximize_window()
        driver.get("https://www.limetorrents.info/")  # Dont change

    def download_queue(self):
        global queue
        queue = defaultdict(list)

        if toEpisode:
            for episode in range(int(fromEpisode), int(toEpisode) + 1):
                search_query = f"{series} S{season.zfill(2)}E{str(episode).zfill(2)}"
                print(search_query)
                title, size, magnet = self.get_torrent(search_query)
                queue["title"].append(title)
                queue["size"].append(size)
                queue["magnet"].append(magnet)

        elif fromEpisode:
            search_query = f"{series} S{season.zfill(2)}E{fromEpisode.zfill(2)}"
            title, size, magnet = self.get_torrent(search_query)
            queue["title"].append(title)
            queue["size"].append(size)
            queue["magnet"].append(magnet)
        else:
            search_query = series
            title, size, magnet = self.get_torrent(search_query)
            queue["title"].append(title)
            queue["size"].append(size)
            queue["magnet"].append(magnet)

        print(search_query)
        notification.notify(
            "Magnet Links", "Found Maget Links....Iniatiating uTorrentWeb!", timeout=10
        )

    def get_torrent(self, search_query):
        try:
            title = size = magnet_download = ""
            search = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            search.clear()
            search.send_keys(search_query)
            search.send_keys(Keys.RETURN)

            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "thnormal"))
            )[4].click()

            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "tt-name"))
            )[3].click()

            title = (
                WebDriverWait(driver, 10)
                .until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
                .text
            )
            if not title.startswith(series):
                raise Exception

            time.sleep(5)

            try:
                size = driver.find_element_by_css_selector(
                    "#content > div:nth-child(7) > div:nth-child(1) > div > table > tbody > tr:nth-child(3) > td:nth-child(2)"
                ).text
            except:
                size = driver.find_element_by_css_selector(
                    "#content > div:nth-child(6) > div:nth-child(1) > div > table > tbody > tr:nth-child(3) > td:nth-child(2)"
                ).text

            try:
                magnet_download = driver.find_element_by_css_selector(
                    "#content > div:nth-child(7) > div:nth-child(1) > div > div:nth-child(13) > div > p > a"
                ).magnet_download.get_attribute("href")
            except:
                magnet_download = driver.find_element_by_css_selector(
                    "#content > div:nth-child(6) > div:nth-child(1) > div > div:nth-child(13) > div > p > a"
                ).get_attribute("href")

            print(title, size, magnet_download)
            return title, size, magnet_download

        except Exception as e:
            print(e)
            driver.quit()


class uTorrentWeb:
    def __init__(self):
        driver.get("")  # localhost address of utorrentWeb
        driver.implicitly_wait(100)

    def send_link(self):
        for i in range(len(queue["magnet"])):
            self.add_torrent(queue["title"][i], queue["magnet"][i], queue["size"][i])

    def add_torrent(self, title, magnet_link, size):
        try:
            add_torrent1 = driver.find_element_by_class_name("add-torrent-btn-text")

            add_torrent1.click()
        except:
            driver.find_element_by_id("auto-upload-btn").click()
        finally:
            link = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "link"))
            )

            link.send_keys(magnet_link)

            add_url = driver.find_element_by_id("add-torrent-url-btn")
            add_url.click()

            notification.notify(title, f"File Size:{size}\nDownload starts", timeout=10)

            while True:
                percentage = int(
                    driver.find_element_by_class_name(
                        "auto-completed-progress-value"
                    ).text[:-1]
                )
                if percentage >= 75:
                    break


if __name__ == "__main__":

    root = Tk()
    interface = Interface(root)
    root.mainloop()

    torrent = Torrent()
    torrent.download_queue()

    time.sleep(5)

    utorrent = uTorrentWeb()
    utorrent.send_link()

    driver.quit()
    vpn_handler.kill()
