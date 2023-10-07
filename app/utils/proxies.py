from app.utils import *
from app.config import *
from aiohttp import *
from aiofiles import *
from aiosocksy.connector import ProxyConnector, ProxyClientRequest
from time import monotonic
from tqdm.asyncio import tqdm
from asyncio import create_task, gather


async def save_proxies(proxies: list[tuple[str, str, float]]):
    async with open(FILE_HTTP, "w", encoding="UTF-8") as file:
        [
            await file.write(f"{proxy.strip()}\n")
            for (prot, proxy, _) in proxies
            if prot == "http"
        ]
    async with open(FILE_SOCKS4, "w", encoding="UTF-8") as file:
        [
            await file.write(f"{proxy.strip()}\n")
            for (prot, proxy, _) in proxies
            if prot == "socks4"
        ]
    async with open(FILE_SOCKS5, "w", encoding="UTF-8") as file:
        [
            await file.write(f"{proxy.strip()}\n")
            for (prot, proxy, _) in proxies
            if prot == "socks5"
        ]


async def load_proxies() -> list[tuple[str, str, float]]:
    result: list[tuple[str, str, float]] = []
    try:
        async with open(FILE_HTTP) as file:
            async for line in file:
                result.append(("http", line.strip(), 0))
        async with open(FILE_SOCKS4) as file:
            async for line in file:
                result.append(("socks4", line.strip(), 0))
        async with open(FILE_SOCKS5) as file:
            async for line in file:
                result.append(("socks5", line.strip(), 0))
    finally:
        return result


async def varification_proxy() -> list[tuple[str, str, float]]:
    conn = ProxyConnector()
    clazz = ProxyClientRequest
    async with ClientSession(connector=conn, request_class=clazz) as session:
        tasks = [check_proxies(session, proxy) for proxy in await load_address()]
        tasks = [create_task(task) for task in tasks]
        tasks = await tqdm.gather(*tasks)
        tasks = [task for datas in tasks for task in datas]
        return tasks


async def check_proxies(session: ClientSession, proxy: str):
    tasks = await create_tasks_proxy(session, proxy)
    tasks = await gather(*tasks)
    tasks: list[tuple[str, float]] = [(task[1], task[2]) for task in tasks if task[0]]
    result: list[tuple[str, float]] = []
    for protocol in set([proto for (proto, _) in tasks]):
        times = [time for (proto, time) in tasks if proto == protocol]
        result.append((protocol, proxy, sum(times) / len(times)))
    return result


async def create_tasks_proxy(session: ClientSession, proxy: str) -> list:
    tasks = [
        check_protocol(session, protocol, proxy, url)
        for url in URL_FOR_VERIFICATION_PROXY
        for protocol in {"http", "socks4", "socks5"}
    ]
    return [create_task(task) for task in tasks]


async def check_protocol(
    session: ClientSession, protocol: str, proxy: str, link: str
) -> tuple[bool, str, float]:
    link = "http://checkip.amazonaws.com"
    time = monotonic()
    try:
        async with session.get(link, proxy=f"{protocol}://{proxy}") as resp:
            return (resp.status == 200, protocol, monotonic() - time)
    except:
        return (False, protocol, 0)
