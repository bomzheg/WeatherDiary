import datetime
import gzip
from typing import io
import typing
from pathlib import Path

import requests
import requests.cookies
from loguru import logger

URL_FOR_GET_COOKIES = "https://rp5.ru/%D0%90%D1%80%D1%85%D0%B8%D0%B2_%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D1%8B_%D0%B2_%D0%96%D1%83%D0%BA%D0%BE%D0%B2%D1%81%D0%BA%D0%BE%D0%BC,_%D0%A0%D0%B0%D0%BC%D0%B5%D0%BD%D1%81%D0%BA%D0%BE%D0%BC_(%D0%B0%D1%8D%D1%80%D0%BE%D0%BF%D0%BE%D1%80%D1%82),_METAR"
URL_TEMPLATE = "https://rp5.ru/responses/reFileMetar.php"
HEADRERS = {
    "Accept": "text/html, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection": "keep-alive",
    "Content-Length": "96",
    "Content-Type": "application/x-www-form-urlencoded",
    "Host": "rp5.ru",
    "Origin": "https://rp5.ru",
    "Referer": "https://rp5.ru/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}
COOKIES_MIX = dict(located='1', tab_metar='2', format='csv', f_enc='utf')
DATE_FORMAT = "%d.%m.%Y"


def load_file(date_from: datetime.date, date_to: datetime.date, csv_file: typing.Union[io.IO[str], io.TextIO]):
    file_url = get_url(
        get_js_script_text(
            post_data=make_post_data(date_from, date_to),
            cookies=prepare_cookies(request_cookies())
        )
    )
    logger.info("Сохраняем файл по ссылке {url}", url=file_url)
    save_file(get_file(file_url), csv_file)


def get_url(js_script_text: str) -> str:
    before_pattern = "'<a href="
    after_pattern = ">Скачать</a>'"
    start = js_script_text.find(before_pattern) + len(before_pattern)
    end = js_script_text.find(after_pattern)
    return js_script_text[start:end]


def get_js_script_text(post_data: dict, cookies: typing.Union[dict, requests.cookies.RequestsCookieJar]):
    r = requests.post(URL_TEMPLATE, data=post_data, cookies=cookies, headers=HEADRERS)
    if r.ok and "Error" not in r.text:
        return r.text
    else:
        raise ConnectionError


def make_post_data(date_from: datetime.date, date_to: datetime.date) -> dict:
    return dict(
        metar=5721,
        a_date1=date_from.strftime(DATE_FORMAT),
        a_date2=date_to.strftime(DATE_FORMAT),
        f_ed3=8,
        f_ed4=8,
        f_ed5=5,
        f_pe=1,
        f_pe1=2,
        lng_id=2,
    )


def request_cookies() -> requests.cookies.RequestsCookieJar:
    r = requests.get(URL_FOR_GET_COOKIES)
    if r.ok and "Error" not in r.text:
        return r.cookies
    raise ConnectionError


def prepare_cookies(cookies: typing.Union[dict, requests.cookies.RequestsCookieJar]) -> dict:
    return dict(**cookies, **COOKIES_MIX)


def get_file(url: str) -> bytes:
    r = requests.get(url)
    if r.ok:
        return r.content
    raise ConnectionError


def save_file(content: bytes, csv_file: typing.Union[io.IO[str], io.TextIO]):
    unzipped = gzip.decompress(content)
    lines = [line + "\n" for line in unzipped.decode("utf-8").splitlines()]
    csv_file.writelines(lines)


if __name__ == "__main__":
    with open(Path("temp.csv"), "w", encoding="utf-8") as file:
        load_file(datetime.date(2020, 3, 15), datetime.date(2020, 7, 12), file)
