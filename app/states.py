from aiogram.fsm.state import State, StatesGroup


class Gen(StatesGroup):
    add_user_to_group_id = State()
    create_user_to_group_title = State()

    add_home_task_item = State()
    add_home_task_task = State()
    add_home_task_grade = State()

    get_home_task_item = State()
    get_home_task_task = State()
    get_home_task_grade = State()
    get_home_task_created_at = State()