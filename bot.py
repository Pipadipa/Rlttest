import asyncio
import logging
import sys
import json

from aggregation import ResponseMaker
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.methods import send_message

# Bot token can be obtained via https://t.me/BotFather
TOKEN = ""

# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()
rm = ResponseMaker()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        query = json.loads(message.text)
    except json.JSONDecodeError:
        await message.answer("This is not json")
    else:
        response = str(await rm.make_a_slice(query['dt_from'], query['dt_upto'], query['group_type']))
        response = response.replace('\'', '\"') # капец у вас гениальный бот
        await message.answer(text=response)


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
