from app.DataBase.models import async_session, Tasks
from app.DataBase.models import Users, Groups
from sqlalchemy import select, update, delete, and_, or_

from app.utils import get_date


async def add_user(user_id):
    async with async_session() as session:
        if not await user_exists(user_id):
            session.add(Users(user_id=user_id, created_at=await get_date()))
            await session.commit()


async def user_exists(user_id):
    async with async_session() as session:
        user = await session.scalar(select(Users).where(Users.user_id == user_id))

        if user:
            return True
        else:
            return False


async def add_group(group_id, title):
    async with async_session() as session:
        if await group_exists(group_id):
            return "Группа с таким айди уже существует.\nПопробуйте создать группу еще раз."
        else:
            session.add(Groups(group_id=group_id, title=title, created_at=await get_date()))
            await session.commit()


async def group_exists(group_id):
    async with async_session() as session:
        group = await session.scalar(select(Groups).where(Groups.group_id == group_id))

        if group:
            return True
        else:
            return False


async def user_exists_in_group(user_id, group_id):
    async with async_session() as session:
        if await user_exists(user_id):
            user_in_group = await session.scalar(
                select(Users.user_group).where(and_(Users.user_id == user_id, Users.user_group == group_id)))

            if user_in_group:
                return True
            else:
                return False


async def add_user_to_group(user_id, group_id):
    async with async_session() as session:
        if not await user_exists_in_group(user_id, group_id):
            await session.execute(update(Users).values(user_group=group_id).where(Users.user_id == user_id))
            await session.commit()


async def add_home_task(group_id, grade, item, task):
    async with async_session() as session:
        if await group_exists(group_id):
            session.add(Tasks(group_id=group_id, grade=grade, task=task, item=item, created_at=await get_date()))
            await session.commit()
        else:
            return "Группа с таким айди не существует.\nОбратитись до создателя бота."


async def get_home_task(user_id, group_id, grade, created_at):
    async with async_session() as session:
        if await user_exists_in_group(user_id, group_id):
            tasks = await session.execute(select(Tasks.task, Tasks.item)
                                          .filter(and_(Tasks.group_id == group_id,
                                                       Tasks.grade == grade,
                                                       Tasks.created_at == created_at)))

            result_list = tasks.fetchall()
            task_list = [(task.item, task.task) for task in result_list]

            formatted_result = {item: task for item, task in task_list}
            result = []

            for item, task in formatted_result.items():
                result.append(f"{item}: {task}")

            return result


async def get_user_groups(user_id):
    async with async_session() as session:
        return await session.scalar(select(Users.user_group).where(Users.user_id == user_id))