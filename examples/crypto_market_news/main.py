import asyncio

from .manager import CryptoNewsManager


async def main() -> None:
    manager = CryptoNewsManager()
    while True:
        await manager.run()
        await asyncio.sleep(600)


if __name__ == "__main__":
    asyncio.run(main())
