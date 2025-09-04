import asyncio
import logging
from aiogram import F, types
from aiogram import Bot
from aiogram import Dispatcher
from aiogram.fsm.context import FSMContext
from pyexpat.errors import messages
from aiogram.types import Message

from config import TOKEN
import lmstudio as lms


bot = Bot(TOKEN)
dp = Dispatcher()




async def main():
    @dp.message()
    async def echo_photo_message(message: types.Message, state: FSMContext):
        if message.photo:
            file_name = f"photos/{message.photo[-1].file_id}.jpg"
            photo_size = message.photo[-1]  # Получаем самое высокое разрешение фото
            file_id = photo_size.file_id
            await bot.download(file_id, destination=file_name)
            async with lms.AsyncClient() as client:
                model = await client.llm.model()
                image_path = file_name  # Replace with the path to your image
                image_handle = lms.prepare_image(image_path)
                chat = lms.Chat()
                chat.add_user_message(f"{message.caption}", images=[image_handle])
                prediction = await model.respond(chat)
                await message.answer(f"{prediction}")
        else:
            model = lms.llm()
            result = model.respond(f"{message.text}")
            await message.answer(str(result))
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')