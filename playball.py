#!/usr/bin/env python
# coding: utf-8

# In[31]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
from collections import Counter


# In[2]:


def single_AB(pitcher,batter,ratio_option = True, ratio_batter = 1, ratio_pitcher = 1):
    
    batterVSpitcher = pitcher[1:] + batter[1:] # 타자 VS 투수 기록
    
    if ratio_option == True :
        batterVSpitcher = batter[1:] * ((1000*ratio_batter)/batter.PA) + pitcher[1:] * ((1000*ratio_pitcher)/pitcher.PA)

    random_number = np.random.randint(1,batterVSpitcher.PA+1) # 타석 기록
    
    res = ""
    
    if (random_number > 0) & (random_number <= batterVSpitcher['1B']) :
        res = "1B"
    sum_ = batterVSpitcher['1B']
    
    if (random_number > sum_) & (random_number <= sum_ + batterVSpitcher['2B']) :
        res = "2B"   
    sum_ += batterVSpitcher['2B']
    
    if (random_number > sum_) & (random_number <= sum_ + batterVSpitcher['3B']) :
        res = "3B"   
    sum_ += batterVSpitcher['3B']
    
    if (random_number > sum_) & (random_number <= sum_ + batterVSpitcher['HR']) :
        res = "HR"   
    sum_ += batterVSpitcher['HR']
    
    if (random_number > sum_) & (random_number <= sum_ + batterVSpitcher['SO']) :
        res = "SO"   
    sum_ += batterVSpitcher['SO']
    
    if (random_number > sum_) & (random_number <= sum_ + batterVSpitcher['BB']) :
        res = "BB"   
    sum_ += batterVSpitcher['BB']
    
    #if (random_number > sum_) & (random_number <= sum_ + batterVSpitcher['OUT']) :
    #    res = "OUT"   
    #sum_ += batterVSpitcher['OUT']
    
    if (random_number > sum_) & (random_number <= sum_ + batterVSpitcher['FLY']) :
        res = "FLY"   
    sum_ += batterVSpitcher['FLY']
    
    if (random_number > sum_) & (random_number <= sum_ + batterVSpitcher['POPUP']) :
        res = "POPUP"   
    sum_ += batterVSpitcher['POPUP']
    
    if (random_number > sum_) & (random_number <= sum_ + batterVSpitcher['GROUND']) :
        res = "GROUND"   
    sum_ += batterVSpitcher['GROUND']
    
    if res == "":
        res = random_number
    
    return(res)


# In[36]:


