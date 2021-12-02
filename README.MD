# 博客网站生成器

## 1.简介:
		语言:Python3.9
		框架:FastApi
		服务:uvicorn
		数据库:Sqlalchemy+Mysql
		前端模板引擎:jinja2

## 2.功能:
		根据数据库字段自动生成主页/分类页/详情页
#### 2.1 主页:
		1.路径:'/'
		2.返回随机获取数据库keyword字段作为分类
		3.返回最新数据
#### 2.2 分类页:
		1.路径:'/{category}?page=1'
		2.返回随机获取数据库keyword字段作为分类
		3.返回最新数据
		4.返回当前页数及最大页数
#### 2.3 详情页
		1.路径:'/{category}/{source}'
		2.返回随机获取数据库keyword字段作为分类
		3.根据source返回一条数据
		4.随机返回几条数据

#### 2.4 sitemap页
        1.路径:/sitemap.xml
        2.根据xml Sitemaps协议
        3.自动获取用户访问的域名,返回数据库所有分类页URL及最新1000条数据的URL
## 3.准备:
### 3.1 安装依赖
```		
	pip install -r requirements.txt
```
### 3.2 配置文件
		config.py 

### 3.3 准备数据库
        根据配置创建数据库,将data.sql导入该数据库表中
        注意:表中keyword字段作为网站分类,分类种类至少需要配置的条数以上才能运行,否则报错!

## 4.运行:
		
```
	python main.py
```

## 5.jinja2前端模板引擎基础: 
参考:http://doc.yonyoucloud.com/doc/jinja2-docs-cn/index.html
#### 5.1 语法
###### 5.11 遍历语句:
```
    <ul>
      {% for 单个数据名 in 数据字段_list %}
        <li>
          {{ 单个数据名.属性 }}
        </li>
      {% endfor %}
    </ul>
```
###### 5.12 过滤器用法:
```HTML
		{{  单个数据名.属性 | 过滤器方法() }}
		<a href="/{{ category.keyword  | replace(' ','-')}}">{{ category.keyword }}</a>
```
###### 5.13 if语句及运算语句:
```HTML
		{% if 单个数据名.属性 >=18 %}
			<p>你已满18岁 {{ 单个数据名.属性-18 }}年</p>
		{% elif 单个数据名.属性 < 18 %}
			<p>你还差{{ 18-单个数据名.属性 }}年满18岁</p>
		{% else %}
			<p>pass</p>
		{% endif %}
```
## 6.页面字段及属性

#### 6.1 主页:
###### 6.11 主页分类字段:
	1.字段名: data.category_list
	2.类型:列表 
	3.遍历后属性:
		关键字(分类):  单个数据名.keyword    
###### 6.11 主页数据字段:
	1.字段名: data.index_data_list
	2.类型:列表 
	3.遍历后属性:
        标题:        单个数据名.title
        图片链接:     单个数据名.img_src
        source:      单个数据名.source
        关键字(分类): 单个数据名.keyword
        描述:         单个数据名.description
        作者:         单个数据名.author
#### 6.2 分类页:
###### 6.21 分类页面包屑字段:
	1.字段名: data.category
	2.类型:字符串
	3.解释:用于面包屑当前分类
###### 6.22 分类页分类字段:
	1.字段名: data.category_list
	2.类型:列表 
	3.遍历后属性:
		关键字(用于分类):  单个数据名.keyword    
###### 6.23 分类页数据字段:
	1.字段名: data.category_data_list
	2.类型:列表 
	3.遍历后属性:
        标题:        单个数据名.title
        图片链接:     单个数据名.img_src
        source:      单个数据名.source
        关键字(分类): 单个数据名.keyword
        描述:         单个数据名.description
        作者:         单个数据名.author
###### 6.24 分类页翻页字段:
		1.字段名: data.page
		2.类型:整数
		3解释:用于当前分类第几页
----------------------------------
		1.字段名: data.max_page
		2.类型:整数
		3解释:用于当前分类最大页数
#### 6.3 详情页:
###### 6.31 详情页面包屑字段:
		1.字段名:data.category
		2.类型:字符串
		3.解释:用于面包屑当前分类
###### 6.31 详情页分类字段:
	1.字段名: data.category_list
	2.类型:列表 
	3.遍历后属性:
		关键字(分类):  单个数据名.keyword  

###### 6.32 详情页数据字段:
	1.字段名: data.one_info_data_list
	2.类型:列表 
	3.遍历后属性:
            标题:      单个数据名.title
            关键字:	  单个数据名.keyword
            创建时间:  单个数据名.create_time
            图片链接:  单个数据名.img_src
            正文:	  单个数据名.content
            source:   单个数据名.source
            描述:      单个数据名.description
            作者:      单个数据名.author
		
###### 6.33 详情页随机数据字段:
	1.字段名: data.random_info_data_list
	2.类型:列表 
	3.遍历后属性:
        标题:       单个数据名.title
        关键字:	单个数据名.keyword
        创建时间:   单个数据名.create_time
        图片链接:   单个数据名.img_src
        source:    单个数据名.source
        描述:       单个数据名.description
        作者:       单个数据名.author
		

	