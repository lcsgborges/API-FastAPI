from sqlalchemy import select

from curso_fastapi.models import User


def test_create_user_database(session):
    new_user = User(username='test', password='password', email='test@test.com')

    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'test'))

    assert user.id == 1
