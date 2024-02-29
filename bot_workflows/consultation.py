from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram import F, Router
from integrations.amo_crm import new_request as amo_request


class ConsultationForm(StatesGroup):
    name = State()
    franchise_name = State()
    phone_number = State()
    problem_description = State()


consultation_router = Router(name="consultation")


@consultation_router.callback_query(F.data == 'support_consultation')
async def consultation_button_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text="""Для получения консультации, заполните информацию указанную ниже:
1. Имя
2. Наименование франшизы 
3. Номер телефона 
4. Описание проблемы """,

    )
    await callback.message.answer("Ваше Имя")
    await state.set_state(ConsultationForm.name)


@consultation_router.message(ConsultationForm.name)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await message.answer("Введите наименование франшизы")
    await state.set_state(ConsultationForm.franchise_name)


@consultation_router.message(ConsultationForm.franchise_name)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(franchise_name=message.text)
    await message.answer("Номер телефона")
    await state.set_state(ConsultationForm.phone_number)


@consultation_router.message(ConsultationForm.phone_number)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(phone_number=message.text)
    await message.answer("Описание проблемы")
    await state.set_state(ConsultationForm.problem_description)


@consultation_router.message(ConsultationForm.problem_description)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(problem_description=message.text)
    data = await state.get_data()
    data["workflow"] = "consultation"
    result = amo_request(message.from_user, data)
    await message.answer(result)
    await state.set_state(None)
