from typing import Callable, Any, Union, Awaitable
from asyncio import iscoroutinefunction
import os

MenuName = Union[Callable[[], Any], Callable[[], Awaitable[Any]], str]
MenuItem = Union[Callable[[], Any], Callable[[], Awaitable[Any]], "Menu"]


class Menu:
    _menu: list[tuple[MenuName, MenuItem]] = []
    _name: MenuName = "Меню"
    _back: str = "Назад"

    def __init__(self, name: MenuName = "Меню", back="Назад"):
        self._name = name
        self._back = back
        self._menu = []

    def register(self, name: MenuName, call: MenuItem):
        self._menu.append((name, call))

    async def _get_name(self, call: MenuName) -> str:
        if callable(call) or isinstance(call, Menu):
            return (await call()) if iscoroutinefunction(call) else call()
        return call

    async def _clear_console(self):
        os.system("clear" if os.name == "posix" else "cls")

    async def _show_menu(self, desc: MenuName = None):
        await self._clear_console()
        print(f"===> {await self._get_name(self._name)} <===")
        print("")
        if not desc is None:
            desc = await self._get_name(desc)
            print("")

        if len(names := [await self._get_name(item[0]) for item in self._menu]) > 0:
            [print(f"{i}) {name}") for i, name in enumerate(names, start=1)]
        print(f"0) {self._back}")
        print("")

    async def _ainput(self, prompt="Введите число: ") -> str:
        return input(prompt)

    async def __call__(self, desc: MenuName = None):
        value = 0
        while True:
            await self._show_menu(desc)
            while True:
                value = await self._ainput()
                if value.isdigit():
                    value = int(value)
                    break

            if value == 0:
                break

            if 0 <= (value := value - 1) < len(self._menu):
                _, handler = self._menu[value]
                if callable(handler):
                    check = iscoroutinefunction(handler) or isinstance(handler, Menu)
                    (await handler()) if check else handler()
                    continue
                print("Недопустимый элемент меню.")


class MenuList(Menu):
    _page = 0
    _data: list[str] = []
    _title: MenuName
    _per_pages = 10

    def __init__(self, name: MenuName = "Меню-список"):
        super().__init__(self._get_title)
        self._title, self._data, self._page = name, [], 0
        self.register(self.prev_name, self.prev_call)
        self.register(self.next_name, self.next_call)

    async def __call__(self, data: list[str]):
        self._data = [] if data is None else data
        await super().__call__(self._handler(self._data))

    def _handler(self, data: list[str]) -> MenuItem:
        def handler() -> MenuItem:
            if len(data) > 0:
                start = self._page * self._per_pages
                end = (self._page + 1) * self._per_pages
                for i in range(start, min(end, len(self._data))):
                    print(f"{i} -> {data[i]}")
            else:
                print("Пусто")

        return handler

    async def _get_title(self) -> MenuName:
        title = await self._get_name(self._title)
        return f"{title} ({self._page}/{self.totle_pages()})"

    def totle_pages(self) -> int:
        return int(len(self._data) / self._per_pages)

    def prev_check(self) -> bool:
        return 0 < self._page

    def next_check(self) -> bool:
        return self._page < self.totle_pages()

    def prev_name(self, title="Предыдущая") -> MenuName:
        return title if self.prev_check() else "#" * len(title)

    def next_name(self, title="Следующая") -> MenuName:
        return title if self.next_check() else "#" * len(title)

    def prev_call(self):
        if self.prev_check():
            self._page -= 1

    def next_call(self):
        if self.next_check():
            self._page += 1
