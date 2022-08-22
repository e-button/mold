#!/usr/bin/env python
# coding: utf-8

# In[22]:


import os
import pandas as pd
import datetime
import xlsxwriter
import numpy as np
import matplotlib.pyplot as plt
import pathlib
import seaborn as sns

def mold_analysis():
    os.chdir(os.getcwd())
    df = pd.read_excel('MoldData.xlsx',sheet_name='工作表1')
    df1 = pd.read_excel('MoldData.xlsx',sheet_name='工作表2')
    nan_value = float('NaN')
    df.replace('', nan_value, inplace=True)
    df1.replace('', nan_value, inplace=True)
    df.dropna(subset=['結束時間'], inplace=True)
    col = ['開始時間','結束時間']
    for list in col:
        df[list] = pd.to_datetime(df[list], format='%Y-%m-%d %H:%M:%S')

    col1 = ['暫停時間1','繼續時間1','暫停時間2','繼續時間2']
    for list in col1:
        df1[list] = pd.to_datetime(df1[list], format='%Y-%m-%d %H:%M:%S')

    df['中斷時間'] = pd.DataFrame(df1['繼續時間1']-df1['暫停時間1']).fillna(pd.Timedelta(seconds=0))+ pd.DataFrame(df1['繼續時間2']-df1['暫停時間2']).fillna(pd.Timedelta(seconds=0))
    df = df.assign(工作小時=lambda x: x.結束時間-x.開始時間-x.中斷時間)
    result = df.set_index('模具編號')
    result1 = pd.pivot_table(result.drop(columns=['員工姓名']),index='模具編號',values='工作小時',columns='機台編號')
    result1.columns.name = None
    result1.index.name = None
    result1 = result1/pd.Timedelta(hours=1)
    result1 = result1.round(2)
    result2 = result1.fillna(0)
    result3 = result1.fillna('')
    result4 = result2.assign(CNC=lambda x: x.CNC01+x.CNC02+x.CNC03)
    result4 = result4.assign(EDM=lambda x: x.EDM01+x.EDM02+x.EDM05)
    result3.loc['Section_time'] = result4.apply(lambda x: x.sum())
    result4.drop(columns=['CNC01', 'CNC02', 'CNC03', 'EDM01', 'EDM02', 'EDM05'], inplace=True)
    result3['Mold_time'] = result4.apply(lambda x: x.sum(), axis=1)
    result5 = pd.DataFrame({'CAD': result4['CAD01'],'CAM': result4['CAM02'],'CNC': result4['CNC'],'EDM': result4['EDM'],'FILTER': result4['FILTER']})
    result5.loc['Section_time'] = result5.apply(lambda x: x.sum())
    result6 = result3.drop(columns=['CAD01','CAM02','FILTER','Mold_time'])
    section = result6.columns.values.tolist()
    for list in section:
        filter = result6[list] != ''
        result6 = result6[filter]
    result6 = result6.T.reset_index()
    result6.columns = ['Machine', 'Time(hr)']

    #創建資料夾
    date = datetime.date.today().strftime("%Y-%m-%d")
    os.chdir('result')
    file = pathlib.Path(date)
    if file.exists():
        os.chdir(date)
    else:
        os.mkdir(date)
        os.chdir(date)

    #匯出excel報表
    writer = pd.ExcelWriter(date+' mold_analysis.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='總表')
    result3.to_excel(writer, sheet_name='分析')
    writer.save()

    #繪製模具時數長條圖
    mold = result2.index.values.tolist()
    x = np.arange(len(mold))
    result2.apply(pd.to_numeric).plot(kind='bar', stacked=True)
    plt.xticks(x, mold, rotation=60)
    plt.xlabel('Mold', fontsize='14')
    plt.ylabel('Time(hr)', fontsize='14')
    plt.title('Mold work time analysis', fontweight='bold', fontsize='20')
    plt.legend(bbox_to_anchor=(1,1), loc='upper left')
    #plt.show()
    plt.savefig('Mold_Analysis.png', bbox_inches='tight')
    plt.pause(0.1)

    #繪製Pie圖
    labels = result5.columns.values
    sizes = result5.iloc[-1].dropna().tolist()
    explode = len(labels)*[0]  
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    plt.title('Section time analysis', fontweight='bold', fontsize='20')
    ax1.axis('equal')  

    #plt.show()
    plt.savefig('Section_Analysis.png', bbox_inches='tight')
    plt.pause(0.1)

    #繪製機器加工長條圖
    ax = sns.barplot(x='Machine', y='Time(hr)', data=result6)
    ax.set_title('Machine work time analysis', fontweight='bold', fontsize='20')
    sfig = ax.get_figure()
    sfig.savefig('Machine_Analysis.png',  orientation="landscape")


mold_analysis()