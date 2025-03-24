from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.user import User

# This is a simplified auth implementation for development purposes
# In a real application, you would implement proper JWT token validation

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    # For development, we'll just return a test user
    # In a real application, you would validate the token and get the user from the database
    
    # Check if we have a test user, if not create one
    user = db.query(User).filter(User.email == "test@example.com").first()
    
    if not user:
        # This is just for development - in production you would validate tokens properly
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user