def base_status(res,base,out_count,score):


    if res == "SO":
        res_str = "SO"
        out_count += 1
        
    if res in ["FLY", "POPUP", "GROUND"]:
        out_count += 1
        # 2024 수비 지표
        infield_fielding_ratio = [3739,1756,3089,11916,8640,11650]
        infield_error_ratio = [949,993,994,985,961,972]
        outfield_fielding_ratio = [9166,12513,9838]
        outfield_error_ratio = [987,991,986]
        
        difficulty = np.random.randint(1,1001) # 1은 수비 쉬움, 1001은 어려움
    
        if res == "FLY" : # 뜬공상황
            res_str1 = "F"
            
            depth =  np.random.randint(1,101) # 1은 얕은 공, 100은 깊은 공 # 타구 깊이
            sample_position = np.random.randint(1,sum(outfield_fielding_ratio)+1)
            if (sample_position > 0) and (sample_position <= outfield_fielding_ratio[0]) :
                position = 7 # 좌익수
            elif (sample_position > outfield_fielding_ratio[0]) and (sample_position <= sum(outfield_fielding_ratio[0:2])) :
                position = 8 # 중견수
            else  :
                position = 9 # 우익수
            
            res_str2 = str(position)
            
        elif res == "POPUP" :
            res_str1 = "P"
            depth = 1 # 내야는 언제나 얕은 공
            sample_list = [1,2,3,3,3,4,4,4,5,5,5,6,6,6]
            position = np.random.choice(sample_list)
            res_str2 = str(position)  
            
        elif res == "GROUND" : # 땅볼 상황
            res_str1 = "G"
            
            
            action = np.random.randint(1,101)
            
            sample_position = np.random.randint(1,sum(infield_fielding_ratio)+1)
            if (sample_position > 0) and (sample_position <= infield_fielding_ratio[0]) :
                position = 1 # 투수
            elif (sample_position > infield_fielding_ratio[0]) and (sample_position <= sum(infield_fielding_ratio[0:2])) :
                position = 2 # 포수
            elif (sample_position > sum(infield_fielding_ratio[0:2])) and (sample_position <= sum(infield_fielding_ratio[0:3])) :
                position = 3 # 1루수
            elif (sample_position > sum(infield_fielding_ratio[0:3])) and (sample_position <= sum(infield_fielding_ratio[0:4])) :
                position = 4 # 2루수
            elif (sample_position > sum(infield_fielding_ratio[0:4])) and (sample_position <= sum(infield_fielding_ratio[0:5])) :
                position = 5 # 3루수
            else  :
                position = 6 # 유격수
    
            res_str2 = str(position)
            
        if position in [1,2,3,4,5,6]: # Error
            if difficulty > infield_error_ratio[position-1] : 
                res = "ERROR"
                res_str1 = "E"
                out_count -= 1
        elif position in [7,8,9]:
            if difficulty > outfield_error_ratio[position-7] : 
                res = "ERROR"
                res_str1 = "E"    
                out_count -= 1
    
        res_str = res_str1 + res_str2
        
        if out_count < 3: # 뜬공 / 땅볼 / 병살 / 희타 상황
            
            if base == "000":
                if res == "ERROR" :
                    base = "100"
                else :
                    base = "000"
                
            
            elif base == "100":
                if res == "FLY" : # 뜬공
                    base = "100"
                    
                elif res == "GROUND" : # 땅볼
                    if action <= 15 : 
                        base = "000" # 병살타 15% 
                        out_count += 1
                        res_str = "DP"
                    elif (action > 15) and (action <= 40) : 
                        base = "100" # 주자 아웃 25%
                    else :
                        base = "010" # 진루타 60%
                
                elif res == "POPUP" :
                    base = "100"
                        
                elif res == "ERROR": # 에러
                    base = "110"
    
            elif base == "010":
                if res == "FLY" : # 뜬공
                    if res_str2 == 7 : # 좌익수 뜬공
                        if depth > 85:
                            base = "001" # 진루타
                        else : 
                            base = "010"
                    elif res_str2 == 8 : # 중견수 뜬공
                        if depth > 70:
                            base = "001" # 진루타
                        else : 
                            base = "010"
                    elif res_str2 == 9 : # 우익수 뜬공
                        if depth > 50:
                            base = "001" # 진루타
                        else : 
                            base = "010"

                elif res == "GROUND" : # 땅볼
                    if res_str2 == 1 : # 투수 땅볼
                        if action <= 75   : 
                            base = "010" # 진루못함
                        elif (action <= 90) and (action > 75) :
                            base = "001" # 진루
                        else :
                            base = "100" # 선행 주자만 아웃
                    
                    elif res_str2 == 2 :
                        if action <= 75   : 
                            base = "010" # 진루못함
                        elif (action <= 90) and (action > 75) :
                            base = "001" # 진루
                        else :
                            base = "100" # 선행 주자만 아웃
                            
                    elif res_str2 == 3 :
                        if action <= 35   : 
                            base = "010" # 진루못함
                        elif (action <= 95) and (action > 35) :
                            base = "001" # 진루
                        else :
                            base = "100" # 선행 주자만 아웃
                    
                    elif res_str2 == 4 :
                        if action <= 27   : 
                            base = "010" # 진루못함
                        elif (action <= 97) and (action > 27) :
                            base = "001" # 진루
                        else :
                            base = "100" # 선행 주자만 아웃
                    
                    elif res_str2 == 5 :
                        if action <= 90   : 
                            base = "010" # 진루못함
                        elif (action <= 92) and (action > 90) :
                            base = "001" # 진루
                        else :
                            base = "100" # 선행 주자만 아웃
                        
                    elif res_str2 == 6 :
                        if action <= 50   : 
                            base = "010" # 진루못함
                        elif (action <= 90) and (action > 50) :
                            base = "001" # 진루
                        else :
                            base = "100" # 선행 주자만 아웃
                    
                elif res == "POPUP" :
                    base == "010"
                    
                elif res == "ERROR": # 에러
                    base = "101"

    
    
            elif base == "001":
                if res == "FLY" : # 뜬공
                    if depth > 80:
                        base = "001" # 진루못함
                    else :
                        base = "000" # 진루타
                        score += 1
                        res_str = "SAC"

                elif res == "GROUND" : # 땅볼
                    if res_str2 == 1 : # 투수 땅볼
                        if action <= 90   : 
                            base = "001" # 진루못함
                        elif (action <= 98) and (action > 90) :
                            base = "000" # 진루
                            score += 1
                        else :
                            base = "100" # 선행 주자만 아웃
                    
                    elif res_str2 == 2 :
                        if action <= 90   : 
                            base = "001" # 진루못함
                        elif (action <= 98) and (action > 90) :
                            base = "000" # 진루
                            score += 1
                        else :
                            base = "100" # 선행 주자만 아웃
                            
                    elif res_str2 == 3 :
                        if action <= 15   : 
                            base = "001" # 진루못함
                        elif (action <= 85) and (action > 15) :
                            base = "000" # 진루
                            score += 1
                        else :
                            base = "100" # 선행 주자만 아웃
                    
                    elif res_str2 == 4 :
                        if action <= 5   : 
                            base = "001" # 진루못함
                        elif (action <= 95) and (action > 5) :
                            base = "000" # 진루
                            score += 1
                        else : 
                            base = "100" # 선행 주자만 아웃
                    
                    elif res_str2 == 5 :
                        if action <= 5   : 
                            base = "001" # 진루못함
                        elif (action <= 95) and (action > 5) :
                            base = "000" # 진루
                            score += 1
                        else : 
                            base = "100" # 선행 주자만 아웃
                        
                    elif res_str2 == 6 :
                        if action <= 70   : 
                            base = "001" # 진루못함
                        elif (action <= 85) and (action > 70) :
                            base = "000" # 진루
                            score += 1
                        else :
                            base = "100" # 선행 주자만 아웃
                
                
                elif res == "POPUP" :
                    base = "001"
                    
                elif res == "ERROR" :
                    base = "100"
                    score += 1
                        
                    
    
                    
            elif base == "110":
                if res == "FLY" : # 뜬공
                    if res_str2 == 7 : # 좌익수 뜬공
                        if depth > 85:
                            base = "101" # 진루타
                        else : 
                            base = "110"
                    elif res_str2 == 8 : # 중견수 뜬공
                        if depth > 70:
                            base = "101" # 진루타
                        else : 
                            base = "110"
                    elif res_str2 == 9 : # 우익수 뜬공
                        if depth > 50:
                            base = "101" # 진루타
                        else : 
                            base = "110"
                elif res == "GROUND" : # 땅볼
                    if action <= 15 : 
                        base = "001" # 병살타 15% 
                        out_count += 1
                        res_str = "DP"
                    elif (action > 15) and (action <= 40) : 
                        base = "100" # 주자 아웃 25%
                    elif action == 41 :
                        base = "001" # 선행주자 아웃 1%
                    else :
                        base = "011" # 진루타 59%
                            
                elif res == "POPUP" :
                        base = "001"
                    
                elif res == "ERROR" :
                        base = "111"

    
                    
            elif base == "101":
                if res == "FLY" : # 뜬공
                    if depth > 80:
                        base = "001" # 진루못함
                    else :
                        base = "000" # 진루타
                        score += 1
                        res_str = "SAC"

                elif res == "GROUND" : # 땅볼
                    if res_str2 == 1 : # 투수 땅볼
                        if action <= 30   : # 병살타 
                            base = "000" 
                            out_count += 1
                            if out_count < 3 :
                                score += 1
                                res_str = "DP"
                            elif out_count == 3 :
                                score += 1
                                res_str = "DP"
                        elif (action <= 45) and (action > 30) : # 홈에서 태그아웃
                            base = "110" # 진루
                        elif (action <= 80) and (action > 45) : # 1루주자 아웃, 홈 세이프
                            base = "100" # 선행 주자만 아웃
                            score += 1
                        else : # 타자 아웃, 홈 세이프
                            base = "010"
                            score += 1
                        
                    
                    elif res_str2 == 2 :
                        if action <= 20   : # 병살타 
                            base = "000" 
                            out_count += 1
                            if out_count < 3 :
                                score += 1
                                res_str = "DP"
                            elif out_count == 3 :
                                score += 1
                                res_str = "DP"
                        elif (action <= 30) and (action > 20) : # 홈에서 태그아웃
                            base = "110" # 진루
                        elif (action <= 80) and (action > 30) : # 1루주자 아웃, 홈 세이프
                            base = "100" # 선행 주자만 아웃
                            score += 1
                        else : # 타자 아웃, 홈 세이프
                            base = "010"
                            score += 1
                            
                    elif res_str2 == 3 :
                        if action <= 30   : # 병살타 
                            base = "000" 
                            out_count += 1
                            if out_count < 3 :
                                score += 1
                                res_str = "DP"
                            elif out_count == 3 :
                                score += 1
                                res_str = "DP"
                        elif (action <= 35) and (action > 30) : # 홈에서 태그아웃
                            base = "110" # 진루
                        elif (action <= 70) and (action > 35) : # 1루주자 아웃, 홈 세이프
                            base = "100" # 선행 주자만 아웃
                            score += 1
                        else : # 타자 아웃, 홈 세이프
                            base = "010"
                            score += 1
                    
                    elif res_str2 == 5 :
                        if action <= 20   : # 병살타 
                            base = "000" 
                            out_count += 1
                            if out_count < 3 :
                                score += 1
                                res_str = "DP"
                            elif out_count == 3 :
                                score += 1
                                res_str = "DP"
                        elif (action <= 30) and (action > 20) : # 홈에서 태그아웃
                            base = "110" # 진루
                        elif (action <= 65) and (action > 30) : # 1루주자 아웃, 홈 세이프
                            base = "100" # 선행 주자만 아웃
                            score += 1
                        else : # 타자 아웃, 홈 세이프
                            base = "010"
                            score += 1
                        
                    elif res_str2 == 6 :
                        if action <= 30   : # 병살타 
                            base = "000" 
                            out_count += 1
                            if out_count < 3 :
                                score += 1
                                res_str = "DP"
                            elif out_count == 3 :
                                score += 1
                                res_str = "DP"
                        elif (action <= 35) and (action > 30) : # 홈에서 태그아웃
                            base = "110" # 진루
                        elif (action <= 70) and (action > 35) : # 1루주자 아웃, 홈 세이프
                            base = "100" # 선행 주자만 아웃
                            score += 1
                        else : # 타자 아웃, 홈 세이프
                            base = "010"
                            score += 1
                
                elif res == "POPUP" :
                    base = "101"
                    
                elif res == "ERROR" :
                    base = "110"
                    score += 1

    
            elif base == "011":
                if res == "FLY" : # 뜬공
                    if depth < 20:
                        base = "011" # 진루못함
                        
                        if res_str2 == 7 : # 좌익수 뜬공
                            if depth > 85:
                                base = "001" # 진루타
                                score +=1
                                res_str = "SAC"
                            else : 
                                base = "010"
                        elif res_str2 == 8 : # 중견수 뜬공
                            if depth > 70:
                                base = "001" # 진루타
                                score +=1
                                res_str = "SAC"
                            else : 
                                base = "010"
                        elif res_str2 == 9 : # 우익수 뜬공
                            if depth > 50:
                                base = "001" # 진루타
                                score +=1
                                res_str = "SAC"
                            else : 
                                base = "010"

                elif res == "GROUND" : # 땅볼
                    if res_str2 == 1 : # 투수 땅볼
                        if action <= 65   : 
                            base = "011" # 진루못함.
                        elif (action <= 90) and (action > 65) : # 진루타
                            base = "001" # 진루
                            score += 1
                        else :
                            base = "101" # 홈 승부
                    
                    elif res_str2 == 2 :
                        if action <= 65   : 
                            base = "011" # 진루못함.
                        elif (action <= 90) and (action > 65) : # 진루타
                            base = "001" # 진루
                            score += 1
                        else :
                            base = "101" # 홈 승부
                            
                    elif res_str2 == 3 :
                        if action <= 25   : 
                            base = "011" # 진루못함.
                        elif (action <= 75) and (action > 25) : # 진루타
                            base = "001" # 진루
                            score += 1
                        else :
                            base = "101" # 홈 승부
                    
                    elif res_str2 == 4 :
                        if action <= 2   : 
                            base = "011" # 진루못함.
                        elif (action <= 60) and (action > 2) : # 진루타
                            base = "001" # 진루
                            score += 1
                        else :
                            base = "101" # 홈 승부
                    
                    elif res_str2 == 5 :
                        if action <= 35   : 
                            base = "011" # 진루못함.
                        elif (action <= 75) and (action > 35) : # 진루타
                            base = "001" # 진루
                            score += 1
                        else :
                            base = "101" # 홈 승부
                        
                    elif res_str2 == 6 :
                        if action <= 2   : 
                            base = "011" # 진루못함.
                        elif (action <= 60) and (action > 2) : # 진루타
                            base = "001" # 진루
                            score += 1
                        else :
                            base = "101" # 홈 승부
                            
                elif res == "POPUP" :
                    base = "011"
                    
                elif res == "ERROR" :
                    base = "101"
                    score += 1
                
            elif base == "111":
                if res == "FLY" : # 뜬공
                    if depth < 20:
                        base = "111" # 진루못함
                        
                        if res_str2 == 7 : # 좌익수 뜬공
                            if depth > 85:
                                base = "101" # 진루타
                                score +=1
                                res_str = "SAC"
                            else : 
                                base = "110"
                                score +=1
                                res_str = "SAC"
                        elif res_str2 == 8 : # 중견수 뜬공
                            if depth > 70:
                                base = "101" # 진루타
                                score +=1
                                res_str = "SAC"
                            else : 
                                base = "110"
                                score += 1
                                res_str = "SAC"
                        elif res_str2 == 9 : # 우익수 뜬공
                            if depth > 50:
                                base = "101" # 진루타
                                score +=1
                                res_str = "SAC"
                            else : 
                                base = "110"
                                score += 1
                                res_str = "SAC"
                                
                elif res == "GROUND" : # 땅볼
                    if res_str2 == 1 : # 투수 땅볼
                        if action <= 20   : 
                            base = "011" # 타자 아웃
                            score +=1
                        elif (action <= 40) and (action > 20) : # 1루주자 아웃
                            base = "101" # 진루
                            score += 1
                        elif (action <= 60) and (action > 40) : # 3루주자 아웃
                            base = "111"
                            
                        elif (action <= 75) and (action > 60) : # 타자,1루주자 아웃
                            base = "001"
                            if out_count < 3 :
                                score += 1
                                res_str = "DP"
                            elif out_count == 3 :
                                score += 1
                                res_str = "DP"
                        else : # 타자, 3루주자 아웃
                            base = "011" # 홈 승부
                            if out_count < 3 :
                                res_str = "DP"
                            elif out_count == 3 :
                                res_str = "DP"

                            
                    
                    elif res_str2 == 2 :
                        if action <= 20   : 
                            base = "011" # 타자 아웃
                            score +=1
                        elif (action <= 40) and (action > 20) : # 1루주자 아웃
                            base = "101" # 진루
                            score += 1
                        elif (action <= 60) and (action > 40) : # 3루주자 아웃
                            base = "111"
                            
                        elif (action <= 75) and (action > 60) : # 타자,1루주자 아웃
                            base = "001"
                            if out_count < 3 :
                                score += 1
                                res_str = "DP"
                            elif out_count == 3 :
                                score += 1
                                res_str = "DP"
                        else : # 타자, 3루주자 아웃
                            base = "011" # 홈 승부
                            if out_count < 3 :
                                res_str = "DP"
                            elif out_count == 3 :
                                res_str = "DP"
                            
                    elif res_str2 == 3 :
                        if action <= 40   : 
                            base = "011" # 타자 아웃
                            score +=1
                        elif (action <= 60) and (action > 40) : # 1루주자 아웃
                            base = "101" # 진루
                            score += 1
                        elif (action <= 70) and (action > 60) : # 3루주자 아웃
                            base = "111"
                            
                        elif (action <= 90) and (action > 70) : # 타자,1루주자 아웃
                            base = "001"
                            if out_count < 3 :
                                score += 1
                                res_str = "DP"
                            elif out_count == 3 :
                                score += 1
                                res_str = "DP"
                        else : # 타자, 3루주자 아웃
                            base = "011" # 홈 승부
                            if out_count < 3 :
                                res_str = "DP"
                            elif out_count == 3 :
                                res_str = "DP"
                    
                    elif res_str2 == 4 :
                        if action <= 35   : 
                            base = "011" # 타자 아웃
                            score +=1
                        elif (action <= 70) and (action > 35) : # 1루주자 아웃
                            base = "101" # 진루
                            score += 1
                        elif (action <= 77) and (action > 70) : # 3루주자 아웃
                            base = "111"
                            
                        elif (action <= 99) and (action > 77) : # 타자,1루주자 아웃
                            base = "001"
                            if out_count < 3 :
                                score += 1
                                res_str = "DP"
                            elif out_count == 3 :
                                score += 1
                                res_str = "DP"
                        else : # 타자, 3루주자 아웃
                            base = "011" # 홈 승부
                            if out_count < 3 :
                                res_str = "DP"
                            elif out_count == 3 :
                                res_str = "DP"
                    
                    elif res_str2 == 5 :
                        if action <= 35   : 
                            base = "011" # 타자 아웃
                            score +=1
                        elif (action <= 55) and (action > 35) : # 1루주자 아웃
                            base = "101" # 진루
                            score += 1
                        elif (action <= 70) and (action > 55) : # 3루주자 아웃
                            base = "111"
                            
                        elif (action <= 90) and (action > 70) : # 타자,1루주자 아웃
                            base = "001"
                            if out_count < 3 :
                                score += 1
                                res_str = "DP"
                            elif out_count == 3 :
                                score += 1
                                res_str = "DP"
                        else : # 타자, 3루주자 아웃
                            base = "011" # 홈 승부
                            if out_count < 3 :
                                res_str = "DP"
                            elif out_count == 3 :
                                res_str = "DP"
                        
                    elif res_str2 == 6 :
                        if action <= 35   : 
                            base = "011" # 타자 아웃
                            score +=1
                        elif (action <= 70) and (action > 35) : # 1루주자 아웃
                            base = "101" # 진루
                            score += 1
                        elif (action <= 77) and (action > 70) : # 3루주자 아웃
                            base = "111"
                            
                        elif (action <= 99) and (action > 77) : # 타자,1루주자 아웃
                            base = "001"
                            if out_count < 3 :
                                score += 1
                                res_str = "DP"
                            elif out_count == 3 :
                                score += 1
                                res_str = "DP"
                        else : # 타자, 3루주자 아웃
                            base = "011" # 홈 승부
                            if out_count < 3 :
                                res_str = "DP"
                            elif out_count == 3 :
                                res_str = "DP"
                            
                elif res == "POPUP" :
                    base = "111"
                    
                elif res == "ERROR" :
                    base = "111"
                    score += 1
        
                
    if res == "1B":
        res_str = "1B"
        if base == "000":
            base = "100"
          
        elif base == "100":
            r = np.random.randint(1,11)
            if r <= 6: 
                base = "110" # 60% 확률로 1루 -> 2루
            else :
                base = "101" # 40% 확률로 1루 -> 3루
            
        elif base == "010":
            r = np.random.randint(1,11)
            if r <= 8: 
                base = "100" # 80% 확률로 2루 -> 홈
                score += 1
            else :
                base = "101" # 20% 확률로 2루 -> 3루
        
        elif base == "001":
            base = "100" 
    
        elif base == "110":
            r = np.random.randint(1,11)
            if r <= 6: 
                base = "110" # 60% 확률로 2루 -> 홈, 1루 -> 2루
                score += 1
            elif (r > 6) & (r <= 8):
                base = "101" # 20% 확률로 2루 -> 홈, 1루 -> 3루
                score += 1
            else :
                base = "111" # 20% 확률로 2루 -> 3루, 1루 -> 2루
            
        elif base == "101": # 13루
            r = np.random.randint(1,11)
            if r <= 6: 
                base = "110" # 60% 확률로 3루 -> 홈, 1루 -> 2루
                score += 1
            else :
                base = "101" # 40% 확률로 3루 -> 홈, 1루 -> 3루
                score += 1
            
        elif base == "011": # 23루
            r = np.random.randint(1,11)
            if r <= 8: 
                base = "100" # 80% 확률로 3루 -> 홈, 2루 -> 홈
                score += 2
            else :
                base = "101" # 20% 확률로 3루 -> 홈, 2루 -> 3루
                score += 1
            
        elif base == "111":
            r = np.random.randint(1,11)
            if r <= 8: 
                base = "110" # 70% 확률로 3루 -> 홈, 2루 -> 홈
                score += 2
            else :
                base = "111" # 30% 확률로 3루 -> 홈, 2루 -> 3루
                score += 1
        
    if res == "2B":
        res_str = "2B"
        
        if base == "000":
            base = "010"
          
        elif base == "100":
            r = np.random.randint(1,11)
            if r <= 7: 
                base = "010" # 70% 확률로 1루 -> 홈
                score += 1
            else :
                base = "011" # 30% 확률로 1루 -> 3루
            
        elif base == "010":
            base == "010"
            score += 1
        
        elif base == "001":
            base = "010" 
            score += 1
    
        elif base == "110":
            r = np.random.randint(1,11)
            if r <= 7: 
                base = "010" # 70% 확률로 2루 -> 홈, 1루 -> 홈
                score += 2
            else :
                base = "011" # 20% 확률로 2,3루
                score += 1
            
        elif base == "101": # 13루
            r = np.random.randint(1,11)
            if r <= 7: 
                base = "010" # 70% 확률로 1루 -> 홈
                score += 2
            else :
                base = "011" # 30% 확률로 1루 -> 3루
                score += 1
                
        elif base == "011": # 23루
            base == "010"
            score += 2
            
        elif base == "111":
            r = np.random.randint(1,11)
            if r <= 7: 
                base = "010" # 70% 확률로 1루 -> 홈
                score += 3
            else :
                base = "011" # 30% 확률로 1루 -> 3루
                score += 2
        
    if res == "3B":
        res_str = "3B"
        
        if base == "000":
            base = "001"
          
        elif base == "100":
            base = "001"
            score += 1
            
        elif base == "010":
            base = "001"
            score += 1
        
        elif base == "001":
            base = "001"
            score += 1
    
        elif base == "110":
            base = "001"
            score += 2
            
        elif base == "101": # 13루
            base = "001"
            score += 2
                
        elif base == "011": # 23루
            base = "001"
            score += 2
            
        elif base == "111":
            base = "001"
            score += 3
            
    if res == "HR":
        res_str = "HR"
        
        if base == "000":
            base = "000"
            score += 1
          
        elif base == "100":
            base = "000"
            score += 2
            
        elif base == "010":
            base = "000"
            score += 2
        
        elif base == "001":
            base = "000"
            score += 2
    
        elif base == "110":
            base = "000"
            score += 3
            
        elif base == "101": # 13루
            base = "000"
            score += 3
                
        elif base == "011": # 23루
            base = "000"
            score += 3
            
        elif base == "111":
            base = "000"
            score += 4
        
    if res == "BB":
        res_str = "BB"
        
        if base == "000":
            base = "100"
          
        elif base == "100":
            base = "110"
            
        elif base == "010":
            base = "110"
        
        elif base == "001":
            base = "101"
    
        elif base == "110":
            base = "111"
            
        elif base == "101": # 13루
            base = "111"
                
        elif base == "011": # 23루
            base = "111"
            
        elif base == "111":
            base = "111"
            score += 1
            
    return(base,out_count,score,res_str)


