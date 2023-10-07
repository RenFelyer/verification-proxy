from dotenv import load_dotenv
from os import getenv
from re import sub
from pathlib import Path

load_dotenv()


def get_list_for_verification() -> list[str]:
    temp = getenv("URL_FOR_VERIFICATION_PROXY", "")
    temp = sub(r"[\n\t]+", "", temp)
    return temp.split(",")


LOGGER_FORMAT = getenv("LOGGER_FORMAT", None)
URL_FOR_VERIFICATION_PROXY = [proxy for proxy in get_list_for_verification()]

# https://ipwho.is

PATH_ASSETS = getenv("PATH_ASSETS", "assets")
PATH_PROXIES = str(Path(Path.cwd(), PATH_ASSETS, "proxies"))

FILE_SOURCES = str(Path(Path.cwd(), PATH_ASSETS, "sources.txt"))
FILE_ADDRESS = str(Path(Path.cwd(), PATH_ASSETS, "address.txt"))

FILE_HTTP = str(Path(PATH_PROXIES, "http.txt"))
FILE_SOCKS4 = str(Path(PATH_PROXIES, "socks4.txt"))
FILE_SOCKS5 = str(Path(PATH_PROXIES, "socks5.txt"))
