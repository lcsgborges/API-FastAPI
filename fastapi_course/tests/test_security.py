from jwt import decode

from fastapi_course.security import create_access_token


def test_create_access_token(settings):
    claim = {'test': 'test'}

    token = create_access_token(claim)

    decoded = decode(token, settings.SECRET_KEY, settings.ALGORITHM)

    assert decoded['test'] == claim['test']
    assert 'exp' in decoded
