import pandas as pd
import numpy as np

def read_data():
    df = pd.read_csv("goibibo_com-travel_sample.csv")
    df = df.replace(np.nan, '', regex=True)
    df= df[df['hotel_star_rating'] != 0] 
    return df

f = open('flights.csv', 'w')

df = read_data()

city_list = list(df['city'].unique())

f.write(', ')
for i in city_list:
    f.write(i)
    f.write(', ')
f.write('\n')

for i in city_list:
    f.write(i)
    f.write(', ')
    f.write('\n')
