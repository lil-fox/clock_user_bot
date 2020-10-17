from telethon.tl.functions.photos import UploadProfilePhotoRequest
from telethon.tl.functions.photos import DeletePhotosRequest
from telethon import TelegramClient
from dotenv import load_dotenv
import asyncio
import config
import os


class UserBot:

    def __init__(self):
        self._client = None

        load_dotenv()

        api_id = os.environ.get("API_ID")
        api_hash = os.environ.get("API_HASH")

        if api_id and api_hash:
            self._client = TelegramClient(config.BOT_ID, api_id, api_hash)

    async def connect(self):
        if self._client:
            await self._client.start()

    def run(self, main):
        if self._client:
            self._client.loop.run_until_complete(main())
        else:
            asyncio.run(main())

    async def upload_clock(self, path_to_clock):
        if self._client:
            clock = self._client.upload_file(path_to_clock)
            await self._client(UploadProfilePhotoRequest(clock))

            await self._delete_prev_clocks()

    async def _delete_prev_clocks(self):
        if self._client:
            prev_clocks = await self._client.get_profile_photos('me')
            prev_clocks = prev_clocks[1:]

            await self._client(DeletePhotosRequest(prev_clocks))
