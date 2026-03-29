from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session


@event.listens_for(Session, 'after_begin')
def session_begin(session, transaction, connection):
    # print("=====================================")
    # print("=" * 50)
    # print("📝 Транзакция началась!")
    # print(f"   Сессия: {id(session)}")
    # print(f"   Подключение: {connection}")
    # print("=" * 50)
    # print("=====================================")
    pass

@event.listens_for(Session, 'after_attach')
def session_events(session, instance):
    # print("=====================================")
    # print("=" * 50)
    # print(f"🔗 Объект присоединен к сессии: {instance.__class__.__name__}")
    # print(f"   Сессия: {id(session)}")
    # print("=" * 50)
    # print("=====================================")
    pass

@event.listens_for(Session, 'before_commit')
def before_commit(session):
    # print("=" * 60)
    # print("💾 ПЕРЕД КОММИТОМ")
    # print(f"   Сессия: {id(session)}")
    # print(f"   Новых объектов: {len(session.new)}")
    # print(f"   Измененных: {len(session.dirty)}")
    # for obj in session.new:
    #     print(f"     - {obj.__class__.__name__}: {obj}")
    # print("=" * 60)
    pass

@event.listens_for(Session, 'after_commit')
def after_commit(session):
    # print("=" * 60)
    # print("✅ ПОСЛЕ КОММИТА")
    # print(f"   Сессия: {id(session)}")
    # print("=" * 60)
    pass