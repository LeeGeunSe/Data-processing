# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 17:29:36 2021

@author: gslee
"""


import datetime
from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import os

user_name = ['jdheee']
mid_sector=['MJ_01']
buoy_name = pd.read_excel('/home/'+user_name+'/SPECTRUM_3days/인근 부이 정리.xlsx', header=None)

for i in range(len(mid_sector)):
    path ='/home/'+user_name+'/TY_M/'+mid_sector+'/CAL'
    event_list = os.listdir(path)
    for j in range(len(event_list)):
        #새롭게 저장하는 폴더 만들어주기
        mkdir('/home/'+user_name+'/SPECTRUM_3days/'+event_list[j])        
        #태풍/비태풍 폴더에 가서 항 이름이 포함된 파일 list만 추출
        port_list = os.listdir(path+'/'+event_list[j])
        port_list = [file for file in port_list if file.endswith(event_list[j]+'.dat')]
        for k in range(len(port_list)):
            port_name = port_list[k].split("_")[0]
            port_num = buoy_name[buoy_name[3]==port_name][2]
            port_num = port_num.reset_index(drop=True)
            port_num = port_num.pop(0)  #새로 배운 pop 함수 한번 써보고 싶었음
            port_data_o = pd.read_table(path+'/'+event_list[j]+'/RLT_M/'+'%03d'%port_num+'.dat',header=None)
            #파고 최대일때의 시간 찾기
            port_data =list(port_data_o[0][0].split())
            for l in range(1,len(port_data_o)):
                if float(list(port_data_o[0][l].split())[1]) > float(port_data[1]): #E+01과 같이 실수형 소수점을 읽기 위해서는 
                    port_data = list(port_data_o[0][l].split())
            max_time = datetime.datetime.strptime(port_data[0],'%Y%m%d.%H%M%S')
            
        #여기부터 max 타임을 가지고 3일로 잘라주어 새로 저장하는 작업
        #f = open('F:/동남권역 스펙트럼 3일정리/SUNGSANPO_0014_SAOMAI.dat')
        #new = open('F:/동남권역 스펙트럼 3일정리/new.dat','w')
            
        f = open(path+'/'+event_list[j]+'/'+port_list[k])
        new = open('/home/'+user_name+'/SPECTRUM_3days/'+port_list[k][:-4]+'.dat','w')
        a=f.readline()
        new.write(a)
        while a!='QUANT\n':
            a=f.readline()
            new.write(a) 
        #헤더는 모두 복사 
        for j in range(4):
            a=f.readline()
            new.write(a)
        #날짜로 구별
        start_time = max_time -datetime.timedelta(days=2)
        #start_time 기준 10분간격으로  max_time을 넘지 않는 시간을 찾는다
        while start_time <= max_time-datetime.timedelta(hours=48):
            start_time = start_time + datetime.timedelta(minutes=10)
        #새로운 start_time 전까지의 시간은 모두 패스
        while a[:15]!=start_time.strftime('%Y%m%d.%H%M%S'):
            a= f.readline()
        #지금부터 3일 뒤까지 새로운 파일에 쓰기
        end_time=start_time+datetime.timedelta(days=3,minutes=10)
        while a[:15]!=end_time.strftime('%Y%m%d.%H%M%S'):
            new.write
            a= f.readline()
        new.close()
            
            
            
            
            
