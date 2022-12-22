import json
import logging
import time

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from db.db import db_insert_stikers


def tlgrm_stickers_grubber():
    begin = time.time()
    logger_tlgrm = logging.getLogger("tlgrm-logger")
    logger_tlgrm.setLevel(logging.INFO)

    # настройка обработчика и форматировщика для logger_tlgrm
    handler3 = logging.FileHandler(f"logs/tlgrm.log", mode='w')
    formatter3 = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

    # добавление форматировщика к обработчику
    handler3.setFormatter(formatter3)
    # добавление обработчика к логгеру
    logger_tlgrm.addHandler(handler3)
    domen = "https://tlgrm.ru"

    pack_info_dict = dict()
    results = list()
    stickers_list = list()
    ua = UserAgent()

    headers = {
        "user-agent": ua.chrome
    }

    print(headers["user-agent"])
    page_count = 0
    for x in range(0, 475):

        uri = f"/stickers?page={x}"
        try:
            res = requests.get(domen + uri, headers=headers)
            if res.status_code == 200:
                logger_tlgrm.info(f'Рабатаю со страницей - {x}')
                soup = BeautifulSoup(res.text, "lxml")
                divs = soup.find("div", class_="sticker-list").find_all("a", class_="stickerbox")

                for div in divs:
                    pack_name_pre = (div.find("p", class_="stickerbox__caption").text).strip()
                    pack_name = pack_name_pre.split("\n")[0] if ("\n" in pack_name_pre) else pack_name_pre
                    pack_info_dict["name"] = pack_name
                    pack_url = div.get("href")
                    pack_info_dict["date"] = None
                    try:
                        pack_res = requests.get(pack_url, headers=headers)
                        if pack_res.status_code == 200:

                            pack_soup = BeautifulSoup(pack_res.text, "lxml")
                            pack_divs = pack_soup.find("div", class_="sticker-pack-preview").find_all("a",
                                                                                                      class_="sticker-pack-preview__item")

                            for pack_div in pack_divs:
                                stickers_list.append(domen + pack_div.get("href"))

                            pack_info_dict["count"] = str(len(pack_divs))
                            pack_info_dict["url"] = pack_soup.find("a", class_="stickerpack-install__btn").get("href")

                            buffer_list = stickers_list.copy()
                            pack_info_dict["stickers"] = buffer_list

                            db_insert_stikers(pack_info_dict["name"],
                                              pack_info_dict["url"],
                                              pack_info_dict["count"],
                                              buffer_list)


                            stickers_list.clear()

                            buffer_dict = pack_info_dict.copy()
                            print(buffer_dict)
                            results.append(buffer_dict)

                            logger_tlgrm.info(f'{len(results)} паков в файле, текущий {buffer_dict}')
                            logger_tlgrm.info("--------‐--------------------------------------------------")

                            pack_info_dict.clear()
                            page_count = page_count + 1
                    except Exception as eee:
                        logger_tlgrm.error(f"Проблеммы с requests внутри пака -  {eee}")
        except Exception as e:
            logger_tlgrm.error(f"Проблеммы с requests на странице с паками - {e}")
    try:
        with open("files/stickers_tlgrm.files", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4, ensure_ascii=False)
        final_time = time.time() - begin
        logger_tlgrm.info(
            f'Закончил с chpic сайтом. Заняло времени - {final_time}. Всего страниц обработано - {page_count}')
    except Exception as ee:
        logger_tlgrm.error(f"Проблеммы с записью в файл - {ee}")
    return results
