# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 10:58:10 2021

@author: gslee
"""

# 기상청 해양관측부이 자료 

import pandas as pd
import os
import numpy as np

    
# 기준에 따라 데이터 QC    
path='F:/기상청_30min'
file_list = os.listdir(path)
for i in range(0,len(file_list)):
    file = pd.read_excel(path+'/'+file_list[i])
    #육안으로 확인된 튀는 구간
    if i ==14 : #인천 부이 경우
         f0=file[pd.Timestamp(2020, 9, 4, 7, 00)<=file['일시']]
         f0= f0[f0['일시']<=pd.Timestamp(2020, 9, 4, 17, 30)]
         file.loc[f0.index[:]]=None
         
         f0=file[pd.Timestamp(2020, 9, 7, 12, 00)<=file['일시']]
         f0= f0[f0['일시']<=pd.Timestamp(2020, 9, 7, 22, 00)]
         file.loc[f0.index[:]]=None
         
         f0=file[pd.Timestamp(2020, 9, 8, 9, 00)<=file['일시']]
         f0= f0[f0['일시']<=pd.Timestamp(2020, 9, 8, 19, 30)]
         file.loc[f0.index[:]]=None
    if i ==15 : #추자도 부이 경우
         f0=file[pd.Timestamp(2020, 2, 23, 12, 00)<=file['일시']]
         f0= f0[f0['일시']<=pd.Timestamp(2020, 2, 24, 2, 00)]
         file.loc[f0.index[:]]=None
         f0=file[pd.Timestamp(2020, 9, 15, 15, 00)<=file['일시']]
         f0= f0[f0['일시']<=pd.Timestamp(2020, 9, 15, 18, 30)]
         file.loc[f0.index[:]]=None
    if i ==3 : #덕적도 부이 경우
         f0=file[pd.Timestamp(2020, 10, 11, 17, 00)<=file['일시']]
         f0= f0[f0['일시']<=pd.Timestamp(2020, 10, 11, 17, 30)]
         file.loc[f0.index[:]]=None
    if i ==19 : #홍도 부이 경우
         f0=file[pd.Timestamp(2020, 7, 1, 00, 00)<=file['일시']]
         f0= f0[f0['일시']<=pd.Timestamp(2020, 7, 9, 12, 00)]
         file.loc[f0.index[:]]=None
    #CASE02 파고 0 파고 Nan도 제거됨
    file1 = file[file['유의파고(m)']>0]
    #CASE03 주기 0 주기 Nan도 제거됨
    file2 = file1[file1['파주기(sec)']>0]
    #CASE04 주기 16이상
    file3 = file2[file2['파주기(sec)']<16]
    #결측된 날짜들 NaN값으로 채워주는 작업 그림그릴때 중요 (결측구간이 이어져서 그려질 수 있음)
    file3.index=pd.DatetimeIndex(file3['일시']) #resample을 위해 index를 시간으로 바꿔줌
    file=file3.drop(['일시'],axis=1) #이제 필요없으니 제거
    file=file.resample('30T').first() #30분간격으로 데이터 resample해주는 작업
    file.to_excel('F:/기상청QC데이터/'+file_list[i][:-5]+'.xlsx')