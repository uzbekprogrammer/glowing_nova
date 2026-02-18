import os
import logging
import asyncio
from aiogram import Router, types, Bot, F
from aiogram.filters import Command
from sqlalchemy import select, func
from database.core import get_session
from database.models import User
from dotenv import load_dotenv

load_dotenv()

router = Router()

ADMIN_ID = os.getenv("ADMIN_ID")

def is_admin(user_id: int) -> bool:
    if not ADMIN_ID:
        return False
    return str(user_id) == str(ADMIN_ID)

@router.message(Command("stat"))
async def cmd_stat(message: types.Message):
    if not is_admin(message.from_user.id):
        return

    async for session in get_session():
        result = await session.execute(select(func.count(User.id)))
        count = result.scalar()
        await message.answer(f"📊 Jami foydalanuvchilar: {count}")
        break

@router.message(Command("rek"))
async def cmd_broadcast(message: types.Message, bot: Bot):
    if not is_admin(message.from_user.id):
        return

    if not message.reply_to_message:
        await message.answer("⚠️ Bu buyruqni biror xabarga javob (reply) tarzida yuboring.")
        return

    users_to_send = []
    async for session in get_session():
        result = await session.execute(select(User.telegram_id))
        users_to_send = result.scalars().all()
        break

    sent_count = 0
    failed_count = 0
    
    status_msg = await message.answer("🚀 Xabar yuborish boshlandi...")

    for user_id in users_to_send:
        try:
            await bot.copy_message(
                chat_id=user_id,
                from_chat_id=message.chat.id,
                message_id=message.reply_to_message.message_id
            )
            sent_count += 1
        except Exception as e:
            # logging.error(f"Failed to send to {user_id}: {e}")
            failed_count += 1
        
        # Avoid flood limits
        await asyncio.sleep(0.05)

    await status_msg.edit_text(
        f"✅ Xabar yuborish yakunlandi.\n\n"
        f"📤 Yuborildi: {sent_count}\n"
        f"❌ Yuborilmadi (bloklagan): {failed_count}"
    )
