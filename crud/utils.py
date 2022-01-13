import hashlib,random,time

def cookie_to_token(cookie:str):
    token=''
    b = cookie.split(';')
    for bb in b:
        c = bb.strip().split('=')
        if c[0] == 'utk':
            token = c[1]
            break
    return token

#发布数据字典转元祖
def data_d_t(d_data:dict):
    title=d_data.get('title')
    keyword=d_data.get('keyword')
    img_src=d_data.get('img_src')
    author=d_data.get('author')
    description=d_data.get('description')
    recommend=d_data.get('recommend')
    category=d_data.get('category')
    if recommend == 'on':
        status=1
    else:
        status=0
    content=d_data.get('content')
    source = random.choice(['1a', 'c3', '2g', 'h2', 'g2', 'n9', 'j5', '62']) + hashlib.md5(str(time.time()).encode("UTF-8")).hexdigest()[0:random.randint(8, 19)]
    l = [title,keyword,img_src,author,description,status,content,source,category]
    return tuple(l)
