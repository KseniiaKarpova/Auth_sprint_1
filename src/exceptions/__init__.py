from fastapi import HTTPException, status


unauthorized = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Bad username or password")
access_revoked = HTTPException(status_code=status.HTTP_200_OK, detail="Access token has been revoked")
refresh_revoked = HTTPException(status_code=status.HTTP_200_OK, detail="Refresh token has been revoked")

role_not_found = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
role_already_exist_error = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Role already exists")
user_not_found = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")