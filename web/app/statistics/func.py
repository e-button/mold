import os
import pandas as pd
import datetime
import xlsxwriter
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from app.models import MoldData
def make_excel(token):
    workbook = xlsxwriter.Workbook(f'statistics_files/{token}/statistics.xlsx')

    worksheet1 = workbook.add_worksheet('工作表1')
    worksheet2 = workbook.add_worksheet('工作表2')

    ms = MoldData.objects.filter(status=1)
    max_times = 0
    for m in ms:
        times = m.times

        if not times:
            continue
        tmp = len(times)
        if tmp > max_times:
            max_times = tmp

    worksheet1.write(0, 0, '員工姓名')
    worksheet1.write(0, 1, '機台編號')
    worksheet1.write(0, 2, '加工類型')
    worksheet1.write(0, 3, '模具編號')
    worksheet1.write(0, 4, '開始時間')
    worksheet1.write(0, 5, '結束時間')

    worksheet2.write(0, 0, '員工姓名')
    worksheet2.write(0, 1, '機台編號')
    worksheet2.write(0, 2, '加工類型')
    worksheet2.write(0, 3, '模具編號')
    worksheet2.write(0, 4, '開始時間')
    for i in range(max_times):
        worksheet2.write(0, 4+(i)*2, f'暫停時間{str(i+1)}')
        worksheet2.write(0, 5+(i)*2, f'繼續時間{str(i+1)}')
    # worksheet2.write(0, 4+2*max_times, '結束時間')
    i = 1
    for m in ms:
        if not m.end_time:
            continue
        worksheet1.write(i, 0, m.staff.name)
        worksheet1.write(i, 1, m.machine.no)
        worksheet1.write(i, 2, m.process.type)
        worksheet1.write(i, 3, m.mod_no)

        worksheet2.write(i, 0, m.staff.name)
        worksheet2.write(i, 1, m.machine.no)
        worksheet2.write(i, 2, m.process.type)
        worksheet2.write(i, 3, m.mod_no)

        start_time = m.start_time
        start_time = str(start_time)
        start_time = start_time.replace('+00:00', '')

        end_time = m.end_time
        if not end_time:
            end_time = ''
        else:
            end_time = str(end_time)
            end_time = end_time.replace('+00:00', '')

        worksheet1.write(i, 4, start_time)
        worksheet2.write(i, 4, start_time)

        times = m.times
        if times:
            current_max_times = len(times)
            for i_inner in range(current_max_times):
                time = times[str(i_inner)]
                worksheet2.write(i, 4 + i_inner * 2, time["stop_time"])
                worksheet2.write(i, 5 + i_inner * 2, time["continue_time"])

        worksheet1.write(i, 5, end_time)
        # worksheet2.write(i, 4+2*max_times+1, end_time)
        i+=1

    workbook.close()


def main(token):
    token_path = f'statistics_files/{token}/'
    # os.chdir(token_path)
    df = pd.read_excel(token_path+'statistics.xlsx', sheet_name='工作表1')  # 起訖時間
    df1 = pd.read_excel(token_path+'statistics.xlsx', sheet_name='工作表2')  # 中斷時間

    # 轉時間資料格式
    col = list(df.filter(regex='時間').columns)
    for l in col:
        df[l] = pd.to_datetime(df[l], format='%Y-%m-%d %H:%M:%S')
    col1 = list(df1.filter(regex='時間').columns)
    for l in col1:
        df1[l] = pd.to_datetime(df1[l], format='%Y-%m-%d %H:%M:%S')
    # 添加欄位
    for i in range(len(df1.filter(regex='繼續').columns)):
        df1['中斷時間' + str(i + 1)] = pd.DataFrame(df1['繼續時間' + str(i + 1)] - df1['暫停時間' + str(i + 1)]).fillna(
            pd.Timedelta(seconds=0))
    df['中斷時間'] = df1.filter(regex='中斷').sum(axis=1)
    df = df.assign(工作小時=lambda x: x.結束時間 - x.開始時間 - x.中斷時間)
    result = df.set_index('模具編號')
    # 資料處理
    result1 = pd.pivot_table(result.drop(columns=['員工姓名']), index='模具編號', values='工作小時', columns='機台編號')
    result1.columns.name = None
    result1.index.name = None
    result1 = result1 / pd.Timedelta(hours=1)
    result2 = result1.round(2)
    column = ['CAD', 'CAM', 'CNC', 'EDM', 'FILTER']
    for i in column:
        result2[i] = result2.filter(regex=i).sum(axis=1)
    result2 = result2.loc[:, column]
    result2.loc['Section_time'] = result2.apply(lambda x: x.sum())
    result3 = result2.assign(Mold_time=list(result2.sum(axis=1)))
    result4 = result1.filter(regex='CNC')
    result5 = result1.filter(regex='EDM')
    result6 = pd.merge(result4, result5, left_index=True, right_index=True, how='outer')
    result6.loc['Section_time'] = result6.apply(lambda x: x.sum())
    result7 = result6.tail(1)
    result7 = result7.T.reset_index()
    result7.columns = ['Machine', 'Time(hr)']

    # 創建資料夾
    date = datetime.date.today().strftime("%Y-%m-%d")
    # os.chdir('result')
    # file = pathlib.Path(date)
    # if file.exists():
    #     os.chdir(date)
    # else:
    #     os.mkdir(date)
    #     os.chdir(date)

    # 匯出excel報表
    writer = pd.ExcelWriter(token_path+'mold_analysis.xlsx', engine='xlsxwriter')

    # Write each dataframe to a different worksheet.
    df.to_excel(writer, sheet_name='總表')
    result3.to_excel(writer, sheet_name='模具加工分析')
    result6.to_excel(writer, sheet_name='機器時數統計')

    # Close the Pandas Excel writer and output the Excel file.



    writer.save()
    # 繪製模具時數長條圖
    mold = result1.index.values.tolist()
    x = np.arange(len(mold))
    result1.apply(pd.to_numeric).plot(kind='bar', stacked=True)
    plt.xticks(x, mold, rotation=60)
    plt.xlabel('Mold', fontsize='14')
    plt.ylabel('Time(hr)', fontsize='14')
    plt.title('Mold work time analysis', fontweight='bold', fontsize='20')
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left')

    plt.savefig(token_path+'1.png', bbox_inches='tight')
    plt.pause(0.01)

    # 繪製Pie圖,plotted counter-clockwise:
    labels = result2.columns.values
    sizes = result2.iloc[-1].dropna().tolist()
    explode = len(labels) * [0]

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    plt.title('Section time analysis', fontweight='bold', fontsize='20')
    # plt.legend(bbox_to_anchor=(1,1), loc='upper left')
    ax1.axis('equal')
    plt.savefig(token_path+'2.png', bbox_inches='tight')
    plt.clf()
    plt.pause(0.01)


    # 繪製機器加工長條圖
    ax = sns.barplot(x='Machine', y='Time(hr)', data=result7)
    ax.set_title('Machine work time analysis', fontweight='bold', fontsize='20')
    sfig = ax.get_figure()
    sfig.savefig(token_path+'3.png', orientation="landscape")






