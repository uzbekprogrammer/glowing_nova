from aiogram.fsm.state import State, StatesGroup

class SubmissionStates(StatesGroup):
    waiting_for_region = State()
    waiting_for_district = State()
    waiting_for_file = State()
