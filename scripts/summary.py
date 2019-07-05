#!/usr/bin/python
# -*- coding: UTF-8 -*- 
import os
import os.path
import re
import yaml
import time
import sys 

reload(sys) 
sys.setdefaultencoding('utf8') 

def writeSummary(summary):
    summary = [(k,summary[k]) for k in sorted(summary.keys(), reverse = True)]
    for smy in summary:
        f = open('./summary/'+smy[0]+'.md', 'w+')
        f.truncate()
        articles = smy[1]
        articles = [(k,articles[k]) for k in sorted(articles.keys(), reverse = True)]
        result = '# '+smy[0]+'\n'
        for arc in articles:
            info = arc[1]
            temp = '- ['+info.get('title')+'](.'+info.get('url')+')\n'
            result += temp
        f.write(result)
        f.close()

def writeCategory(category_map):
    f = open('./summary/category.md', 'w+')
    f.truncate()
    category = [(k,category_map[k]) for k in sorted(category_map.keys(), reverse = True)]  
    result = '# 分类\n'
    for cate in category:
       temp = '- ['+cate[0]+'](./'+cate[0]+'.md) ('+str(cate[1])+') \n'
       result += temp
    f.write(result)
    f.close()

def writeArticle(article_map):
    f = open('./summary/article.md', 'w+')
    f.truncate()
    article = [(k,article_map[k]) for k in sorted(article_map.keys(), reverse = True)]  
    result = '# 文章\n'
    for arc in article:
        info = arc[1]
        temp = '- ['+info.get('title')+'](.'+info.get('url')+')\n'
        result += temp
    f.write(result)
    f.close()

def generateSummary(rootdir):
    category_map = {}
    article_map = {}
    summary = {}
    for parent, dirnames, filenames in os.walk(rootdir):

        for filename in filenames:
            
            if ('.md' in filename):

                title = filename
                category = []
                date = int(os.path.getctime(os.path.join(parent,filename)))

                f = open(os.path.join(parent, filename), 'r+')
                content = f.read()
                f.close()

                searchObj = re.search( r'\-{3,}([\s\S]+)\-{3,}', content, re.M)

                if searchObj and searchObj.group(1):
                    config = yaml.safe_load(searchObj.group(1))

                    if config.get('title'):
                        title = config.get('title')

                    if config.get('categories'):
                        categories = config.get('categories')
                        if isinstance(categories, str):
                            category.append(categories)
                        
                        if isinstance(categories,list):
                            for cate in categories:
                                category.append(cate)
                    
                    if config.get('date'):
                        dt = str(config.get('date'))
                        # re.search( r'\d{4}\-\d{2}\-\d{2}( \d{2}:\d{2}:\d{2})', dt)
                        # date = int(time.mktime(time.strptime(dt, "%Y-%m-%d %H:%M:%S")))
                        date = int(time.mktime(time.strptime(dt, "%Y-%m-%d")))
                # else: 
                    # category.append('0')
                
                key = str(date) + '_' + title 
                value = {'title':title, 'url':os.path.join(parent,filename)}

                for cat in category:
                    if category_map.get(cat):
                        category_map[cat] += 1
                    else:
                        category_map[cat] = 0;
                        category_map[cat] += 1

                    if summary.get(cat):
                        summary[cat][key] = value
                    else:
                        summary[cat] = {};
                        summary[cat][key] = value
                
                article_map[key] = value

    writeSummary(summary)
    writeCategory(category_map)
    writeArticle(article_map)

if __name__ == '__main__':
    generateSummary('./docs')