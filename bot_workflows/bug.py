from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram import F, Router
from integrations.amo_crm import new_request as amo_request
from integrations.amo_crm import request_bot_answer

class BugForm(StatesGroup):
    name = State()
    franchise_name = State()
    phone_number = State()
    bug_name = State()
    description_and_scenario = State()
    additional_information = State()


bug_router = Router(name="bug")


@bug_router.callback_query(F.data == 'support_bug')
async def bug_button_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text="""Для обращения касательно бага, заполните информацию указанную ниже:

1. Имя
2. Наименование франшизы 
3. Номер телефона 
4. Название бага. Название бага должно быть коротким, понятным и отвечать на вопросы где и в чем проблема. Информативный заголовок помогает понять суть проблемы, не читая весь баг-репорт. Пример: Оприходование. В оприходовании неправильно показывает итоговую сумму на (WEB, IOS и Android)
5. Описание и сценарий. Подробное описание бага и сценарий воспроизведения (последовательные действия), которые нужно совершить, чтобы воспроизвести баг.
6. Дополнительная информация, окружение и вложения. Например: ссылка или id магазина(-ов) , id: компании*, операции*, штрихкод товара, какие способы ещё пробовали, чтобы воспроизвести баг, и что получилось. Где нашли баг. Например: web, iOS, android, pos-касса. Версия клиента(приложения).
*Фото или Видео-фиксация:
""",

    )
    request_bot_answer(callback,"Text")
    await callback.message.answer("Ваше Имя")
    await state.set_state(BugForm.name)


@bug_router.message(BugForm.name)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await message.answer("Введите наименование франшизы")
    await state.set_state(BugForm.franchise_name)


@bug_router.message(BugForm.franchise_name)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(franchise_name=message.text)
    await message.answer("Номер телефона")
    await state.set_state(BugForm.phone_number)


@bug_router.message(BugForm.phone_number)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(phone_number=message.text)
    await message.answer("Название бага")
    await state.set_state(BugForm.bug_name)


@bug_router.message(BugForm.bug_name)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(bug_name=message.text)
    await message.answer("Описание и сценарий")
    await state.set_state(BugForm.description_and_scenario)


@bug_router.message(BugForm.description_and_scenario)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(description_and_scenario=message.text)
    await message.answer("Дополнительная информация. (фото или видео)")
    await state.set_state(BugForm.additional_information)


@bug_router.message(BugForm.additional_information)
async def process_name(message: Message, state: FSMContext) -> None:
    data = {}
    match message.content_type:
        case ContentType.PHOTO:
            data[ContentType.PHOTO.value] = message.photo
            data["type"] = ContentType.PHOTO.value
        case ContentType.VIDEO:
            data[ContentType.VIDEO.value] = message.video
            data["type"] = ContentType.VIDEO.value
        case ContentType.DOCUMENT:
            data[ContentType.DOCUMENT.value] = message.document
            data["type"] = ContentType.DOCUMENT.value
        case _:
            data["type"] = ContentType.TEXT.value
        #     await message.answer("Дополнительная информация. (Только фото или видео)")


    await state.update_data(data)
    data = await state.get_data()
    data["workflow"] = "bug"
    result = amo_request(message.from_user, data)
    await message.answer(result)
    await state.set_state(None)
    await state.clear()
