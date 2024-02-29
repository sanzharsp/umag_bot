from aiogram import BaseMiddleware
from aiogram.types import Message
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")


class CounterMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.counter = 0

    async def SendAmoCrm(self, object_data: object) -> None:
        requests.post(
            f'https://amojo.amocrm.ru/~external/hooks/telegram?t={TOKEN}',
            json=object_data)

    async def __call__(
            self,
            handler,
            event: Message,
            data,
    ):
        # event_data = event.model_dump_json(indent=2)
        # print(event_data)
        # for k, v in data.items():
        #     print(k)
        #     print(k, v)
        # print("event -------------------------------------------------------")
        #
        print(event)
        #
        # print("handler -------------------------------------------------------")
        #
        # print(handler)
        #
        # print("-------------------------------------------------------")
        #
        # print(data['raw_state'] == 'ConsultationForm:name')
        # print(event.update_id)
        # print(event.message.message_id)
        # print(event.message.date)
        # print(event.message.chat.id)
        # print(event.message.chat.type)
        # print(event.message.chat.username)
        # print(event.message.chat.first_name)
        if event.message is not None:
            await self.handle_message(data, event)
        if event.callback_query is not None:
            await self.handle_callback_query(data, event)

        return await handler(event, data)


    async def handle_callback_query(self, data, event):
        message = event.callback_query.message
        text = f'{translations[data["raw_state"]]}{button_translations[event.callback_query.data]}'

        object_data = {
            'update_id': event.update_id,
            'message': {
                'message_id': message.message_id,
                'from': {
                    'id': message.chat.id,
                    'is_bot': data['event_from_user'].is_bot,
                    'first_name': data['event_from_user'].first_name,
                    'username': data['event_from_user'].username,
                    'language_code': data['event_from_user'].language_code
                },
                'chat': {
                    'id': message.chat.id,
                    'first_name': message.chat.first_name,
                    'username': message.chat.username,
                    'type': message.chat.type
                },
                'date': int(message.date.timestamp()),
                'text': text,
            }
        }

        await self.SendAmoCrm(object_data)

    async def handle_message(self, data, event):
        message = event.message
        print(message)
        text = f'{translations[data["raw_state"]]}{message.text}'
        # if data["raw_state"] == "BugForm:additional_information":
        if (message.text is not None):
            text = f'{translations[data["raw_state"]]}{message.text}'

        elif (message.photo is not None):
            telegram_file_id = f'https://api.telegram.org/bot{os.getenv("BOT_TOKEN")}/getFile?file_id={message.photo[-1].file_id}'
            file_path = requests.get(telegram_file_id).json()
            text = f'Клиент отправил фото\n'
            text += f'https://api.telegram.org/file/bot{os.getenv("BOT_TOKEN")}/{file_path["result"]["file_path"]}'

        elif (message.video is not None):
            telegram_file_id = f'https://api.telegram.org/bot{os.getenv("BOT_TOKEN")}/getFile?file_id={message.video.file_id}'
            file_path = requests.get(telegram_file_id).json()
            text = f'Клиент отправил видео\n'
            text += f'https://api.telegram.org/file/bot{os.getenv("BOT_TOKEN")}/{file_path["result"]["file_path"]}'

        elif (message.document is not None):
            telegram_file_id = f'https://api.telegram.org/bot{os.getenv("BOT_TOKEN")}/getFile?file_id={message.document.file_id}'
            file_path = requests.get(telegram_file_id).json()
            text = f'Клиент отправил документ\n'
            text += f'https://api.telegram.org/file/bot{os.getenv("BOT_TOKEN")}/{file_path["result"]["file_path"]}'

        elif (message.audio is not None):
            telegram_file_id = f'https://api.telegram.org/bot{os.getenv("BOT_TOKEN")}/getFile?file_id={message.audio.file_id}'
            file_path = requests.get(telegram_file_id).json()
            text = f'Клиент отправил аудио\n'
            text += f'https://api.telegram.org/file/bot{os.getenv("BOT_TOKEN")}/{file_path["result"]["file_path"]}'

        elif (message.voice is not None):
            telegram_file_id = f'https://api.telegram.org/bot{os.getenv("BOT_TOKEN")}/getFile?file_id={message.voice.file_id}'
            file_path = requests.get(telegram_file_id).json()
            text = f'Клиент отправил голосовое сообщение\n'
            text += f'https://api.telegram.org/file/bot{os.getenv("BOT_TOKEN")}/{file_path["result"]["file_path"]}'

        if data['raw_state'] == "BugForm:additional_information":
            text = f'Идентификатор клиента телеграм: {message.chat.id}'

        object_data = {
            'update_id': event.update_id,
            'message': {
                'message_id': message.message_id,
                'from': {
                    'id': message.chat.id,
                    'is_bot': data['event_from_user'].is_bot,
                    'first_name': data['event_from_user'].first_name,
                    'username': data['event_from_user'].username,
                    'language_code': data['event_from_user'].language_code
                },
                'chat': {
                    'id': message.chat.id,
                    'first_name': message.chat.first_name,
                    'username': message.chat.username,
                    'type': message.chat.type
                },
                'date': int(message.date.timestamp()),
                'text': text,

            }
        }
        await self.SendAmoCrm(object_data)


