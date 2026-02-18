from aiogram.filters.callback_data import CallbackData

class RegionCallback(CallbackData, prefix="reg"):
    name: str

class DistrictCallback(CallbackData, prefix="dist"):
    name: str
