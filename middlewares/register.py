from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from sqlalchemy.future import select
from database.core import get_session
from database.models import User

class RegisterMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        # Only work with Messages
        if not isinstance(event, Message):
            return await handler(event, data)

        user = event.from_user
        if not user:
             return await handler(event, data)

        async for session in get_session():
            result = await session.execute(select(User).where(User.telegram_id == user.id))
            db_user = result.scalar_one_or_none()

            if not db_user:
                new_user = User(
                    telegram_id=user.id,
                    full_name=user.full_name,
                    username=user.username
                )
                session.add(new_user)
                await session.commit()
            
            # Break after one session usage as get_session is a generator
            break

        return await handler(event, data)
