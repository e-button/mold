import os
import pandas as pd
from google.colab import drive
from google.oauth2.service_account import Credentials
import gspread
import datetime
import xlsxwriter
import numpy as np
import matplotlib.pyplot as plt
import pathlib

# drive.mount('/content/drive')
##出現提示欄進行授權

# os.chdir('/content/drive/MyDrive/倍騰/03_製程管理') #切換該目錄
#os.listdir() #確認目錄內容

# #匯入google API憑及檔案連結
# scope = ['https://www.googleapis.com/auth/spreadsheets']
# creds = Credentials.from_service_account_file("credential/gs_credentials.json", scopes=scope)
# gs = gspread.authorize(creds)

#匯入google表單
df = pd.read_excel('example.xlsx',sheet_name='工作表1')
# sheet = gs.open_by_url('https://docs.google.com/spreadsheets/d/13Xjx9Dh1GCQqxPt24aQ0apR4bTRH8LUACPmPV9Gzn_E/edit#gid=0')
# worksheet = sheet.get_worksheet(2)
# df = pd.DataFrame(worksheet.get_all_records())
# worksheet1 = sheet.get_worksheet(3)
# #df1 = pd.DataFrame(worksheet1.get_all_records())

df

nan_value = float('NaN')
df.replace('', nan_value, inplace=True)
#df1.replace('', nan_value, inplace=True)
df.dropna(subset=['結束時間'], inplace=True)

df

col = ['開始時間','結束時間']
for list in col:
  df[list] = pd.to_datetime(df[list], format='%Y-%m-%d %H:%M:%S')

col = ['暫停時間1','繼續時間1','暫停時間2','繼續時間2']
for list in col:
  pa
  #df1[list] = pd.to_datetime(#df1[list], format='%Y-%m-%d %H:%M:%S')

df['中斷時間'] = pd.DataFrame(#df1['繼續時間1']-#df1['暫停時間1']).fillna(pd.Timedelta(seconds=0))+ pd.DataFrame(#df1['繼續時間2']-#df1['暫停時間2']).fillna(pd.Timedelta(seconds=0))

df

df = df.assign(工作小時=lambda x: x.結束時間-x.開始時間-x.中斷時間)
df

result = df.set_index('模具編號')
result

result1 = pd.pivot_table(result.drop(columns=['員工姓名']),index='模具編號',values='工作小時',columns='機台編號')
result1.columns.name = None
result1.index.name = None
result1 = result1/pd.Timedelta(hours=1)
result1 = result1.round(2)
result2 = result1.fillna(0)
result3 = result1.fillna('')
result2

result4 = result2.assign(CNC=lambda x: x.CNC01+x.CNC02+x.CNC03)
result4 = result4.assign(EDM=lambda x: x.EDM01+x.EDM02+x.EDM05)
result3.loc['Section_time'] = result4.apply(lambda x: x.sum())
result4.drop(columns=['CNC01', 'CNC02', 'CNC03', 'EDM01', 'EDM02', 'EDM05'], inplace=True)
result3['Mold_time'] = result4.apply(lambda x: x.sum(), axis=1)

