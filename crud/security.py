from datetime import datetime, timedelta
from fastapi import Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError,jwt
from passlib.context import CryptContext
from db.session import get_db
from crud import crud_admin



# oauth2_schema = OAuth2PasswordBearer(tokenUrl="/api/login")
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  # schemes参数值算法在:passlib.hash
#
# def get_hash(password):#哈希加密
#     return pwd_context.hash(password)
#
# def jwt_authenticate_user(user,password: str):#验证用户
#     verity_password_res=pwd_context.verify(password, user.password)#验证接收用户密码与数据库加密用户密码
#     print('验证密码:', verity_password_res)
#     if not verity_password_res:
#         raise HTTPException(status_code=401,detail='密码输入错误!')
#     return user

SECRET_KEY = 'fa6ef66fd74ad65695288df40d86b43eaca88f8b500551fcabccdc6b3dd4ee04'
ALGORITHM = 'HS256'
#生成token
def create_access_token(data:dict):
    to_encode = data.copy()
    print('加密前数据',to_encode)
    encoded_jwt = jwt.encode(claims=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)#加密
    print('加密后数据',encoded_jwt)
    return encoded_jwt


#token获取当前用户名
def token_get_current_user(token):
    #token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTYzNTQxNTk0Nn0.ywoux75755NVSH3WjQ1GcjloUK6A2IbdJiohIcJuxsM'
    try:#解密
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        print('解密后:',payload)
        return payload
    except JWTError as e:
        print('解密报错:', e)
        return None


#
# #####后台用户权限依赖
# def get_current_authority_user(current_user = Depends(jwt_get_current_user)):
#     if current_user.authority in ['root','manager']:#判断是否是管理权限用户:
#         return current_user
#     else:
#         raise HTTPException(403,'用户权限不够!')
# # async def jwt_get_current_authority_user(token):
# #     current_user: User = await jwt_get_current_user(token=token)
# #     if current_user.authority
# #         return current_user
# #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
