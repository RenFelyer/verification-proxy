from app.utils import *


class MainMenu(Menu):
    def __init__(self):
        super().__init__(back="Закончить")
        self.register("Извлечь адреса", self.extract)
        self.register("Извлечь прокси", self.verification)
        # self.register("Анализировать прокси")

    async def extract(self):
        _, line = await extract_address()
        await self._ainput(f"(Було\стало) -> {line}")

    async def verification(self):
        proxies = sorted(await varification_proxy(), key=lambda d: d[2])
        for i, (protocol, proxy, delta) in enumerate(proxies):
            print(f"{i+1}) [{protocol}] [{delta:3.3f}] >> {proxy}".strip())
        load = await load_proxies()
        await save_proxies([*proxies, *load])
        await self._ainput(f"всего прошедших прокси ({len(proxies)})")
