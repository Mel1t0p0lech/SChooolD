from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

menu = [[InlineKeyboardButton(text="Зайти в группу", callback_data="add_user_to_group"),
         InlineKeyboardButton(text="Создать группу", callback_data="create_group")],
        [InlineKeyboardButton(text="Меню группы", callback_data="group_menu")],]
        # [InlineKeyboardButton(text="Информация о пользователе", callback_data="info_about_user")]]

group_menu = [
    [InlineKeyboardButton(text="Получить ДЗ", callback_data="get_home_task"),
     InlineKeyboardButton(text="Добавить ДЗ", callback_data="add_home_task")],
]

register_button_markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Зарегестрировать аккаунт", callback_data="register_account")]])

menu_markup = InlineKeyboardMarkup(inline_keyboard=menu)
group_menu_markup = InlineKeyboardMarkup(inline_keyboard=group_menu)
