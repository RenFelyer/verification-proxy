from logging import basicConfig, getLogger, INFO
from app.config import LOGGER_FORMAT
from app.menu import MainMenu
import asyncio


logger = getLogger(__name__)


if __name__ == "__main__":
    try:
        main = MainMenu()
        basicConfig(level=INFO, format=LOGGER_FORMAT)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except (KeyboardInterrupt, StopIteration, SystemExit):
        logger.info("Работа завершена!")
