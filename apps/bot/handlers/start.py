from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

router = Router()

@router.message(Command('start'))
async def start_command(message: types.Message, state:FSMContext):
    await message.answer(text='Assalomu alaykum, xush kelibsiz') # noqa