import os
import uuid
import logging
from aiogram import Router, F, types, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from data.locations import REGIONS
from states.submission import SubmissionStates
from database.core import get_session
from database.models import UserSubmission

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    
    builder = InlineKeyboardBuilder()
    for region in REGIONS.keys():
        builder.button(text=region, callback_data=f"region:{region}")
    builder.adjust(2)
    
    await message.answer(
        "Assalomu alaykum! Iltimos, viloyatni tanlang:",
        reply_markup=builder.as_markup()
    )
    await state.set_state(SubmissionStates.waiting_for_region)

@router.callback_query(SubmissionStates.waiting_for_region, F.data.startswith("region:"))
async def process_region_selection(callback: types.CallbackQuery, state: FSMContext):
    region_name = callback.data.split(":")[1]
    
    if region_name not in REGIONS:
        await callback.answer("Noto'g'ri viloyat tanlandi.", show_alert=True)
        return
        
    await state.update_data(region=region_name)
    
    builder = InlineKeyboardBuilder()
    for district in REGIONS[region_name]:
        # Truncate if necessary or ensure it fits, but standard districts should fit
        builder.button(text=district, callback_data=f"district:{district}")
    builder.adjust(2)
    builder.button(text="⬅️ Ortga", callback_data="back_to_regions")
    
    await callback.message.edit_text(
        f"Tanlangan viloyat: <b>{region_name}</b>\nEndi tumanni tanlang:",
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )
    await state.set_state(SubmissionStates.waiting_for_district)

@router.callback_query(SubmissionStates.waiting_for_district, F.data == "back_to_regions")
async def back_to_regions(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(SubmissionStates.waiting_for_region)
    # Re-show regions (logic similar to start but editing)
    builder = InlineKeyboardBuilder()
    for region in REGIONS.keys():
        builder.button(text=region, callback_data=f"region:{region}")
    builder.adjust(2)
    
    await callback.message.edit_text(
        "Iltimos, viloyatni tanlang:",
        reply_markup=builder.as_markup()
    )

@router.callback_query(SubmissionStates.waiting_for_district, F.data.startswith("district:"))
async def process_district_selection(callback: types.CallbackQuery, state: FSMContext):
    district_name = callback.data.split(":")[1]
    data = await state.get_data()
    region_name = data.get("region")
    
    # Validate
    if region_name not in REGIONS or district_name not in REGIONS[region_name]:
        await callback.answer("Noto'g'ri tuman tanlandi.", show_alert=True)
        return

    await state.update_data(district=district_name)
    
    await callback.message.edit_text(
        f"Viloyat: <b>{region_name}</b>\nTuman: <b>{district_name}</b>\n\n"
        "Endi faylni (hujjat yoki rasm) yuboring:",
        parse_mode="HTML"
    )
    await state.set_state(SubmissionStates.waiting_for_file)

@router.message(SubmissionStates.waiting_for_file, F.document | F.photo)
async def process_file_upload(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    region = data.get("region")
    district = data.get("district")
    
    if not region or not district:
        await message.answer("Xatolik yuz berdi. Iltimos, /start buyrug'ini bosing.")
        await state.clear()
        return

    # Determine file info
    if message.document:
        file_id = message.document.file_id
        original_name = message.document.file_name or "document"
        file_ext = os.path.splitext(original_name)[1]
        if not file_ext:
            file_ext = ".bin"
    elif message.photo:
        file_id = message.photo[-1].file_id # Get largest
        original_name = "photo.jpg"
        file_ext = ".jpg"
    else:
        await message.answer("Noma'lum fayl turi.")
        return

    # Generate unique filename
    unique_name = f"{uuid.uuid4().hex}{file_ext}"
    
    # Create directory structure
    save_dir = os.path.join("uploads", region, district)
    os.makedirs(save_dir, exist_ok=True)
    
    file_path = os.path.join(save_dir, unique_name)
    
    try:
        # Download file
        file_obj = await bot.get_file(file_id)
        await bot.download_file(file_obj.file_path, file_path)
        
        # Save to DB
        async for session in get_session(): # Using the generator directly
            new_submission = UserSubmission(
                user_id=message.from_user.id,
                region=region,
                district=district,
                file_name=original_name,
                file_path=file_path
            )
            session.add(new_submission)
            await session.commit()
            break # Consume one session and break

        await message.answer(
            f"✅ Fayl qabul qilindi!\n\n"
            f"<b>Viloyat:</b> {region}\n"
            f"<b>Tuman:</b> {district}\n"
            f"<b>Fayl:</b> {original_name}\n\n"
            f"/start orqali yangi yuborishni boshlashingiz mumkin.",
            parse_mode="HTML"
        )
        await state.clear()
        
    except Exception as e:
        logging.error(f"Error saving file: {e}")
        await message.answer("Faylni saqlashda xatolik yuz berdi. Iltimos qaytadan urinib ko'ring.")

@router.message(SubmissionStates.waiting_for_file)
async def process_invalid_file(message: types.Message):
    await message.answer("Iltimos, fayl yuboring (Rasm yoki Hujjat).")
