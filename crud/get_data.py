from sqlalchemy.orm import Session
import random

def index_data(db:Session,skip=0,limit=10,category=None,source=None):
    if category:
        category_data_list=db.execute(f"select id,category,title,img_src,source,keyword,description,author from data  where status=1 and keyword = '{category}' ORDER BY create_time DESC LIMIT {skip*limit},{limit}")
        return list(category_data_list)
    elif source:
        return list(db.execute(f'select * from data where source="{source}"'))
    else:
        return list(db.execute(f'select id,category,title,img_src,source,keyword,description,author from data  where status=1 ORDER BY create_time DESC LIMIT {skip},{limit}'))

def get_categorys(db:Session,count:int=1,is_all=False):
    category_list=list(db.execute(f"SELECT DISTINCT keyword FROM data"))
    if is_all:
        return category_list
    if len(category_list)>=count:
        category_list=random.sample(category_list,count)
    else:
        category_list=random.sample(category_list,len(category_list))
    return category_list

def count_by_category(db:Session,category):
    return int(db.execute(f"SELECT COUNT(id) FROM data where keyword = '{category}' and status=1").fetchone()[0])

def info_data(db:Session,count=30,keyword=None,source=None):
    if source:
        other_info_data_list = list(db.execute(f"select title,img_src,source,keyword,description,create_time,author from data  where status=1 and keyword = '{keyword}' ORDER BY RAND() LIMIT {count}"))
        return other_info_data_list
    else:
        random_info_data_list = list(db.execute(f"SELECT * FROM `data` AS t1 JOIN (SELECT ROUND(RAND() * ((SELECT MAX(id) FROM `data`) - (SELECT MIN(id) FROM `data`)) + (SELECT MIN(id) FROM `data`)) AS id ) AS t2 WHERE t1.id >= t2.id and status =1 ORDER BY t1.id LIMIT {count}"))
        return random_info_data_list





