from fastapi import APIRouter,Depends,Request,Response,Form,Cookie
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from db.session import get_db
from crud import get_data
import config,datetime


application = APIRouter()

templates = Jinja2Templates(directory='./templates')



@application.get('/robots.txt')
def robots():
    return RedirectResponse('/static/robots.txt',status_code=302)



#站点地图
@application.get('/sitemap.xml')
def sitemap(request:Request,db=Depends(get_db)):
    #request.client.host
    domain='https://{}/'.format(request.headers.get("host"))
    res_1='''
        <urlset
        xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9
        http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">'''
    res_list=['']
    category_list=get_data.get_categorys(db,is_all=True)
    data_list = get_data.index_data(db, 0, 1000)
    date = datetime.datetime.now()
    for category in category_list:
        res_list.append(category.keyword.replace(' ','-'))
    for data in data_list:
        res_list.append(data.keyword.replace(' ','-')+'/'+data.source)
    for res in res_list:
        res_1+='<url><loc>{}</loc >'.format(domain+res)
        res_1+='<lastmod>{}</lastmod>'.format(date.strftime("%Y-%m-%d"))
        res_1+='<changefreq>always</changefreq>'
        res_1+='<priority>1.0</priority></url>'
    res_1+='</urlset>'
    return Response(content=res_1,media_type='application/xml')

#主页
@application.get('/')
def index(request:Request,db=Depends(get_db)):
    category_list = get_data.get_categorys(db, count=config.INDEX_CATEGORY_COUNT)
    index_data_list=get_data.index_data(db,0,config.INDEX_DATA_COUNT)
    host = request.headers.get("host")
    return templates.TemplateResponse(
        'index.html',{
            "request": request,
            'code':200,
            'msg':'成功',
            'data':{'index_data_list':index_data_list,'category_list':category_list,'host':host}
        })
#分类页
@application.get('/{category}')
def category(request:Request,category:str,page:int=1,count:int=config.CATEGORY_DATA_COUNT,db=Depends(get_db)):
    if page==0:
        return templates.TemplateResponse('404.html', {"request": request},status_code=404)
    category=category.replace('-',' ')
    category_data_list = get_data.index_data(db,page-1,count,category)
    if len(category_data_list)<1 :
        return templates.TemplateResponse('404.html',{"request": request},status_code=404)
    category_list = get_data.get_categorys(db, count=config.CATEGORY_CATEGORY_COUNT)
    max_page=get_data.count_by_category(db,category)//count+1
    host = request.headers.get("host")
    return templates.TemplateResponse(
        'category.html', {
            "request": request,
            'code':200,
            'msg':'成功',
            'data':{'category_data_list':category_data_list,'category':category,'category_list':category_list,'page':page,'max_page':max_page,'host':host}
        })
#详情页
@application.get('/{category}/{source}')
def info(request:Request,category,source,db=Depends(get_db)):
    category = category.replace('-', ' ')
    one_info_data_list =get_data.index_data(db,0,1,source=source)
    if len(one_info_data_list)<1:
        return templates.TemplateResponse('404.html',{"request": request},status_code=404)
    host=request.headers.get("host")
    category_list = get_data.get_categorys(db, count=config.INFO_CATEGORY_COUNT)
    random_info_data_list=get_data.info_data(db,count=config.INFO_RANDOM_DATA_COUNT)
    other_info_data_list=get_data.info_data(db,count=10,keyword=category.replace('-',' '),source=source)
    return templates.TemplateResponse(
        'info.html', {
            "request": request,
            'code':200,
            'msg':'成功',
            'data':{'one_info_data_list':one_info_data_list,
                    'category':category,'category_list':category_list,
                    'random_info_data_list':random_info_data_list,'other_info_data_list':other_info_data_list,
                    'host':host}
        })

