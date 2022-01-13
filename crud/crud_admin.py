from sqlalchemy.orm import Session
import random

def sql_userdata(db:Session,username,password_hx=None):
    if password_hx:
        sql_userdata=db.execute(f"select * from user where username='{username}' and password_hx='{password_hx}'").fetchone()
        if not sql_userdata:
            return None
        return sql_userdata
    else:
        sql_userdata=db.execute(f"select * from user where username='{username}'").fetchone()
        if not sql_userdata:
            return None
        return sql_userdata
#后台创建用户
def create_user(db:Session,create_data:dict):
    db.execute(f"insert into user(username,password_hx,authority,email,phone_num,nickname)  values(:username,:password_hx,:authority,:email,:phone_num,:nickname)",create_data)
    db.commit()

def index_data(db:Session,skip=0,limit=10,category=None,source=None):
    if category:
        category_data_list=db.execute(f"select * from data  where  keyword = '{category}' ORDER BY create_time DESC LIMIT {skip*limit},{limit}")
        return list(category_data_list)
    elif source:
        return list(db.execute(f'select * from data where source="{source}"'))
    #后台返回全部数据
    else:
        return list(db.execute(f'select * from data  ORDER BY create_time DESC LIMIT {skip},{limit}'))

def get_categorys(db:Session,count:int=1,is_all=False):
    category_list=list(db.execute(f"SELECT DISTINCT keyword FROM data"))
    #后台返回全部分类
    if is_all:
        return category_list
    if len(category_list)>=count:
        category_list=random.sample(category_list,count)
    else:
        category_list=random.sample(category_list,len(category_list))
    return category_list
#后台发布数据
def insert_data(db:Session,t_data):
    try:
        db.execute(f"insert into data(title,keyword,img_src,author,description,status,content,source,category)  values{t_data}")
        db.commit()
        return '发布成功!'
    except Exception as e:
        return 'error:发布失败,'+str(e)
#后台修改博客数据a
def update_blog_data(db:Session,update_blog_data:dict):
    db.execute(f"update data set title=:title,status=:status,author=:author,description=:description,img_src=:img_src,content=:content,keyword=:keyword where id=:id",update_blog_data)
    db.commit()
#后台删除博客数据
def delete_blog_data(db:Session,id_dict:dict):
    if id_dict.get('id'):
        db.execute(f"delete from data where id=:id",id_dict)
    else:
        pass
    db.commit()
#后台修改关键字数据
def update_keyword_data(db:Session,update_keyword_data:dict):
    db.execute(f"update data set keyword=:category_new where keyword=:category_old",update_keyword_data)
    db.commit()

#后台删除关键字数据
def delete_keyword_data(db:Session,delete_keyword_data:dict):
    db.execute(f"delete from data where keyword=:category_delete",delete_keyword_data)
    db.commit()
#后台修改用户信息
def update_user_data(db:Session,user_data:dict):
    db.execute(f"update data set username=:username,nickname=:nickname,email=:email,phone_num=:phone_num")
