import json
import logging
import datetime
import time
from bs4 import BeautifulSoup
from django.contrib.sites import requests
from fake_useragent import UserAgent
import requests
from db.db import db_insert_stikers


def chpic_stickers_grubber():
    begin = time.time()
    logger_chpic = logging.getLogger("chpic-logger")
    logger_chpic.setLevel(logging.INFO)

    # настройка обработчика и форматировщика для logger_chpic
    handler1 = logging.FileHandler("../logs/chpic.log", mode='w')
    formatter1 = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

    # добавление форматировщика к обработчику
    handler1.setFormatter(formatter1)
    # добавление обработчика к логгеру
    logger_chpic.addHandler(handler1)

    domen = "https://chpic.su"
    pack_info_dict = dict()
    results = list()
    stickers_list = list()
    ua = UserAgent()
    headers = {
        "user-agent": ua.chrome
    }

    print(headers["user-agent"])
    page_count = 0
    for x in range(0, 343):
        uri = f"/ru/stickers/?sortby=date&page={x}"
        print(uri + " " + str(datetime.datetime.now()))
        try:
            res = requests.get(domen + uri, headers=headers)
            if res.status_code == 200:
                logger_chpic.info(f'Рабатаю со страницей - {x}')
                soup = BeautifulSoup(res.text, "lxml")
                divs = soup.find_all("div", class_="collections_list_item clickable_area")

                for div in divs:
                    pack_info_dict["name"] = div.find("div", class_="title").find("a").text
                    pack_url = domen + div.find("div", class_="title").find("a").get("href")
                    pack_info_dict["count"] = (div.find("div", class_="subtitle").text).split(" ")[0]
                    pack_info_dict["date"] = div.find("div", class_="datetime").find("span", class_="t").text
                    try:
                        pack_res = requests.get(pack_url, headers=headers)
                        if pack_res.status_code == 200:

                            pack_soup = BeautifulSoup(pack_res.text, "lxml")
                            pack_divs = pack_soup.find_all("div", class_="stickers_list_item")
                            pack_info_dict["url"] = pack_soup.find("div", class_="collection_info").find("div",
                                                                                                         class_="install").find(
                                "a").get("href")
                            for pack_div in pack_divs:
                                stickers_list.append(domen + pack_div.find("a").find("img").get("src"))

                            buffer_list = stickers_list.copy()
                            pack_info_dict["stickers"] = buffer_list

                            db_insert_stikers(pack_info_dict["name"], pack_info_dict["url"], pack_info_dict["count"],
                                              buffer_list)

                            stickers_list.clear()
                            buffer_dict = pack_info_dict.copy()
                            print(buffer_dict)
                            results.append(buffer_dict)
                            pack_info_dict.clear()
                            logger_chpic.info(f'{len(results)} паков в файле, текущий {buffer_dict}')
                            logger_chpic.info("--------‐--------------------------------------------------")
                            page_count = page_count + 1

                    except Exception as eee:
                        logger_chpic.error(f"Проблеммы с requests внутри пака -  {eee}")

        except Exception as e:
            logger_chpic.error(f"Проблеммы с requests на странице с паками - {e}")

    try:
        with open("files/stickers_chpic.files", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4)
        final_time = time.time() - begin
        logger_chpic.info(
            f'Закончил с chpic сайтом. Заняло времени - {final_time}. Всего страниц обработано - {page_count}')
    except Exception as ee:
        logger_chpic.error(f"Проблеммы с записью в файл - {ee}")
    return results

# if __name__ == "__main__":
#     # logging.basicConfig(level=logging.INFO, filename="stickers_log.log", filemode="w",
#     #                     format="%(asctime)s %(levelname)s %(message)s")
#     chpic_stickers_grubber()
# ---------------------------------------------------------------------------
