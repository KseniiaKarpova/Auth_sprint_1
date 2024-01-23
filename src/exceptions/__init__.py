from fastapi import HTTPException, status


unauthorized = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Bad username or password")
access_revoked = HTTPException(status_code=status.HTTP_200_OK, detail="Access token has been revoked")
refresh_revoked = HTTPException(status_code=status.HTTP_200_OK, detail="Refresh token has been revoked")
user_exists = HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Login is already used")