# In[29]:


def one_innging(team1_batter,team2_starter, team2_bullpen, batter_index, pitcher_index,pitch_count, is_starter = True, print_record = False, return_res_record = False):
    res_list = []
    rbi_list = []
    
    if is_starter == True:
        pitcher = team2_starter.loc[pitcher_index]
    else :
        pitcher = team2_bullpen.loc[pitcher_index]
    batter = team1_batter.loc[batter_index]

    
    score = 0
    base = "000"
    out_count = 0
    
    
    while out_count < 3:
        if print_record == True :
            print(pitcher.Player, "/ PITCH COUNT : ", pitch_count)
        #res = single_AB(pitcher,batter)
        res = single_AB(pitcher,batter,ratio_option = False)
        pitch = np.random.randint(1,8)
        if res == "BB":
            pitch = np.max([pitch,4])
        if res == "SO":
            pitch = np.max([pitch,3])
        pitch_count += pitch
        
        base,out_count,score,res_str = base_status(res,base,out_count,score = 0)
        if res_str[0] == "E" :
            res_list.append("ERROR")
        elif res in ["FLY","POPUP","GROUND"]:
            res = "OUT"
            res_list.append(res)
        elif res_str == "DP" :
            res_list.append(res_str)
        elif res_str == "SAC" :
            res_list.append(res_str)

        else :
            res_list.append(res)

        rbi_list.append(score)
        
        if print_record == True :
            print(batter_index,". ", batter.Player,":",res_str,"/ BASE STATUS :", base, "/ OUT COUNT :", out_count)
            print("--------------------------------------------------------------")
        
        batter_index += 1
        if batter_index == 10 :
            batter_index = 1
        batter = team1_batter.loc[batter_index] 
    
    score = sum(rbi_list)
    if print_record == True :
        print("SCORE : ",score)
    
    if return_res_record == True:
        return score, pitch_count, pitcher_index, batter_index, res_list, rbi_list
    
    return score, pitch_count, pitcher_index, batter_index


