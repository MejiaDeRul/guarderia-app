from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.config import settings
from app.database.session import get_db
from app.models.user import User, UserRole


reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/login")


class CurrentUser:
    def __init__(self, roles: list[UserRole] | None = None):
        self.roles = roles


    def __call__(self, token: str = Depends(reusable_oauth2), db: Session = Depends(get_db)) -> User:
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            email: str = payload.get("sub")
            role: str = payload.get("role")
            if email is None or role is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")


        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        if self.roles and user.role not in self.roles:
            raise HTTPException(status_code=403, detail="Not enough privileges")
        return user


AdminOnly = CurrentUser([UserRole.admin])
TeacherOnly = CurrentUser([UserRole.teacher])
ParentOnly = CurrentUser([UserRole.parent])
AnyUser = CurrentUser()