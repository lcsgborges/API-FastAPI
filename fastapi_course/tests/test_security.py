from jwt import decode

from fastapi_course.security import ALGORITHM, SECRET_KEY, create_access_token


def test_create_access_token():
    claim = {'test': 'test'}

    token = create_access_token(claim)

    decoded = decode(token, SECRET_KEY, ALGORITHM)

    assert decoded['test'] == claim['test']
    assert 'exp' in decoded