translations = {
    None: "",
    'ConsultationForm:name': "🖊️ Клиент выбрал консультацию и ввел имя: ",
    'ConsultationForm:franchise_name': "🖊️ Клиент ввел наименование франшизы: ",
    'ConsultationForm:phone_number': "🖊️ Клиент ввел номер телефона: ",
    'ConsultationForm:problem_description': "🖊️ Клиент ввел описание проблемы: ",

    'BugForm:name': "🚫 Клиент хочет сообщить о баге и ввел свое имя: ",
    'BugForm:franchise_name': "🚫 Клиент ввел наименование франшизы: ",
    'BugForm:phone_number': "🚫 Клиент ввел номер телефона: ",
    'BugForm:bug_name': "🚫 Клиент ввел название бага: ",
    'BugForm:description_and_scenario': "🚫 Клиент ввел описание и сценарий: ",
    'BugForm:additional_information': "🚫 Клиент ввел дополнительную информацию: ",

    'SynchronizationForm:name': "🔄 Клиент выбрал синхранизацию и ввел имя: ",
    'SynchronizationForm:franchise_name': "🔄 Клиент ввел номер телефона: ",
    'SynchronizationForm:phone_number': "🔄 Клиент ввел название проблемы: ",
    'SynchronizationForm:problem_name': "🔄 Клиент ввел название магазина: ",
    'SynchronizationForm:shop_name': "🔄 Клиент ввел версию кассы: ",
    'SynchronizationForm:cash_register_version': "🔄 Клиент ввел имя кассира: ",
    'SynchronizationForm:cashier_name': "🔄 Клиент имя: ",
    'SynchronizationForm:cash_register_password': "🔄 Клиент ввел пароль от кассы: ",
    'SynchronizationForm:link_to_shop': "🔄 Клиент ввел ссылку на магазин: ",
    'SynchronizationForm:link_to_archive': "🔄 Клиент имя ссылку на архив: ",
    'SynchronizationForm:login': "🔄 Клиент ввел Логин: ",
    'SynchronizationForm:password': "🔄 Клиент ввел пароль: ",
    'GetCourseForm:name': "🧑‍💻 Клиент выбрал запись в GetCource и ввел свое имя: ",
    'GetCourseForm:franchise_name': "🧑‍💻 Клиент ввел наименование франшизы: ",
    'GetCourseForm:phone_number': "🧑‍💻 Клиент ввел номер телефона: ",
    'GetCourseForm:email': "🧑‍💻 Клиент ввел email: ",
    'GetCourseForm:study_type': "🧑‍💻 Клиент ввел вид обучения:: ",

}

button_translations = {
    "franchisee": "Франчайзи",
    "technical_specialist": "Технический специалист",
    "sales_manager": "Менеджер по продажам",
    "hr": "HR",
    "support_consultation": "Консультация",
    "support_bug": "Баг",
    "support_synchronization": "Синхронизация",
    "support_access_flash": "Доступ на идеальную флешку",
    "support_knowledge_base": "База знаний",
    "support_getcource": "Доступ на обучение в GetCource",
    "support_document_templates": "Шаблоны документов",
    "support_ideas": "Ваши идеи по улучшению ПО",
}