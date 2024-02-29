from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram import F, Router
from integrations.amo_crm import new_request as amo_request

class SynchronizationForm(StatesGroup):
    name = State()
    franchise_name = State()
    phone_number = State()
    problem_name = State()
    shop_name = State()
    cash_register_version = State()
    cashier_name = State()
    cash_register_password = State()
    link_to_shop = State()
    link_to_archive = State()
    login = State()
    password = State()


synchronization_router = Router(name="synchronization")


@synchronization_router.callback_query(F.data == 'support_synchronization')
async def synchronization_button_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text="""Для обращения касательно синхронизации, заполните информацию указанную ниже:
        
1. Имя
2. Наименование франшизы 
3. Номер телефона 
4. Название проблемы должно быть коротким, понятным и отвечать на вопросы где и в чем проблема. 
5. Название магазина: 
6. Версия кассы: 
7. Имя кассира: 
8. Пароль от кассы: 
9. Ссылка на магазин: 
10. Ссылка на архив: 
11. Логин: 
12. Пароль: 
""",

    )
    await callback.message.answer("Ваше Имя")
    await state.set_state(SynchronizationForm.name)


@synchronization_router.message(SynchronizationForm.name)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await message.answer("Введите наименование франшизы")
    await state.set_state(SynchronizationForm.franchise_name)


@synchronization_router.message(SynchronizationForm.franchise_name)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(franchise_name=message.text)
    await message.answer("Номер телефона")
    await state.set_state(SynchronizationForm.phone_number)


@synchronization_router.message(SynchronizationForm.phone_number)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(phone_number=message.text)
    await message.answer(
        "Название проблемы должно быть коротким, понятным и отвечать на вопросы где и в чем проблема")
    await state.set_state(SynchronizationForm.problem_name)


@synchronization_router.message(SynchronizationForm.problem_name)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(problem_name=message.text)
    await message.answer("Название магазина")
    await state.set_state(SynchronizationForm.shop_name)


@synchronization_router.message(SynchronizationForm.shop_name)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(shop_name=message.text)
    await message.answer("Версия кассы")
    await state.set_state(SynchronizationForm.cash_register_version)


@synchronization_router.message(SynchronizationForm.cash_register_version)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(cash_register_version=message.text)
    await message.answer("Имя кассира")
    await state.set_state(SynchronizationForm.cashier_name)


@synchronization_router.message(SynchronizationForm.cashier_name)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(cashier_name=message.text)
    await message.answer("Пароль от кассы")
    await state.set_state(SynchronizationForm.cash_register_password)


@synchronization_router.message(SynchronizationForm.cash_register_password)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(cash_register_password=message.text)
    await message.answer("Ссылка на магазин")
    await state.set_state(SynchronizationForm.link_to_shop)


@synchronization_router.message(SynchronizationForm.link_to_shop)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(link_to_shop=message.text)
    await message.answer("Ссылка на архив")
    await state.set_state(SynchronizationForm.link_to_archive)


@synchronization_router.message(SynchronizationForm.link_to_archive)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(link_to_archive=message.text)
    await message.answer("Логин")
    await state.set_state(SynchronizationForm.login)


@synchronization_router.message(SynchronizationForm.login)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(login=message.text)
    await message.answer("Пароль")
    await state.set_state(SynchronizationForm.password)


@synchronization_router.message(SynchronizationForm.password)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(password=message.text)
    data = await state.get_data()
    data["workflow"] = "synchronization"
    result = amo_request(message.from_user, data)
    await message.answer(result)
    await state.set_state(None)
