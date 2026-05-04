import asyncio
import logging
from logging.handlers import TimedRotatingFileHandler
import nest_asyncio
from centralSystem import CentralSystem
from utils import convertdate
import config
import os
from dotenv import load_dotenv

load_dotenv()

PATH_LOG = os.getenv('PATH_LOG')


async def main():
    logging.basicConfig(
        format="%(asctime)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename=PATH_LOG,
        level=logging.INFO
    )

    logging.Formatter.converter = convertdate.localTimeZone

    csms = CentralSystem()

    await config.create_websocket_server(csms)
    await config.create_http_server(csms)

    print("HTTP rodando na porta 8090")
    print("WebSocket rodando na porta 9000")

    await asyncio.Future()  # 🔥 mantém rodando pra sempre

if __name__ == '__main__':
    nest_asyncio.apply()
    asyncio.run(main())