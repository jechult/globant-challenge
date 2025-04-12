from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = 'login')

SECRET_KEY = '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict):

    """This function generates an access token once user is correctly authenticated
    Args:
        data: user data to be part of token generation
    Returns:
        access_token: token code generated from jwt library
    """

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):

    """This function verify if access token is still valid
    Args:
        token: token code as a result of access token creation
    Returns:
        token_data: token id as a result of correct checking
    """

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])

        id: str = payload.get('user_id')

        if id is None:
            raise credentials_exception
        
        return 0
    
    except JWTError:

        raise credentials_exception
    
def get_current_user(
    token: str = Depends(oauth2_scheme)
):

    """This function returns a 0 value is checking process is ok
    Args:
        token: token code as a result of access token creation
    Returns:
        message: 0 value as a result of correct checking
    """

    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = 'It was not possible to validate credentials',
        headers = {"WWW-Authenticate": "Bearer"}
    )

    return verify_access_token(token, credentials_exception)