from aiogram.types import InlineKeyboardButton
menu = [
    [InlineKeyboardButton(text="Консультация ", callback_data="support_consultation"),
     InlineKeyboardButton(text="Баг", callback_data="support_bug")],
    [InlineKeyboardButton(text="Синхронизация ", callback_data="support_synchronization"),
     InlineKeyboardButton(text="Доступ на идеальную флешку", callback_data="support_access_flash")],
    [InlineKeyboardButton(text="База знаний", callback_data="support_knowledge_base"),
     InlineKeyboardButton(text="Доступ на обучение в GetCource", callback_data="support_getcource")],
    [InlineKeyboardButton(text="Шаблоны документов", callback_data="support_document_templates"),
     InlineKeyboardButton(text="Ваши идеи по улучшению ПО", callback_data="support_ideas")
     ]
]

command_menu: dict[str, str] = {
    '/start': 'Запуск бота',
    '/menu': 'Меню',
}

