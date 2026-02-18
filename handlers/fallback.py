from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

router = Router()

@router.message()
async def echo_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state is None:
        await message.reply("Kechirasiz, men sizni tushunmadim. Fayl yuborishni boshlash uchun /start buyrug'ini bosing.")
    else:
        await message.reply("Hozirgi jarayonni yakunlang yoki menyudan foydalaning. Agar adashib qolgan bo'lsangiz, /start bosing.")
