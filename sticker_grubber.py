import json
import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from grubbers.chpic import chpic_stickers_grubber
from grubbers.combot import combot_stickers_grubber
from grubbers.tlgrm import tlgrm_stickers_grubber


def main():
    begin = time.time()
    logger_main = logging.getLogger(__name__)
    logger_main.setLevel(logging.INFO)
    handler = logging.FileHandler(f"logs/main.log", mode='w')
    formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
    handler.setFormatter(formatter)
    logger_main.addHandler(handler)

    try:
        with ThreadPoolExecutor(max_workers=3) as executor:
            future_list = []
            result_list = []

            future1 = executor.submit(tlgrm_stickers_grubber)
            future3 = executor.submit(chpic_stickers_grubber)
            future_list.append(future1)
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

q
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