# In[39]:


def single_game(team1_name,team2_name,
                team1_roster,team2_roster,
                team1_starter_index,team2_starter_index,
                first_attack,print_record = False,print_HBE = False) :  
    
    team1_batter = team1_roster[0]
    team1_starter = team1_roster[1]
    team1_bullpen = team1_roster[2]
    
    team2_batter = team2_roster[0]
    team2_starter = team2_roster[1]
    team2_bullpen = team2_roster[2]
    
    result_by_inning = []
    
    score_list_team1 = []
    pitch_count_list_team1 = []
    pitcher_bullpen_list_team1 = [1,2,3,4,5,6,7,8]
    score_team1 = 0
    pitch_count_team1 = 0
    batter_index_team1 = 1
    pitcher_index_team1 = team1_starter_index
    pitcher_order_team1 = 1
    team1_res_batter = []
    team1_res_pitcher = []
    team1_rbi = []
    
    score_list_team2 = []
    pitch_count_list_team2 = []
    pitcher_bullpen_list_team2 = [1,2,3,4,5,6,7,8]
    score_team2 = 0
    pitch_count_team2 = 0
    batter_index_team2 = 1
    pitcher_index_team2 = team2_starter_index
    pitcher_order_team2 = 1
    team2_res_batter = []
    team2_res_pitcher = []
    team2_rbi = []
    
    for i in range(1,25):
        if print_record == True:
            print(" ")
            print(" ")
            print("[ TOP of " + str(i) + " INNING" + " ]" )
        
        # 선발 투수 교체 여부
        if pitcher_order_team2 == 1 :
            if (pitch_count_team2 >= 100) or (i>=5 and sum(score_list_team1) >= 4 ) or (i>=6 and sum(score_list_team1) >= 3  ) or  (i>=4 and sum(score_list_team1) >= 4  ) or  (sum(score_list_team1) >= 5  ):
                if print_record == True:
                    print (" ")
                    print ("*PITCHER CHANGE*")
                    print (" ")
                pitch_count_team2 = 0
                pitcher_order_team2 += 1
                if abs( (sum(score_list_team2) - sum(score_list_team1)) ) <= 3: # 접전일때
                    if ( sum(score_list_team2) - sum(score_list_team1) >= 0 ) & (i >= 9):
                        pitcher_index_team2 = pitcher_bullpen_list_team2[0] # 마무리 
                    else:
                        if len(pitcher_bullpen_list_team2) >= 4:
                            pitcher_index_team2 = np.random.choice(pitcher_bullpen_list_team2[1:5])
                        elif len(pitcher_bullpen_list_team2) == 1:
                            pitcher_index_team2 = pitcher_bullpen_list_team2[0] 
                        else :
                            random_num = np.random.randint(1,len(pitcher_bullpen_list_team2)+1)
                            pitcher_index_team2 = pitcher_bullpen_list_team2[random_num] # 마무리 제외하고
                        
                else : #  3~5점차
                    if len(pitcher_bullpen_list_team2) >= 4:
                        pitcher_index_team2 = np.random.choice(pitcher_bullpen_list_team2[-4:])
                    elif len(pitcher_bullpen_list_team2) == 1:
                        pitcher_index_team2 = pitcher_bullpen_list_team2[0] # 
                    else :
                        random_num = np.random.randint(1,len(pitcher_bullpen_list_team2)+1)
                        pitcher_index_team2 = pitcher_bullpen_list_team2[random_num] # 마무리 제외하고
                
                pitcher_bullpen_list_team2.remove(pitcher_index_team2)
                    
        else : # 불펜투수교체할 투수 선택
            if (score_team1 == 0) and (pitch_count_team2 < 25) :
                pass
            elif pitcher_index_team2 > 6 and (score_team1 <= 3) and (pitch_count_team2 < 45) and (sum(score_list_team1) - sum(score_list_team2)) > 5 :
                pass
            else: # 불펜 투수 교체
                if print_record == True:
                    print (" ")
                    print ("*PITCHER CHANGE*")
                    print (" ")
                pitcher_order_team2 += 1
                if len(pitcher_bullpen_list_team2) == 0: # 교체할 투수 없음
                    pass
                else: 
                    if abs( (sum(score_list_team2) - sum(score_list_team1)) ) <= 1: # 접전일때
                        if ( sum(score_list_team2) - sum(score_list_team1) >= 0 ) & (i >= 9):
                            pitcher_index_team2 = pitcher_bullpen_list_team2[0] # 마무리
                            
                        else:
                            if len(pitcher_bullpen_list_team2) >= 4: # 불펜 4명 이상
                                pitcher_index_team2 = np.random.choice(pitcher_bullpen_list_team2[0:4])
                            elif len(pitcher_bullpen_list_team2) == 1:# 불펜 1명
                                pitcher_index_team2 = pitcher_bullpen_list_team2[0] 
                            else : # 불펜 1~3명
                                random_num = np.random.randint(0,len(pitcher_bullpen_list_team2))
                                pitcher_index_team2 = pitcher_bullpen_list_team2[random_num] # 마무리 포함
                    
                    elif abs( (sum(score_list_team2) - sum(score_list_team1)) ) <= 3: # 접전일때
                        if ( sum(score_list_team2) - sum(score_list_team1) >= 0 ) & (i >= 9):
                            pitcher_index_team2 = pitcher_bullpen_list_team2[0] # 마무리 
                        else:
                            if len(pitcher_bullpen_list_team2) >= 4:
                                pitcher_index_team2 = np.random.choice(pitcher_bullpen_list_team2[1:5])
                            elif len(pitcher_bullpen_list_team2) == 1:
                                pitcher_index_team2 = pitcher_bullpen_list_team2[0] 
                            else :
                                random_num = np.random.randint(1,len(pitcher_bullpen_list_team2))
                                pitcher_index_team2 = pitcher_bullpen_list_team2[random_num] # 마무리 제외하고
                            
                    else : #  3~5점차
                        if len(pitcher_bullpen_list_team2) >= 4:
                            pitcher_index_team2 = np.random.choice(pitcher_bullpen_list_team2[-4:])
                        elif len(pitcher_bullpen_list_team2) == 1:
                            pitcher_index_team2 = pitcher_bullpen_list_team2[0] # 
                        else :
                            random_num = np.random.randint(1,len(pitcher_bullpen_list_team2))
                            pitcher_index_team2 = pitcher_bullpen_list_team2[random_num] # 마무리 제외하고
                    
                    pitcher_bullpen_list_team2.remove(pitcher_index_team2)
                    pitch_count_team2 = 0
        
    
        if pitcher_order_team2 == 1:
            score_team1, pitch_count_team2, pitcher_index_team2, batter_index_team1, inning_res_team1, inning_rbi_team1 = one_innging(team1_batter,team2_starter,team2_bullpen,batter_index_team1, pitcher_index_team2,pitch_count_team2,is_starter = True, print_record=print_record,return_res_record = True)
            team2_res_pitcher.append(team2_starter.Player[team2_starter_index])
        else : 
            score_team1, pitch_count_team2, pitcher_index_team2, batter_index_team1, inning_res_team1, inning_rbi_team1 = one_innging(team1_batter,team2_starter,team2_bullpen,batter_index_team1, pitcher_index_team2,pitch_count_team2,is_starter = False,print_record=print_record,return_res_record = True)
            team2_res_pitcher.append(team2_bullpen.Player[pitcher_index_team2])
            
        team1_res_batter.append(inning_res_team1)
        team1_rbi.append(inning_rbi_team1)
        score_list_team1.append(score_team1)
        pitch_count_list_team2.append(pitch_count_team2)
        
        if print_record == True:
            if first_attack == team1_name : 
                print( str(team1_name), ": " , sum(score_list_team1), "VS" ,str(team2_name), ": ",  sum(score_list_team2))
        
            if first_attack == team2_name : 
                print( str(team2_name), ": " , sum(score_list_team2), "VS" ,str(team1_name), ": ",  sum(score_list_team1))
        
        if sum(score_list_team1) > sum(score_list_team2):
            current_winning_team = "team1"
        elif sum(score_list_team1) < sum(score_list_team2):
            current_winning_team = "team2"
        elif sum(score_list_team1) == sum(score_list_team2):
            current_winning_team = "" 
            
        #############################################################################
        if print_record == True:
            print(" ")
            print(" ")
            print("[ Bottom of " + str(i) + " INNING" + " ]" )
        
    
        if (i==9) and ( sum(score_list_team2) - sum(score_list_team1) > 0 ) :
            score_list_team2.append("-")
            break
        # 선발 투수 교체 여부
        if pitcher_order_team1 == 1 :
            if (pitch_count_team1 >= 100) or (i>=5 and sum(score_list_team2) >= 4 ) or (i>=6 and sum(score_list_team2) >= 3  ) or  (i>=4 and sum(score_list_team2) >= 4  ) or  (sum(score_list_team2) >= 5  ):
                if print_record == True:
                    print (" ")
                    print ("*PITCHER CHANGE*")
                    print (" ")
                pitch_count_team1 = 0
                pitcher_order_team1 += 1
                if abs( (sum(score_list_team1) - sum(score_list_team2)) ) <= 3: # 접전일때
                    if ( sum(score_list_team1) - sum(score_list_team2) >= 0 ) & (i >= 9):
                        pitcher_index_team1 = pitcher_bullpen_list_team1[0] # 마무리 
                    else:
                        if len(pitcher_bullpen_list_team1) >= 4:
                            pitcher_index_team1 = np.random.choice(pitcher_bullpen_list_team1[1:5])
                        elif len(pitcher_bullpen_list_team1) == 1:
                            pitcher_index_team1 = pitcher_bullpen_list_team1[0] 
                        else :
                            random_num = np.random.randint(1,len(pitcher_bullpen_list_team1))
                            pitcher_index_team1 = pitcher_bullpen_list_team1[random_num] # 마무리 제외하고
                        
                else : #  3~5점차
                    if len(pitcher_bullpen_list_team1) >= 4:
                        pitcher_index_team1 = np.random.choice(pitcher_bullpen_list_team1[-4:])
                    elif len(pitcher_bullpen_list_team1) == 1:
                        pitcher_index_team1 = pitcher_bullpen_list_team1[0] # 
                    else :
                        random_num = np.random.randint(1,len(pitcher_bullpen_list_team1))
                        pitcher_index_team1 = pitcher_bullpen_list_team1[random_num] # 마무리 제외하고
                
                pitcher_bullpen_list_team1.remove(pitcher_index_team1)
                    
        else : # 불펜투수교체할 투수 선택
            if (score_team2 == 0) and (pitch_count_team1 < 25) :
                pass
            elif pitcher_index_team1 > 6 and (score_team2 <= 3) and (pitch_count_team1 < 45) and (sum(score_list_team2) - sum(score_list_team1)) > 5  :
                pass
            
            else: # 불펜 투수 교체
                if print_record == True:
                    print (" ")
                    print ("*PITCHER CHANGE*")
                    print (" ")
                pitcher_order_team1 += 1
                if len(pitcher_bullpen_list_team1) == 0: # 교체할 투수 없음
                    pass
                else: 
 
                    if abs( (sum(score_list_team1) - sum(score_list_team2)) ) <= 1: # 접전일때
                        if ( sum(score_list_team1) - sum(score_list_team2) >= 0 ) & (i >= 9):
                            pitcher_index_team1 = pitcher_bullpen_list_team1[0] # 마무리
                            
                        else:
                            if len(pitcher_bullpen_list_team1) >= 4: # 불펜 4명 이상
                                pitcher_index_team1 = np.random.choice(pitcher_bullpen_list_team1[0:4])
                            elif len(pitcher_bullpen_list_team1) == 1:# 불펜 1명
                                pitcher_index_team1 = pitcher_bullpen_list_team1[0] 
                            else : # 불펜 1~3명
                                random_num = np.random.randint(0,len(pitcher_bullpen_list_team1))
                                pitcher_index_team1 = pitcher_bullpen_list_team1[random_num] # 마무리 포함
                                
                    elif abs( (sum(score_list_team1) - sum(score_list_team2)) ) <= 3: # 접전일때
                        if ( sum(score_list_team1) - sum(score_list_team2) >= 0 ) & (i >= 9):
                            pitcher_index_team1 = pitcher_bullpen_list_team1[0] # 마무리
                            
                        else:
                            if len(pitcher_bullpen_list_team1) >= 4:
                                pitcher_index_team1 = np.random.choice(pitcher_bullpen_list_team1[1:5])
                            elif len(pitcher_bullpen_list_team1) == 1:
                                pitcher_index_team1 = pitcher_bullpen_list_team1[0] 
                            else :
                                random_num = np.random.randint(1,len(pitcher_bullpen_list_team1))
                                pitcher_index_team1 = pitcher_bullpen_list_team1[random_num] # 마무리 제외하고
                            
                    else : #  3~5점차
                        if len(pitcher_bullpen_list_team1) >= 4:
                            pitcher_index_team1 = np.random.choice(pitcher_bullpen_list_team1[-4:])
                        elif len(pitcher_bullpen_list_team1) == 1:
                            pitcher_index_team1 = pitcher_bullpen_list_team1[0] # 
                        else :
                            random_num = np.random.randint(1,len(pitcher_bullpen_list_team1))
                            pitcher_index_team1 = pitcher_bullpen_list_team1[random_num] # 마무리 제외하고
                    
                    pitcher_bullpen_list_team1.remove(pitcher_index_team1)
                    pitch_count_team1 = 0
        
    
        if pitcher_order_team1 == 1:
            score_team2, pitch_count_team1, pitcher_index_team1, batter_index_team2, inning_res_team2, inning_rbi_team2 = one_innging(team2_batter,team1_starter,team1_bullpen,batter_index_team2, pitcher_index_team1,pitch_count_team1,is_starter = True, print_record=print_record,return_res_record = True)
            team1_res_pitcher.append(team1_starter.Player[team1_starter_index])
            
        else : 
            score_team2, pitch_count_team1, pitcher_index_team1, batter_index_team2, inning_res_team2, inning_rbi_team2 = one_innging(team2_batter,team1_starter,team1_bullpen,batter_index_team2, pitcher_index_team1,pitch_count_team1,is_starter = False, print_record=print_record,return_res_record = True)
            team1_res_pitcher.append(team1_bullpen.Player[pitcher_index_team1])
            
        team2_res_batter.append(inning_res_team2)
        team2_rbi.append(inning_rbi_team2)
        score_list_team2.append(score_team2)
        pitch_count_list_team1.append(pitch_count_team1)
        
        if print_record == True:
            if first_attack == team1_name : 
                print( str(team1_name), ": " , sum(score_list_team1), "VS" ,str(team2_name), ": ",  sum(score_list_team2))
        
            if first_attack == team2_name : 
                print( str(team2_name), ": " , sum(score_list_team2), "VS" ,str(team1_name), ": ",  sum(score_list_team1))
                
        if sum(score_list_team1) > sum(score_list_team2):
            current_winning_team = "team1"
        elif sum(score_list_team1) < sum(score_list_team2):
            current_winning_team = "team2"
        elif sum(score_list_team1) == sum(score_list_team2):
            current_winning_team = "" 
            
        result_by_inning.append(current_winning_team)
        # 연장전
        if (i>=9) and ( sum(score_list_team2) - sum(score_list_team1) != 0) :
            break  
            
            


        
    # 9회초 종료시 
    
    # 기록지
            
    score_array = np.array([score_list_team1, score_list_team2])

    if first_attack == team1_name :
        df_score = pd.DataFrame(score_array, index=[team1_name, team2_name])
    if first_attack == team2_name : 
        df_score = pd.DataFrame(score_array, index=[team2_name, team1_name])
    df_score.columns = range(1,len(score_list_team1)+1)
    team1_run = 0
    team2_run = 0
    for i in df_score.iloc[0]:
        team1_run += int(i)
    for i in df_score.iloc[1]:
        if i == "-":
            pass
        else :
            team2_run += int(i)
    
    # 안타수 
    hit_types = {'1B', '2B', '3B', 'HR'}
    hit_count1 = sum(play in hit_types for inning in team1_res_batter for play in inning)
    hit_count2 = sum(play in hit_types for inning in team2_res_batter for play in inning)
    bb_types = {'BB'}
    bb_count1 = sum(play in bb_types for inning in team1_res_batter for play in inning)
    bb_count2 = sum(play in bb_types for inning in team2_res_batter for play in inning)
    error_types = {"ERROR"}
    error_count1 = sum(play in error_types for inning in team2_res_batter for play in inning)
    error_count2 = sum(play in error_types for inning in team1_res_batter for play in inning)
    
    df_score["R"] = [team1_run, team2_run]
    
    if print_HBE == True:
        df_score["H"] = [hit_count1,hit_count2]
        df_score["B"] = [bb_count1,bb_count2]
        df_score["E"] = [error_count1,error_count2]

            
    if print_record == True:
        print(" ")
        print(" ")
        print("[ FINAL SCORE ]")
        print("--------------------------------")
    
    if print_record == True:
        print( df_score )
        print("--------------------------------")
    


    decision_inning = 0
    for i in range(0,len(result_by_inning)-1):
        if result_by_inning[i] != result_by_inning[i+1] :
            decision_inning = i + 1
    
    win_inning = decision_inning + 1
    win_pitcher = ""
    losing_pitcher = ""
    
    win_team = result_by_inning[-1]
    if win_team == "team1":
        win_pitcher = team1_res_pitcher[win_inning-1]
        losing_pitcher = team2_res_pitcher[win_inning-1]
        if win_pitcher == team1_starter.Player[team1_starter_index] :
            if team1_res_pitcher.count(win_pitcher) <  5:
                win_pitcher = team1_res_pitcher[team1_res_pitcher.count(win_pitcher)] 
                
    elif win_team == "team2":
        win_pitcher = team2_res_pitcher[win_inning-1]
        losing_pitcher = team1_res_pitcher[win_inning-1]
        if win_pitcher == team2_starter.Player[team2_starter_index] :
            if team2_res_pitcher.count(win_pitcher) <  5:
                win_pitcher = team2_res_pitcher[team2_res_pitcher.count(win_pitcher)] 
        

    

    return df_score, team1_res_batter,team2_res_batter, team1_res_pitcher, team2_res_pitcher,  team1_rbi, team2_rbi, win_pitcher, losing_pitcher 


