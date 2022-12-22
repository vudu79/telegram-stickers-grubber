import datetime
import json
import logging
from datetime import time
import time
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def combot_stickers_grubber():
    begin = time.time()
    logger_combot = logging.getLogger("combot-logger")
    logger_combot.setLevel(logging.INFO)
    handler2 = logging.FileHandler('logs/combot.log', mode='w')
    formatter2 = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
    handler2.setFormatter(formatter2)
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
                        print(pack_div.get("data-src"))
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
            f'Закончил с combot.org сайтом. Заняло времени - {final_time}. Всего страниц обработано - {page_count}')
    except Exception as ee:
        logger_combot.error(f"Проблеммы с записью в файл - {ee}")
    return results

#
# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO, filename="stickers_log_combot.log", filemode="w",
#                         format="%(asctime)s %(levelname)s %(message)s")
#     main()
