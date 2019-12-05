import uuid
import requests
import time
import json
from lxml import etree
import pandas as pd
import re
import random

#公司名称，职位，薪水，城市，学历要求，工作经验，融资情况，公司规模，工作描述，行业领域
companyname_list=[]#公司名称
positionname_list=[]#职位
salary_list=[]#薪水
city_list=[]#城市
district_list=[]#城市区域
education_list=[]#学历要求
workyear_list=[]#工作经验
financestage_list=[]#融资情况
companysize_list=[]#公司规模
workdescribe_list=[]#工作描述
industryfield_list=[]#行业领域

def get_uuid():
    return str(uuid.uuid4())

#page:页数；city：城市；kd：职位关键词
def get_lagou_information(page,city,kd):
    url="https://www.lagou.com/jobs/positionAjax.json"
    querystring={"px":"new","city":city,"needAddtionalResult":"false","isSchoolJob":"0"}
    payload="first=false&pn="+str(page)+"&kd="+str(kd)

    cookie = "JSESSIONID=" + get_uuid() + ";" \
             "user_trace_token=" + get_uuid() + "; LGUID=" + get_uuid() + "; index_location_city=%E6%88%90%E9%83%BD; " \
             "SEARCH_ID=" + get_uuid() + '; _gid=GA1.2.717841549.1514043316; ' + '_ga=GA1.2.952298646.1514043316; ' \
             'LGSID=' + get_uuid() + "; " + "LGRID=" + get_uuid() + "; "

    headers = {'cookie': cookie, 'origin': "https://www.lagou.com", 'x-anit-forge-code': "0",
               'accept-encoding': "gzip, deflate, br", 'accept-language': "zh-CN,zh;q=0.8,en;q=0.6",
               'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
               'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
               'accept': "application/json, text/javascript, */*; q=0.01",
               'referer': "https://www.lagou.com/jobs/list_Java?px=new&city=%E6%88%90%E9%83%BD",
               'x-requested-with': "XMLHttpRequest", 'connection': "keep-alive", 'x-anit-forge-token': "None",
               'cache-control': "no-cache", 'postman-token': "91beb456-8dd9-0390-a3a5-64ff3936fa63"}

    response=requests.request("POST",url,data=payload.encode('utf-8'),headers=headers,params=querystring)
    print("{} is printed...".format(response.text))
    hjson=json.loads(response.text)
    try:
        for i in range(15):#每页15个职位
            companyname=hjson['content']['positionResult']['result'][i]['companyShortName']
            compangid = hjson['content']['positionResult']['result'][i]['companyId']
            positionname=hjson['content']['positionResult']['result'][i]['positionName']
            positionid=hjson['content']['positionResult']['result'][i]['positionId']
            salary=hjson['content']['positionResult']['result'][i]['salary']
            city=hjson['content']['positionResult']['result'][i]['city']
            district=hjson['content']['positionResult']['result'][i]['district']
            education=hjson['content']['positionResult']['result'][i]['education']
            workyear=hjson['content']['positionResult']['result'][i]['workYear']
            financestage=hjson['content']['positionResult']['result'][i]['financeStage']
            companysize=hjson['content']['positionResult']['result'][i]['companySize']
            industryfield=hjson['content']['positionResult']['result'][i]['industryField']
            workdescribe=get_job_desc(positionid)
            companyname_list.append(companyname)
            positionname_list.append(positionname)
            salary_list.append(salary)
            city_list.append(city)
            district_list.append(district)
            education_list.append(education)
            workyear_list.append(workyear)
            financestage_list.append(financestage)
            companysize_list.append(companysize)
            industryfield_list.append(industryfield)
            workdescribe_list.append(workdescribe)

            print('success get {}..'.format(i))
            #延时0-2s
            time.sleep(round(random.uniform(3, 5), 2))
            print('desc={}'.format(workdescribe))
    except IndexError:
        print('获取完成...')


def get_job_desc(positionid):
    url="https://www.lagou.com/jobs/{}.html".format(positionid)
    cookie = "JSESSIONID=" + get_uuid() + ";"+"user_trace_token=" + get_uuid() + "; LGUID=" + get_uuid() + "; index_location_city=%E6%88%90%E9%83%BD; " +"SEARCH_ID=" + get_uuid() + '; _gid=GA1.2.717841549.1514043316; ' + '_ga=GA1.2.952298646.1514043316; '+'LGSID=' + get_uuid() + "; " + "LGRID=" + get_uuid() + "; "
    headers = {'cookie': cookie, 'origin': "https://www.lagou.com", 'x-anit-forge-code': "0",
               'accept-encoding': "gzip, deflate, br", 'accept-language': "zh-CN,zh;q=0.8,en;q=0.6",
               'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
               'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
               'accept': "application/json, text/javascript, */*; q=0.01",
               'referer': "https://www.lagou.com/jobs/list_Java?px=new&city=%E6%88%90%E9%83%BD",
               'x-requested-with': "XMLHttpRequest", 'connection': "keep-alive", 'x-anit-forge-token': "None",
               'cache-control': "no-cache", 'postman-token': "91beb456-8dd9-0390-a3a5-64ff3936fa63"}

    response=requests.request("GET",url,headers=headers)
    x=etree.HTML(response.text)
    #xpath语法：//：从匹配选择的当前节点选择文档中的节点，@：选取属性
    data=x.xpath('//*[@id="job_detail"]/dd[2]/div/*/text()')
    return ''.join(data)

def write_to_csv(city,kd):
    info={"companyname":companyname_list,
          "positionname":positionname_list,
          "salary":salary_list,
          "city":city_list,
          "district":district_list,
          "education":education_list,
          "workyear":workyear_list,
          "financestage":financestage_list,
          "companysize":companysize_list,
          "industryfield":industryfield_list,
          "workdescrbe":workdescribe_list
          }
    data=pd.DataFrame(info,columns=['companyname','positionname', 'salary', 'city', 'district', 'education','workyear','financestage','companysize','industryfield','workdescribe'])
    data.to_csv("lagou-"+city+"-"+kd+".csv")

def get(pages,city,kd):
    for i in range(1,pages+1):
        get_lagou_information(i,city,kd)
        time.sleep(round(random.uniform(3, 5), 2))
    write_to_csv(city,kd)
