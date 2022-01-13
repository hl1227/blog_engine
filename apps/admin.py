from fastapi import APIRouter,Depends,Request,Response,Form,Body
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from db.session import get_db
from crud import security,crud_admin,utils
import config,datetime
from fastapi.staticfiles import StaticFiles

admin = APIRouter()
templates = Jinja2Templates(directory='./templates/admin')

#admin.mount(path='/888', app=StaticFiles(directory='./templates/admin'), name='888')  # .mount()不要在分路由APIRouter().mount()调用，模板会报错

######################################################################
@admin.get('')
def admin_index(request:Request,db=Depends(get_db)):
    token=request.cookies.get('utk')
    if token:
        #解密token
        token_dict=security.token_get_current_user(token)
        token_username=token_dict.get('username')
        sql_userdata = crud_admin.sql_userdata(db, token_username)
        return templates.TemplateResponse(
            '/01-yibiaopan.html', {
                "request": request,
                'data': {'msg': '','user':sql_userdata}
            }
        )
    else:
        return RedirectResponse('/admin/login',status_code=302)

######################################################################
#后台登录页
@admin.get('/login')
def admin_login(request:Request):
    return templates.TemplateResponse(
        '/login.html', {
            "request": request,
            'data': {'msg':''}
        })
#后台登录返回token4656465
@admin.post('/login/token')
def admin_token(request:Request,username=Form(...),password=Form(...),db=Depends(get_db)):
    print(username)
    print(password)
    #对比数据库用户
    sql_userdata=crud_admin.sql_userdata(db, username, password)
    if sql_userdata:
        referer=request.headers.get('Referer')
        if '/admin/login' in referer:
            referer='/admin'
        # 生成token
        token=security.create_access_token({'username':sql_userdata.username})
        print('生成的token:',token)
        res=RedirectResponse(referer,status_code=302)
        res.set_cookie('utk',token,max_age=6000)
        return res
    return {'msg':'账号密码错误'}
#后台登录创建用户
@admin.post('/login/create_user')
def admin_create_user(create_user_data=Body(...),db=Depends(get_db)):
    print('接收到的注册用户数据:', create_user_data)
    try:
        crud_admin.create_user(db,create_user_data)
        return {'msg': '注册成功'}
    except Exception as e:
        e=str(e)
        print(e)
        if 'Duplicate entry' in e:
            return {'msg': f'注册失败:用户名重复!'}
        return {'msg': f'注册失败:{e}'}
######################################################################
#发布博客
@admin.get('/issue_blog')
def issue_blog(request:Request,db=Depends(get_db)):
    token = request.cookies.get('utk')
    if token:
        # 解密token
        token_dict = security.token_get_current_user(token)
        token_username = token_dict.get('username')
        sql_userdata = crud_admin.sql_userdata(db, token_username)
        return templates.TemplateResponse(
            '/02-issue_blog.html', {
                "request": request,
                'data': {'msg': '', 'user': sql_userdata}
            }
        )
    else:
        return RedirectResponse('/admin/login',status_code=302)

#发布博客数据
@admin.post('/issue_blog/issue_data')
def issue_data(request:Request,issue_data=Body(...),db=Depends(get_db)):
    token = request.cookies.get('utk')
    if token:
        # 解密token
        token_dict = security.token_get_current_user(token)
        token_username = token_dict.get('username')
        if token_username:
            t_data=utils.data_d_t(issue_data)
            print(f'接收的发布数据:{t_data}')
            return {'msg':crud_admin.insert_data(db,t_data)}
    else:
        return templates.TemplateResponse(
            '/login.html', {
                "request": request,
            })
######################################################################
#博客管理
@admin.get('/blog_manager')
def blog_manager(request:Request,db=Depends(get_db)):
    token = request.cookies.get('utk')
    if token:
        # 解密token
        token_dict = security.token_get_current_user(token)
        token_username = token_dict.get('username')
        sql_userdata = crud_admin.sql_userdata(db, token_username)
        # 所有分类数据
        category_list = crud_admin.get_categorys(db, is_all=True)
        return templates.TemplateResponse(
            '/03-blog_manager.html', {
                "request": request,
                'data': {'msg': '', 'user': sql_userdata,'category_list':category_list}
            }
        )
    else:
        return RedirectResponse('/admin/login',status_code=302)
#博客管理-返回数据
@admin.get('/blog_manager/data')
def blog_data(category:str=None,page:int=1,count:int=100,q:str=None,db=Depends(get_db)):
    print('接收到的返回数据参数q:',q)
    if q:
        #return {'data':[{'title':'ttt','keyword':'key','content':'con','img_path':'img','status':1,'description':'description',},]}
        index_data_list = crud_admin.index_data(db, page - 1, count, category)
        return {'data': index_data_list}
    else:
        index_data_list = crud_admin.index_data(db, page-1,count,category)
        return {'data':index_data_list}

#博客管理-修改数据
@admin.post('/blog_manager/update_data')
def update_data(request:Request,update_blog_data=Body(...),db=Depends(get_db)):
    print('接收到的修改博客数据:',update_blog_data)
    try:
        crud_admin.update_blog_data(db,update_blog_data)
        return {'msg': '修改成功'}
    except Exception as e:
        print(e)
        return {'msg':f'修改失败:{e}'}

