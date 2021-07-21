import csv
import os.path

import numpy as np
import pandas as pd

from config.settings import DATA_DIRS

class Restaurant:
    def OpeningClosing(self):
        result = {}
        if os.path.isfile(DATA_DIRS[0] + '\\openingclosing.csv'):
            df = pd.read_csv(DATA_DIRS[0] + '\\openingclosing.csv')
            result = {
                'index': df['index'].tolist(),
                'opening': df['opening'].tolist(),
                'closing': df['closing'].tolist(),
            }
        else:
            # 데이터 불러오기
            normal_restaurants = pd.read_csv(DATA_DIRS[0] + '\\food_normal_restaurants.csv', encoding='cp949')

            # 일반 음식점 5년치 개업 수
            normal_restaurants_5year = normal_restaurants[
                (normal_restaurants['인허가일자'] >= 20190101) & (normal_restaurants['인허가일자'] <= 20210630)]
            normal_restaurants_5year_opening = normal_restaurants_5year[normal_restaurants_5year['상세영업상태명'] == '영업']
            normal_restaurants_5year_opening.index = pd.to_datetime(normal_restaurants_5year_opening['인허가일자'],
                                                                    format='%Y%m%d')
            normal_restaurants_5year_opening = normal_restaurants_5year_opening['상세영업상태명'].resample('M').count()

            # 일반 음식점 5년치 폐업 수
            normal_restaurants_closing = normal_restaurants[normal_restaurants['상세영업상태명'] == '폐업']
            normal_restaurants_closing['폐업일자'] = normal_restaurants_closing['폐업일자'].apply(pd.to_numeric,
                                                                                          errors='coerce')
            normal_restaurants_closing.dropna(subset=['폐업일자'], inplace=True)
            normal_restaurants_5year_closing = normal_restaurants_closing[
                (normal_restaurants_closing['폐업일자'] >= 20190101) & (normal_restaurants_closing['폐업일자'] <= 20210630)]
            normal_restaurants_5year_closing.index = pd.to_datetime(normal_restaurants_5year_closing['폐업일자'],
                                                                    format='%Y%m%d')
            normal_restaurants_5year_closing = normal_restaurants_5year_closing['상세영업상태명'].resample('M').count()

            # 리스트 변환(날짜인덱스, 개업, 폐업)
            index_data = normal_restaurants_5year_opening.index.strftime('%Y-%m').tolist()
            opening_data = normal_restaurants_5year_opening.tolist()
            closing_data = normal_restaurants_5year_closing.tolist()

            # 결과값만 따로 csv 파일로 저장
            df = pd.DataFrame({
                'index': index_data,
                'opening': opening_data,
                'closing': closing_data,
            })
            df.to_csv(DATA_DIRS[0] + '\\openingclosing.csv', mode='w')

            # 결과값 추출
            result = {
                'index': index_data,
                'opening': opening_data,
                'closing': closing_data,
            }
        print(result)
        return result

if __name__ == '__main__':
    Restaurant().OpeningClosing()