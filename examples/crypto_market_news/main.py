import asyncio

from .manager import CryptoNewsManager


async def main() -> None:
    await CryptoNewsManager().run()


if __name__ == "__main__":
    asyncio.run(main())