#博客管理-删除数据
@admin.post('/blog_manager/delete_data')
def delete_data(request:Request,delete_data=Body(...),db=Depends(get_db)):
    print('接收到的删除数据:',delete_data)
    try:
        crud_admin.delete_blog_data(db, delete_data)
        return {'msg': '删除成功'}
    except Exception as e:
        print(e)
        return {'msg': f'删除失败:{e}'}
######################################################################
#分类管理
@admin.get('/category_manager')
def category_manager(request:Request,db=Depends(get_db)):
    token = request.cookies.get('utk')
    if token:
        # 解密token
        token_dict = security.token_get_current_user(token)
        token_username = token_dict.get('username')
        sql_userdata = crud_admin.sql_userdata(db, token_username)
        # 分类管理-分类数据
        category_list = crud_admin.get_categorys(db, is_all=True)
        return templates.TemplateResponse(
            '/04-category_manager.html', {
                "request": request,
                'data': {'msg': '', 'user': sql_userdata,'category_list':category_list}
            }
        )
    else:
        return RedirectResponse('/admin/login',status_code=302)

#分类管理-修改分类
@admin.post('/category_manager/update_category')
def update_category(request:Request,update_keyword_data=Body(...),db=Depends(get_db)):
    print('接收到的修改分类数据:',update_keyword_data)
    try:
        crud_admin.update_keyword_data(db,update_keyword_data)
        return {'msg': '修改成功'}
    except Exception as e:
        print(e)
        return {'msg':f'修改失败:{e}'}


#分类管理-删除分类
@admin.post('/category_manager/delete_category')
def delete_category(request:Request,delete_keyword_data=Body(...),db=Depends(get_db)):
    print('接收到的删除分类数据:',delete_keyword_data)
    try:
        crud_admin.delete_keyword_data(db, delete_keyword_data)
        return {'msg': '删除成功'}
    except Exception as e:
        print(e)
        return {'msg': f'删除失败:{e}'}
######################################################################
#标签管理
@admin.get('/tag_manager')
def tag_manager(request:Request,db=Depends(get_db)):
    token = request.cookies.get('utk')
    if token:
        # 解密token
        token_dict = security.token_get_current_user(token)
        token_username = token_dict.get('username')
        sql_userdata = crud_admin.sql_userdata(db, token_username)
        return templates.TemplateResponse(
            '/05-tag_manager.html', {
                "request": request,
                'data': {'msg': '', 'user': sql_userdata}
            }
        )
    else:
        return RedirectResponse('/admin/login',status_code=302)
#标签管理-修改标签
@admin.post('/tag_manager/update_tag')
def update_tag(request:Request,data=Body(...)):
    print('接收到的修改标签数据:',data)
    return {'msg': '修改成功'}



#标签管理-删除标签
@admin.post('/tag_manager/delete_tag')
def delete_tag(request:Request,data=Body(...)):
    print('接收到的删除标签数据:',data)
    return {'msg': '删除成功'}
######################################################################
#评论管理
@admin.get('/comment_manager')
def comment_manager(request:Request,db=Depends(get_db)):
    token = request.cookies.get('utk')
    if token:
        # 解密token
        token_dict = security.token_get_current_user(token)
        token_username = token_dict.get('username')
        sql_userdata = crud_admin.sql_userdata(db, token_username)
        return templates.TemplateResponse(
            '/06-comment_manager.html', {
                "request": request,
                'data': {'msg': '', 'user': sql_userdata}
            }
        )
    else:
        return RedirectResponse('/admin/login',status_code=302)
######################################################################
#个人中心
@admin.get('/configuration')
def configuration(request:Request,db=Depends(get_db)):
    token = request.cookies.get('utk')
    if token:
        # 解密token
        token_dict = security.token_get_current_user(token)
        token_username = token_dict.get('username')
        sql_userdata = crud_admin.sql_userdata(db, token_username)
        return templates.TemplateResponse(
            '/07-configuration.html', {
                "request": request,
                'data': {'msg': '', 'user': sql_userdata}
            }
        )
    else:
        return RedirectResponse('/admin/login',status_code=302)
#个人中心-修改用户数据
@admin.post('/configuration/update_user')
def update_user(data=Body(...),db=Depends(get_db)):
    print(data)
    return {'msg':'修改成功'}
#个人中心-修改用户密码
@admin.post('/configuration/update_user_password')
def update_user_password(data=Body(...),db=Depends(get_db)):
    print(data)
    return {'msg':'修改成功'}
######################################################################
#安全退出
@admin.get('/logout')
def blog_manager(request:Request):
    token = request.cookies.get('utk')
    if token:
        res=RedirectResponse('/',status_code=302)
        res.delete_cookie('utk')
        return res
        # # 解密token
        # token_dict = security.token_get_current_user(token)
        # token_username = token_dict.get('username')
        # sql_userdata = crud_admin.sql_userdata(db, token_username)
        # return templates.TemplateResponse(
        #     '/06-comment_manager.html', {
        #         "request": request,
        #         'data': {'msg': '', 'user': sql_userdata}
        #     }
        # )
    else:
        return RedirectResponse('/admin/login',status_code=302)
######################################################################