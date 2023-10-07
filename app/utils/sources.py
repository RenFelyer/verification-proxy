from app.config import *
from aiofiles import open
from aiohttp import ClientSession
from asyncio import create_task
from tqdm.asyncio import tqdm
from re import findall


async def extract_address() -> tuple[list[str], str]:
    async with open(FILE_SOURCES, encoding="UTF-8") as file:
        async with ClientSession() as session:
            tasks = [extract_for_link(session, link) async for link in file]
            tasks = [create_task(task) for task in tasks]
            tasks = await tqdm.gather(*tasks)
            tasks = [data for task in tasks for data in task]
            addr = await load_address()
            tasks = list(set([*tasks, *addr]))
            await save_address(tasks)
            return tasks, f"({len(addr)}/{len(tasks)})"


async def load_address() -> list[str]:
    try:
        async with open(FILE_ADDRESS, "r", encoding="UTF-8") as file:
            return [addr async for addr in file]
    except:
        return []


async def save_address(address: list[str]):
    async with open(FILE_ADDRESS, "w", encoding="UTF-8") as file:
        [
            await file.write(f"{addr.strip()}\n")
            for addr in address
            if len(addr.strip()) > 0
        ]


async def extract_for_link(session: ClientSession, link: str) -> list[str]:
    async with session.get(link) as response:
        return [addr for addr in findall(PATTERN_IP_AND_PORT, await response.text())]
