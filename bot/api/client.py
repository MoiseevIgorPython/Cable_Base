import os
import aiohttp
from aiogram.fsm.context import FSMContext

_session: aiohttp.ClientSession | None = None

def get_session() -> aiohttp.ClientSession:
    global _session
    if _session is None:
        # It's better to initialize this in the main loop, 
        # but this is a fallback.
        _session = aiohttp.ClientSession()
    return _session

async def close_session():
    global _session
    if _session:
        await _session.close()
        _session = None

def get_backend_url():
    host = os.getenv("BACKEND_HOST", os.getenv("POSTGRES_HOST", "localhost"))
    return f"http://{host}:8000/api"

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
    session = get_session()
    async with session.get(f'{get_backend_url()}/construction/',
                           headers=headers) as response:
        if response.status == 200:
            return await response.json()
        return None


async def get_metall(headers):
    """Запрос к таблице Metall."""
    session = get_session()
    async with session.get(f'{get_backend_url()}/components/metall/',
                           headers=headers) as response:
        data = await response.json()
        if response.status == 200 and data != []:
            return data
        return None


async def get_twist(headers, params):
    """Запрос к таблице Twisting."""
    session = get_session()
    async with session.get(f'{get_backend_url()}/twist/',
                           params=params,
                           headers=headers) as response:
        data = await response.json()
        if response.status == 200 and data != []:
            return data
        return None


async def auth_func(auth_data):
    """Функция авторизации."""
    session = get_session()
    async with session.post(f'{get_backend_url()}/auth/jwt/login',
                            data=auth_data) as response:
        if response.status == 200:
            return await response.json()
        return None
