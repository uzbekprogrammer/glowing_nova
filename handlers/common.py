import os
from aiogram import Router, types, F
from aiogram.filters import Command
from dotenv import load_dotenv

load_dotenv()

router = Router()

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    admin_id = os.getenv("ADMIN_ID")
    is_admin = False
    if admin_id and str(message.from_user.id) == str(admin_id):
        is_admin = True

    help_text = (
        "<b>🤖 Botdan foydalanish bo'yicha qo'llanma</b>\n\n"
        "<b>📌Qanday foydalaniladi?</b>\n"
        "1. <b>/start</b> buyrug'ini bosing.\n"
        "2. Ro‘yxatdan <b>Viloyatni</b> tanlang.\n"
        "3. Tegishli <b>Tumanni</b> tanlang.\n"
        "4. So‘ralgan <b>fayl yoki rasmni</b> yuboring.\n\n"
    )

    if is_admin:
        help_text += (
            "<b>👨‍💻 Admin buyruqlari:</b>\n"
            "• <b>!stat</b> - Foydalanuvchilar statistikasini ko'rish.\n"
            "• <b>!rek</b> - (Reply orqali) Xabarni barcha foydalanuvchilarga tarqatish.\n"
        )
    
    await message.answer(help_text, parse_mode="HTML")
