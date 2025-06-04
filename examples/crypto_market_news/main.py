import asyncio
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

from .manager import CryptoNewsManager


async def main() -> None:
    await CryptoNewsManager().run()


if __name__ == "__main__":
    asyncio.run(main())
