from aiogram.fsm.state import State, StatesGroup


class AuthState(StatesGroup):
    """Состояния аутентификации."""
    username = State()
    password = State()


class BaseState(StatesGroup):
    choose_work = State()


class ShellIsolateState(BaseState):
    """Состояния при выборе Оболочки."""
    work = State()
    construction = State()
    title = State()


class TwistState(BaseState):
    """Состояния при выборе Скрутки"""
    work = State()
    metall = State()
    count_wires = State()
    diametr_wires = State()


class ArticleState(BaseState):
    """Сотояние при выборе артикула:"""
    work = State()
    article = State()
