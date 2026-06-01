from fastapi import APIRouter, HTTPException, Depends
from auth import hash_password, verify_password, create_access_token, get_current_user
from database import get_db
from models import Staff as StaffModel
from schemas import StaffCreate
from schemas import StaffLogin

router = APIRouter()


@router.post("/register")
async def register(user:StaffCreate, db = Depends(get_db)):
    add_staff = StaffModel(role=user.role, username=user.username, password=hash_password(user.password))
    db.add(add_staff)
    db.commit()
    return {"Message": "Staff Member Created Successfully."}

@router.post("/login")
async def login(user:StaffLogin, db = Depends(get_db)):
    get_user = db.query(StaffModel).filter(StaffModel.username == user.username).first()
    if get_user is None:
        raise HTTPException(status_code=401, detail="Incorrect Username or password")
    if not verify_password(user.password, get_user.password):
        raise HTTPException(status_code=401, detail="Incorrect Username or password")
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}