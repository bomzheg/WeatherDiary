import os
from pathlib import Path

from dotenv import load_dotenv

from weather.utils import CliTexts

app_dir = Path(__file__).parent
load_dotenv(str(app_dir / '.env'))

errLog = "err.log"
printLog = "print.log"

cli_texts = CliTexts(
    program_name="WeatherDiary",
    program_desc="This program is a Python 3+ script. ",
    program_ep="© bomzheg. License MIT.",
    desc_fill="Convert csv to DB. Take all *.csv files from csv directory.",
    desc_drop="Drop table weather",
    desc_create="Create table weather",
    desc_nogui="Do not start windows",
)

file_db = os.getenv("FILE_DB", default=r"c:\Users\Public\Python\WeatherDiary.db")
