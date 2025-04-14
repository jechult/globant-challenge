from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from oauth2 import create_access_token
from constants import API_USER, API_PASSWORD
from typing import Annotated

router = APIRouter(
    tags = ['Authentication']
)

@router.post('/login')
def login(user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()]):

    """This post request allows us to generate an access token for authentication
    Args:
        user_credentials: Credentials to be checked if they are valid
    Returns:
        access_token: token code as a result of authentication request
    """

    # checking if filled credentials are valid
    
    if user_credentials.username != API_USER or user_credentials.password != API_PASSWORD:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = 'Invalid credentials'
        )

    # creating an access token for authentication
    
    access_token = create_access_token(data = {"user_id": user_credentials.username})
    
    return {'access_token': access_token, "token_type": "bearer"}