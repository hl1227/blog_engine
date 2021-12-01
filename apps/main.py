from fastapi import APIRouter,Depends,Request
from fastapi.templating import Jinja2Templates
from db.session import SessionLocal
from crud import get_data
import config

application = APIRouter()

templates = Jinja2Templates(directory='./templates')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@application.get('/')
async def index(request:Request,db=Depends(get_db)):
    index_data_list=get_data.index_data(db,0,config.INDEX_DATA_COUNT)
    category_list=get_data.get_categorys(db,count=config.INDEX_CATEGORY_COUNT)
    return templates.TemplateResponse(
        'index.html',{
            "request": request,
            'code':200,
            'msg':'成功',
            'data':{'index_data_list':index_data_list,'category_list':category_list}
        })

@application.get('/{category}')
async def category(request:Request,category:str,page:int=1,count:int=config.CATEGORY_DATA_COUNT,db=Depends(get_db)):
    category=category.replace('-',' ')
    category_data_list = get_data.index_data(db,page-1,count,category)
    category_list = get_data.get_categorys(db, count=config.CATEGORY_CATEGORY_COUNT)
    max_page=get_data.count_by_category(db,category)//count+1
    return templates.TemplateResponse(
        'category.html', {
            "request": request,
            'code':200,
            'msg':'成功',
            'data':{'category_data_list':category_data_list,'category':category,'category_list':category_list,'page':page,'max_page':max_page}
        })

@application.get('/{category}/{source}')
async def category(request:Request,category,source,db=Depends(get_db)):
    category = category.replace('-', ' ')
    one_info_data_list =get_data.index_data(db,0,1,source=source)
    category_list = get_data.get_categorys(db, count=config.INFO_CATEGORY_COUNT)
    random_info_data_list=get_data.info_data(db,count=config.INFO_RANDOM_DATA_COUNT)
    return templates.TemplateResponse(
        'info.html', {
            "request": request,
            'code':200,
            'msg':'成功',
            'data':{'one_info_data_list':one_info_data_list,'category':category,'category_list':category_list,'random_info_data_list':random_info_data_list}
        })
