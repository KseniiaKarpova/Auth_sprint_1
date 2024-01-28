from fastapi import HTTPException, status

unauthorized = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Bad username or password")
user_created = HTTPException(status_code=status.HTTP_201_CREATED, detail="User has been created")
access_revoked = HTTPException(status_code=status.HTTP_200_OK, detail="Access token has been revoked")
refresh_revoked = HTTPException(status_code=status.HTTP_200_OK, detail="Refresh token has been revoked")

user_exists = HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Login is already used")
incorrect_credentials = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="incorrect login or password")

role_not_found = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
role_already_exist_error = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Role already exists")
role_user_already_exist_error = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Role already exists")
crud_not_found = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Can`t create rules")

server_error = HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Sorry...")
forbidden_error = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have been denied access")
