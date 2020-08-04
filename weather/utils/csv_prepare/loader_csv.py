import datetime

try:
    import requests
except ImportError:
    raise ImportError("Requests don't install")
URL_TEMPLATE = (
    r"http://{ip}/download/files.metar/UU/UUBW.{date_from}.{date_to}.1.0.0.ru.utf8.00000000.csv.gz"
)
DATE_FORMAT = "%d.%m.%Y"
IP = "93.90.217.250"


def get_url(date_from: datetime.date, date_to: datetime.date):
    """
    http://37.9.3.250/download/files.metar/UU/UUBW.02.08.2020.04.08.2020.1.0.0.ru.utf8.00000000.csv.gz
    http://93.90.217.250/download/files.metar/UU/UUBW.02.08.2020.04.08.2020.1.0.0.ru.utf8.00000000.csv.gz
    http://93.90.217.250/download/files.metar/UU/UUBW.01.08.2020.04.08.2020.1.0.0.ru.utf8.00000000.csv.gz
    http://93.90.217.250/download/files.metar/UU/UUBW.01.08.2020.04.08.2020.1.0.0.ru.utf8.00000000.csv.gz
    """
    return URL_TEMPLATE.format(
        ip=IP,
        date_from=date_from.strftime(DATE_FORMAT),
        date_to=date_to.strftime(DATE_FORMAT)
    )


def get_url2():
    r = requests.get("https://rp5.ru/%D0%90%D1%80%D1%85%D0%B8%D0%B2_%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D1%8B_%D0%B2_%D0%96%D1%83%D0%BA%D0%BE%D0%B2%D1%81%D0%BA%D0%BE%D0%BC,_%D0%A0%D0%B0%D0%BC%D0%B5%D0%BD%D1%81%D0%BA%D0%BE%D0%BC_(%D0%B0%D1%8D%D1%80%D0%BE%D0%BF%D0%BE%D1%80%D1%82),_METAR")


if __name__ == "__main__":
    print(get_url(datetime.date(2020, 3, 15), datetime.date(2020, 7, 12)))
