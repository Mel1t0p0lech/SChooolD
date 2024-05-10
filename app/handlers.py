from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import app.DataBase.request as rq
import app.keyboard as kb
from app.states import Gen
from app.utils import generate_random_code

router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    if await rq.user_exists(msg.from_user.id):
        await msg.answer("Вы находитесь в меню бота.\nНиже приведен ряд кнопок, которыю являются навигатором по всему "
                         "боту.", reply_markup=kb.menu_markup)
    else:
        await msg.answer("Приветсвую вас в боте HomeTasker!\nДанный бот поможет вам с получением ДЗ.\n\n\nДля "
                         "продолжения работы с ботом нажмите на кнопку.", reply_markup=kb.register_button_markup)


@router.callback_query(F.data == "register_account")
async def register_account(call: CallbackQuery):
    await rq.add_user(call.from_user.id)
    await call.message.answer(
        "Успшено!\nВаш ID был добавлен в базу данных бота.\nТеперь вы можете пользоватся ботом.",
        reply_markup=kb.menu_markup)


@router.callback_query(F.data == "add_user_to_group")
async def add_user_to_group_handler(call: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.add_user_to_group_id)
    await call.message.answer(
        "Введите ID группы в которую желаете вступить:\n(ID можно получить от пользователей/создателя группы.)")


@router.message(Gen.add_user_to_group_id)
async def add_user_to_group_id(msg: Message, state: FSMContext):
    await state.update_data(add_user_to_group_id=msg.text)
    data = await state.get_data()
    await rq.add_user_to_group(msg.from_user.id, data['add_user_to_group_id'])
    await msg.answer("Успешно!\nВы были добавленны в группу.\nДля дальшего пользования с группами вернитесь в меню.")
    await state.clear()


@router.callback_query(F.data == "info_about_user")
async def info_about_user(call: CallbackQuery):
    await call.message.edit_text(f"Инофрмация о пользователе:\n"
                                 f"ID: {call.from_user.id},\nСостоит в группе:"
                                 f" {await rq.get_user_groups(user_id=call.from_user.id)}.")


@router.callback_query(F.data == "group_menu")
async def group_menu_handler(call: CallbackQuery):
    await call.message.answer(f"Вы находитесь в меню группы.\nID группы: {await rq.get_user_groups(call.from_user.id)}",
                              reply_markup=kb.group_menu_markup)


@router.callback_query(F.data == "create_group")
async def create_group_handler(call: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.create_user_to_group_title)
    await call.message.answer("Введите название для группы.")


@router.message(Gen.create_user_to_group_title)
async def create_group_title(msg: Message, state: FSMContext):
    await state.update_data(create_user_to_group_title=msg.text)
    data = await state.get_data()
    generated_code = await generate_random_code(6)

    await rq.add_group(generated_code, data['create_user_to_group_title'])
    await msg.answer(f"Группа была создана.\nID: {generated_code}.\nНазвание: {data['create_user_to_group_title']}")


@router.callback_query(F.data == "add_home_task")
async def add_home_task_handler(call: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.add_home_task_grade)
    await call.message.answer("Введите класс для которого хотите добавить ДЗ.")


@router.message(Gen.add_home_task_grade)
async def add_home_task_grade(msg: Message, state: FSMContext):
    await state.update_data(add_home_task_grade=msg.text)
    await state.set_state(Gen.add_home_task_task)
    await msg.answer("Введите предмет")


@router.message(Gen.add_home_task_task)
async def add_home_task_task(msg: Message, state: FSMContext):
    await state.update_data(add_home_task_task=msg.text)
    await state.set_state(Gen.add_home_task_item)
    await msg.answer("Введите ДЗ")


@router.message(Gen.add_home_task_item)
async def add_home_task_item(msg: Message, state: FSMContext):
    await state.update_data(add_home_task_item=msg.text)
    data = await state.get_data()

    await rq.add_home_task(
        await rq.get_user_groups(msg.from_user.id), data['add_home_task_grade'],
        data['add_home_task_task'], data['add_home_task_item'])
    await msg.answer("ДЗ было добавленно в базу данных.")
    await state.clear()


@router.callback_query(F.data == "get_home_task")
async def get_home_task_handler(call: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.get_home_task_grade)
    await call.message.answer("Введите класс из которого хотите получить ДЗ.")


@router.message(Gen.get_home_task_grade)
async def get_home_task_grade(msg: Message, state: FSMContext):
    await state.update_data(get_home_task_grade=msg.text)
    await state.set_state(Gen.get_home_task_created_at)
    await msg.answer("Введите дату за которую хотите получить ДЗ в формате xxxx-xx-xx (год-месец-день, пример: 2007-01.01)")


@router.message(Gen.get_home_task_created_at)
async def get_home_task_created_at(msg: Message, state: FSMContext):
    await state.update_data(get_home_task_created_at=msg.text)
    data = await state.get_data()

    wtf = await rq.get_home_task(msg.from_user.id, await rq.get_user_groups(msg.from_user.id), data['get_home_task_grade'],
                           data['get_home_task_created_at'])
    await msg.answer(f"{wtf}")
    await state.clear()