# In[40]:


def game_simulation(team1_name,team2_name,
               team1_roster,team2_roster,
               team1_starter_index,team2_starter_index,
               first_attack, trial = 10, n = 5000):
    # 경기 시뮬레이션
    
    team1_total_wins = 0
    team2_total_wins = 0
    team1_score_list = []
    team2_score_list = []
    for i in range(trial):
        team1_win = 0 
        team2_win = 0 
        for _ in range(n):
            game_result, team1_res, team2_res, team1_pitching_order, team2_pitching_order, team1_rbi, team2_rbi,win_pitcher,losing_pitcher = single_game(team1_name,team2_name,team1_roster,team2_roster,team1_starter_index,team2_starter_index,first_attack,print_record = False,print_HBE = False)
            if game_result["R"][team1_name] > game_result["R"][team2_name] :
                team1_win += 1
            elif game_result["R"][team1_name] < game_result["R"][team2_name] :
                team2_win += 1
                    
            team1_score_list.append(game_result["R"][team1_name])
            team2_score_list.append(game_result["R"][team2_name])
        team1_total_wins += team1_win
        team2_total_wins += team2_win
        print("")
        print("--------------------------------------------")
        print("--------------------------------------------")
        print("Game Simulation [",i+1,"]")
        print(str(team1_name),"wins by",team1_win/(n/100), "%" )
        print(str(team2_name),"wins by",team2_win/(n/100), "%" )
        #print("Most Simulated Result","[LA : ", LA_bin_list[i]," - ",NY_bin_list[i]," : NY]" )
        print("--------------------------------------------")
        print("--------------------------------------------")
        print("")
        
    score_list = []
    for i in range( trial * n ):
        team1_sc = team1_score_list[i]
        team2_sc = team2_score_list[i]
    
        score = str(team1_sc) + "-" + str(team2_sc)
        score_list.append(score)
    score_freq = Counter(score_list)
    sorted_scores = score_freq.most_common()
        
    return team1_total_wins,team2_total_wins,team1_score_list,team2_score_list, sorted_scores

