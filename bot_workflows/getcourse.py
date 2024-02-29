from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import F, Router
from integrations.amo_crm import new_request as amo_request


class GetCourseForm(StatesGroup):
    name = State()
    franchise_name = State()
    phone_number = State()
    email = State()
    study_type = State()


study_type_map = {
    "franchisee": "Франчайзи",
    "technical_specialist": "Технический специалист",
    "sales_manager": "Менеджер по продажам",
    "hr": "HR"
}

study_type_buttons = [
    [InlineKeyboardButton(text=value, callback_data=key)]
    for key, value in study_type_map.items()
]

getcourse_router = Router(name="getcourse")


@getcourse_router.callback_query(F.data == 'support_getcource')
async def getcourse_button_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text="""Для получения доступа на обучение в GetCource, заполните информацию указанную ниже:):

1. Имя
2. Наименование франшизы 
3. Номер телефона 
4. Электронная почта 
5. Вид обучения : 
- Франчайзи
- технический специалист
- менеджер по продажам 
- HR
""",

    )
    await callback.message.answer("Ваше Имя")
    await state.set_state(GetCourseForm.name)


@getcourse_router.message(GetCourseForm.name)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await message.answer("Введите наименование франшизы")
    await state.set_state(GetCourseForm.franchise_name)


@getcourse_router.message(GetCourseForm.franchise_name)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(franchise_name=message.text)
    await message.answer("Номер телефона")
    await state.set_state(GetCourseForm.phone_number)


@getcourse_router.message(GetCourseForm.phone_number)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(phone=message.text)
    await message.answer("Электронная почта")
    await state.set_state(GetCourseForm.email)


@getcourse_router.message(GetCourseForm.email)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(email=message.text)
    markup = InlineKeyboardMarkup(inline_keyboard=study_type_buttons)
    await message.answer("Вид обучения", reply_markup=markup)
    await state.set_state(GetCourseForm.study_type)


@getcourse_router.message(GetCourseForm.study_type)
async def process_name(message: Message, state: FSMContext) -> None:
    if message.text not in study_type_map.keys():
        await message.delete()
        return
    await state.update_data({
        "study_type_key": message.text,
        "study_type_value": study_type_map[message.text]
    })
    data = await state.get_data()
    data["workflow"] = "getcourse"
    result = amo_request(message.from_user, data)
    await message.answer(result)
    await state.set_state(None)


@getcourse_router.callback_query(GetCourseForm.study_type)
async def process_name(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data({
        "study_type_key": callback.data,
        "study_type_value": study_type_map[callback.data]
    })
    data = await state.get_data()
    data["workflow"] = "getcourse"
    result = amo_request(callback.from_user, data)
    await callback.message.answer(result)
    await state.set_state(None)
