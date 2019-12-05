import  os
import pandas as pd
import matplotlib.pyplot as plt
import pyecharts
from  pyecharts import Page
import re
from collections import Counter
import get_information

def data_draw(csv_file):
    page=Page(csv_file+":按区域分析")
    #读取csv转为dataframe格式
    d=pd.read_csv(csv_file,engine='python',encoding='utf-8')
    position_info=d['positionname'].value_counts()
    #画职位信息柱状图
    position_bar=pyecharts.Bar('职位信息柱状图')
    position_bar.add('职位',position_info.index,position_info.values,is_stack=True,is_label_show=True)
    position_bar.render(csv_file[:-4]+"_职位信息柱状图.html")
    page.add_chart(position_bar)


    salary_info=d['salary'].values
    #画薪水信息柱状图
    salary_bar=pyecharts.Bar('薪水信息柱状图')

    dict={'2k-':0,'2k-5k':0,'5k-10k':0,'10k-15k':0,'15k-20k':0,'20k-30k':0,'30k+':0}
    for salary in salary_info:
        #正则表达式：^开始符，$结束符,[]:范围,\d:数字,{}位数
        if re.match('^[0-1]k-*|.*-[0-1]k$',salary)!=None:
            dict['2k-']+=1
        if re.match('^[2-4]k-*|.*-[2-4]k$', salary) != None:
            dict['2k-5k'] += 1
        if re.match('^[5-9]k-*|.*-[5-9]k$', salary) != None:
            dict['5k-10k'] += 1
        if re.match('^1[0-4]k-*|.*-1[0-4]k$', salary) != None:
            dict['10k-15k'] += 1
        if re.match('^1[5-9]k-*|.*-1[5-9]k$', salary) != None:
            dict['15k-20k'] += 1
        if re.match('^2[0-9]k-*|.*-2[0-9]k$', salary) != None:
            dict['20k-30k'] += 1
        if re.match('^[3-9][0-9]k-*|.*-[3-9][0-9]k$|\d{3,}k-*|.*-\d{3,}k$', salary) != None:
            dict['30k+'] += 1

    salary_bar.add('薪水',list(dict.keys()),list(dict.values()),is_stack=True,is_label_show=True)
    salary_bar.render(csv_file[:-4]+'_薪水信息柱状图.html')
    page.add_chart(salary_bar)


    industryfield_info=d['industryfield'].values
    #行业分布饼状图
    industryfield_pie=pyecharts.Pie('行业分布饼状图',title_pos='right')
    industryfields=[]
    for i in range(len(industryfield_info)):
        try:
            data=re.split('[,、 ]',industryfield_info[i])#逗号，顿号，空格
        except:
            continue
        for j in range(len(data)):
            industryfields.append(data[j])
    counts=Counter(industryfields) #字典类型
    print(type(counts))

    industryfield_pie.add('',list(counts.keys()),list(counts.values()),radius=[15,60],label_text_color=None,is_label_show=True,legend_orient='vertical',is_more_utils=True,legend_pos='left')
    industryfield_pie.render(csv_file[:-4]+'_行业分布饼状图.html')
    page.add_chart(industryfield_pie)


    companysize_info=d['companysize'].value_counts()
    #公司规模饼状图
    companysize_pie=pyecharts.Pie('公司规模饼状图',title_pos='right')
    companysize_pie.add('',companysize_info.index,companysize_info.values,radius=[15,60],label_text_color=None,is_label_show=True,legend_orient='vertical',is_more_utils=True,legend_pos='left')
    companysize_pie.render(csv_file[:-4]+'_公司规模饼状图.html')
    page.add_chart(companysize_pie)


    #公司融资情况饼状图
    financestage_info=d['financestage'].value_counts()
    financestage_pie=pyecharts.Pie('公司融资信息饼状图',title_pos='right')
    financestage_pie.add('',financestage_info.index,financestage_info.values,radius=[15,60],label_text_color=None,is_label_show=True,legend_orient='vertical',is_more_utils=True,legend_pos='left')
    financestage_pie.render(csv_file[:-4]+'_公司融资信息饼状图.html')
    page.add_chart(financestage_pie)


    #工作经验饼状图
    workyear_info = d['workyear'].value_counts()
    workyear_pie = pyecharts.Pie('工作经验信息饼状图', title_pos='right')
    workyear_pie.add('', workyear_info.index, workyear_info.values, radius=[15, 60], label_text_color=None,
                         is_label_show=True, legend_orient='vertical', is_more_utils=True, legend_pos='left')
    workyear_pie.render(csv_file[:-4] + '_工作经验信息饼状图.html')
    page.add_chart(workyear_pie)


    #学历要去饼状图
    education_info = d['education'].value_counts()
    education_pie = pyecharts.Pie('学历要求信息饼状图', title_pos='right')
    education_pie.add('', education_info.index, education_info.values, radius=[15, 60], label_text_color=None,
                     is_label_show=True, legend_orient='vertical', is_more_utils=True, legend_pos='left')
    education_pie.render(csv_file[:-4] + '_学历要求信息饼状图.html')
    page.add_chart(education_pie)


    #工作地点饼状图
    district_info = d['district'].value_counts()
    district_pie = pyecharts.Pie('工作地点信息饼状图', title_pos='right')
    district_pie.add('', district_info.index, district_info.values, radius=[15, 60], label_text_color=None,
                      is_label_show=True, legend_orient='vertical', is_more_utils=True, legend_pos='left')
    district_pie.render(csv_file[:-4] + '_工作地点信息饼状图.html')
    page.add_chart(district_pie)

    #汇总
    page.render(csv_file[:-4]+'.html')


def main(csv_file):
    csv_file=csv_file
    data_draw(csv_file)


if __name__ == '__main__':
    page=8
    city='成都'
    kd='嵌入式'
    get_information.get(page,city,kd)
    main('lagou-{}-{}.csv'.format(city,kd))