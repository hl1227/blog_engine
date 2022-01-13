from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from apps import application,admin
from fastapi.responses import RedirectResponse
import uvicorn
app=FastAPI(
    title='博客网站生成器',
    docs_url=None,
    redoc_url=None
)
app.mount(path='/static', app=StaticFiles(directory='./static'), name='static')  # .mount()不要在分路由APIRouter().mount()调用，模板会报错


app.add_middleware(
    CORSMiddleware,
    allow_origins=[#信任的域
        "http://127.0.0.1",
        "http://127.0.0.1:8080",'*'],
    allow_credentials=True,#允许的证书
    allow_methods=["*"],   #跨域的请求方法[get,post,put]
    allow_headers=["*"],   #允许的请求头
)
# @app.middleware('http')
# async def add_process_time_header(request: Request, call_next):  # call_next将接收request请求做为参数
#     url=str(request.url)
#     if 'admin' in url and 'login' not in url:
#         if  request.cookies.get('utk'):
#             response = await call_next(request)
#             return response
#         else:
#             return RedirectResponse('/admin/login',status_code=302)
#
#     return await call_next(request)

# app.include_router(admin,prefix='/admin')
app.include_router(admin,prefix='/admin')
app.include_router(application,prefix='')

app.mount(path='/admin', app=StaticFiles(directory='./templates/admin'), name='admin')  # .mount()不要在分路由APIRouter().mount()调用，模板会报错

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8001, reload=True, workers=1)
    #uvicorn.run('main:app', host='0.0.0.0', port=80)