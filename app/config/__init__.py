from .environment import (
    URL_FOR_VERIFICATION_PROXY,
    LOGGER_FORMAT,
    FILE_ADDRESS,
    FILE_SOURCES,
    FILE_SOCKS5,
    FILE_SOCKS4,
    FILE_HTTP,
)

PATTERN_IP_AND_PORT = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}:[0-9]{1,5}\b"
PATTERN_PROXY_LINK = r"(\w+:\w+@)?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+)"
