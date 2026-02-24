from fastapi import Depends, Header, HTTPException
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from .auth import SECRET_KEY, ALGORITHM, get_db
from ..models import User


def get_current_user(
    authorization: str = Header(None),
    db: Session = Depends(get_db),
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Missing or invalid authorization header",
        )

    token = authorization.split("Bearer ")[1]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user = db.query(User).filter(User.username == username).first()

        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

