import csv

import numpy as np
import pandas as pd

from config.settings import DATA_DIRS


class Restaurant:
    def OpeningClosing(self):
        food_health = pd.read_csv(DATA_DIRS[0] + '\\food_health.csv', encoding='cp949')
        food_health = food_health[food_health['인허가일자'] >= 20160101]
        food_health_opening = food_health[food_health['상세영업상태명'] == '영업']
        food_health_opening.index = pd.to_datetime(food_health_opening['인허가일자'], format='%Y%m%d')
        monthly_opening = food_health_opening['상세영업상태명'].resample('M').count()

        food_health_closing = food_health[food_health['상세영업상태명'] == '폐업']
        food_health_closing.index = pd.to_datetime(food_health_closing['폐업일자'], format='%Y%m%d')
        monthly_closing = food_health_closing['상세영업상태명'].resample('M').count()

        index_data = monthly_opening.index.strftime('%m/%d/%y').tolist()
        opening_data = monthly_opening.tolist()
        closing_data = monthly_closing.tolist()

        result = []
        headers = ['Day Index', 'opening', 'closing']
        result.append(headers)
        for i in range(0, len(index_data)):
            temp_list = []
            temp_list.append(index_data[i])
            temp_list.append(opening_data[i])
            temp_list.append(closing_data[i])
            result.append(temp_list)

        print(result)
        return result


if __name__ == '__main__':
    Restaurant().OpeningClosing()