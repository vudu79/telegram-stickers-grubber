import datetime
import json
import time


import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup


# сайт "https://chpic.su" ------------------------------------------------
def chpic_stickers_grubber():
    begin = time.time()
    logger_chpic = logging.getLogger("chpic-logger")
    logger_chpic.setLevel(logging.INFO)

    # настройка обработчика и форматировщика для logger_chpic
    handler1 = logging.FileHandler(f"logs/chpic.log", mode='w')
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
#     logging.basicConfig(level=logging.INFO, filename="stickers_log.log", filemode="w",
#                         format="%(asctime)s %(levelname)s %(message)s")
#     main()
# ---------------------------------------------------------------------------

# сайт https://combot.org/telegram/stickers
def combot_stickers_grubber():
    begin = time.time()
    logger_combot = logging.getLogger("combot-logger")
    logger_combot.setLevel(logging.INFO)

    # настройка обработчика и форматировщика для logger_combot
    handler2 = logging.FileHandler('logs/combot.log', mode='w')
    formatter2 = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

    # добавление форматировщика к обработчику
    handler2.setFormatter(formatter2)
    # добавление обработчика к логгеру
    logger_combot.addHandler(handler2)

    domen = "https://combot.org"
    pack_info_dict = dict()
    results = list()
    stickers_list = list()
    ua = UserAgent()

    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept - language": 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        "origin": "https://combot.org",
        "referer": "https://combot.org/",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": ua.msie
    }

    print(headers["user-agent"])
    page_count = 0
    for x in range(0, 79):
        uri = f"/telegram/stickers?page={x}"
        print(uri + " " + str(datetime.datetime.now()))
        try:
            res = requests.get(domen + uri, headers=headers)

            if res.status_code == 200:
                logger_combot.info(f'Рабатаю со страницей - {x}')
                soup = BeautifulSoup(res.text, "lxml")
                divs = soup.find_all("div", class_="sticker-pack sticker-packs-list__item")
                for div in divs:
                    pack_info_dict["name"] = div.find("div", class_="sticker-pack__title").text
                    pack_info_dict["url"] = div.find("a").get("href")
                    pack_info_dict["date"] = None
                    pack_divs = div.find_all("div", class_="sticker-pack__sticker-img")

                    for pack_div in pack_divs:
                        stickers_list.append(pack_div.get("data-src"))

                    pack_info_dict["count"] = str(len(pack_divs))
                    buffer_list = stickers_list.copy()
                    pack_info_dict["stickers"] = buffer_list
                    stickers_list.clear()

                    buffer_dict = pack_info_dict.copy()
                    print(buffer_dict)
                    results.append(buffer_dict)

                    logger_combot.info(f'{len(results)} паков в файле, текущий {buffer_dict}')
                    logger_combot.info("--------‐--------------------------------------------------")
                    pack_info_dict.clear()
                    page_count = page_count + 1

        except Exception as e:
            logger_combot.error(f"Проблеммы с requests на странице с паками - {e}")

    try:
        with open("files/stickers_combot.files", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4, ensure_ascii=False)
        final_time = time.time() - begin
        logger_combot.info(
            f'Закончил с chpic сайтом. Заняло времени - {final_time}. Всего страниц обработано - {page_count}')
    except Exception as ee:
        logger_combot.error(f"Проблеммы с записью в файл - {ee}")
    return results


#
# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO, filename="stickers_log_combot.log", filemode="w",
#                         format="%(asctime)s %(levelname)s %(message)s")
#     main()

# сайт https://tlgrm.ru/stickers ------------------------------------------------------------
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
    # for x in range(1, 475):
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


def main():
    begin = time.time()
    logger_main = logging.getLogger(__name__)
    logger_main.setLevel(logging.INFO)

    # настройка обработчика и форматировщика для logger_main
    handler = logging.FileHandler(f"logs/main.log", mode='w')
    formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

    # добавление форматировщика к обработчику
    handler.setFormatter(formatter)
    # добавление обработчика к логгеру
    logger_main.addHandler(handler)

    try:
        with ThreadPoolExecutor(max_workers=3) as executor:
            future_list = []
            result_list = []

            future1 = executor.submit(tlgrm_stickers_grubber)
            future2 = executor.submit(combot_stickers_grubber)
            future3 = executor.submit(chpic_stickers_grubber)
            future_list.append(future1)
            future_list.append(future2)
            future_list.append(future3)
            logger_main.info("Запустил процессы скрапинга")

            for f in as_completed(future_list):
                worker_done = f.result()
                result_list = result_list + (f.result())
                logger_main.info(f'отработал {worker_done}')


    except Exception as e:
        logger_main.error(f'Ошибка в main с процессами -  {e}')

        try:
            with open("files/stickers_total.files", "w", encoding="utf-8") as f:
                json.dump(result_list, f, indent=4, ensure_ascii=False)
            logger_main.info("записал список в итоговый файл")
            logger_main.info(
                f'Общее время работы скрипта - {time.time() - begin}. В итоговм списке {len(result_list)} записей.')
        except Exception as eeee:
            logger_main.error(f"Проблеммы с записью в файл stickers_total.files - {eeee}")


#
# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO, filename="stickers_log_tlgrm.log", filemode="w",
#                         format="%(asctime)s %(levelname)s %(message)s")
#     main()


# def collect_stickers():
#     with open("files/stickers_chpic.files", "r", encoding="utf-8") as file:
#         chpic_list = files.load(file)
#     with open("files/stickers_combot.files", "r", encoding="utf-8") as file:
#         combot_list = files.load(file)
#     with open("files/stickers_tlgrm.files", "r", encoding="utf-8") as file:
#         tlgrm_list = files.load(file)
#
#     result_list = combot_list + chpic_list + tlgrm_list
#     print(len(result_list))
#     return result_list


if __name__ == "__main__":
    main()
