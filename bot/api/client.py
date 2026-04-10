import os

import aiohttp
from aiogram.fsm.context import FSMContext


async def get_headers(state: FSMContext) -> dict:
    """Возвращает заголовки с токеном авторизации"""
    user_data = await state.get_data()
    access_token = user_data.get("access_token")
    if not access_token:
        return {}
    return {"Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"}


async def get_constructions(headers):
    """Запрос к таблице Construction."""
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://{os.getenv("POSTGRES_HOST")}:8000/api/construction/',
                               headers=headers) as response:
            if response.status == 200:
                return await response.json()
            return None


async def get_metall(headers):
    """Запрос к таблице Metall."""
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://{os.getenv("POSTGRES_HOST")}:8000/api/components/metall/',
                               headers=headers) as response:
            data = await response.json()
            if response.status == 200 and data != []:
                return data
            return None


async def get_twist(headers, params):
    """Запрос к таблице Twisting."""
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://{os.getenv("POSTGRES_HOST")}:8000/api/twist/',
                               params=params,
                               headers=headers) as response:
            data = await response.json()
            if response.status == 200 and data != []:
                return data
            return None


async def auth_func(auth_data):
    """Функция авторизации."""
    async with aiohttp.ClientSession() as session:
        async with session.post(f'http://{os.getenv("POSTGRES_HOST")}:8000/api/auth/jwt/login',
                                data=auth_data) as response:
            if response.status == 200:
                return await response.json()
            return None
