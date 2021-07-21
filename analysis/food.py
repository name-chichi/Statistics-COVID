import csv
import os.path

import numpy as np
import pandas as pd

from config.settings import DATA_DIRS

class Restaurant:
    # COVID-19 기간 일반음식점 개업,폐업 수
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

    def Region(self):
        result = {}
        if os.path.isfile(DATA_DIRS[0] + '\\region.csv'):
            normal_restaurants_opening_region_group = pd.read_csv(DATA_DIRS[0] + '\\region.csv')

            # 리스트 변환
            categories = normal_restaurants_opening_region_group['region'].unique().tolist()
            series = []
            year_list = normal_restaurants_opening_region_group['year'].unique().tolist()

            for year in year_list:
                temp_dict = {
                    'name': str(year),
                    'data': normal_restaurants_opening_region_group[
                        normal_restaurants_opening_region_group['year'] == year][
                        '상세영업상태명'].tolist(),
                }
                series.append(temp_dict)

            # 결과값 추출
            result = {
                'categories': categories,
                'series': series,
            }
        else:
            # 데이터 불러오기
            normal_restaurants = pd.read_csv(DATA_DIRS[0] + '\\food_normal_restaurants.csv', encoding='cp949')

            # 지역 컬럼 전처리
            normal_restaurants['region'] = np.where(pd.notnull(normal_restaurants['소재지전체주소']),
                                                    normal_restaurants['소재지전체주소'], normal_restaurants['도로명전체주소'])
            normal_restaurants['region'] = normal_restaurants['region'].astype(str)
            normal_restaurants['region'] = normal_restaurants.region.str.split(' ').str[0]
            normal_restaurants = normal_restaurants[(normal_restaurants['region'].str.endswith('시')) | (normal_restaurants['region'].str.endswith('도'))]

            # 인허가날짜 전처리(5년)
            normal_restaurants_5year = normal_restaurants[
                (normal_restaurants['인허가일자'] >= 20160101) & (normal_restaurants['인허가일자'] <= 20210630)]
            normal_restaurants_5year_opening = normal_restaurants_5year[normal_restaurants_5year['상세영업상태명'] == '영업']
            normal_restaurants_5year_opening['인허가일자'] = pd.to_datetime(normal_restaurants_5year_opening['인허가일자'],
                                                                       format='%Y%m%d')
            normal_restaurants_5year_opening['year'] = normal_restaurants_5year_opening['인허가일자'].dt.year

            # groupby - 기간+지역
            normal_restaurants_opening_region = normal_restaurants_5year_opening.groupby(['region', 'year'])
            normal_restaurants_opening_region_group = normal_restaurants_opening_region["상세영업상태명"].count()
            normal_restaurants_opening_region_group = normal_restaurants_opening_region_group.reset_index()

            # groupby 데이터프레임 csv 파일로 저장
            normal_restaurants_opening_region_group.to_csv(DATA_DIRS[0] + '\\region.csv', mode='w')

            # 리스트 변환
            categories = normal_restaurants_opening_region_group['region'].unique().tolist()
            series = []
            year_list = normal_restaurants_opening_region_group['year'].unique().tolist()

            for year in year_list:
                temp_dict = {
                    'name': str(year),
                    'data': normal_restaurants_opening_region_group[normal_restaurants_opening_region_group['year'] == year][
                        '상세영업상태명'].tolist(),
                }
                series.append(temp_dict)

            # 결과값 추출
            result = {
                'categories': categories,
                'series': series,
            }

        print(result)
        return result

if __name__ == '__main__':
    Restaurant().Region()