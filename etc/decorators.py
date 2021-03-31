from functools import wraps

from fastapi import Request, HTTPException


# Decorator function to check if a user is authenticated
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if kwargs['request'].state.user_id is None:
            raise HTTPException(status_code=401, detail="User needs to be logged in - bearer token missing / incorrect")
        return func(*args, **kwargs)
    return wrapper
