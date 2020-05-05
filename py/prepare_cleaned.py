#conda activate ir
import pandas as pd
path = '../data/'
filename = path + 'owid-covid-data.csv'
filename_country_codes = path + 'country_codes.csv'
filename_out = path + 'cleaned.csv'
df = pd.read_csv(filename)
df_country_codes = pd.read_csv(filename_country_codes)
print(df.head())
columns = ['iso_code', 'country', 'updated', 'total_cases', 'confirmed',
       'total_deaths', 'deaths', 'total_cases_per_million',
       'new_cases_per_million', 'total_deaths_per_million',
       'new_deaths_per_million', 'total_tests', 'new_tests',
       'total_tests_per_thousand', 'new_tests_per_thousand', 'tests_units']
df.columns = columns

print(df.columns)
columns = ['iso_code', 'country', 'updated', 'confirmed', 'deaths']
coutries_codes = set(['USA', 'RUS', 'MEX', 'JOR', 'CHN', 'GBR', 'FRA'])
print('set: coutries_codes:', coutries_codes)
df = df[columns]
print(df.head())
df['updated']= pd.to_datetime(df['updated'])
df['updated'] = df['updated'].dt.strftime('%m/%d/%y')
print(df.head())

del_count = 0
for index, row in df.iterrows():
    mm = row['updated'][:2]

    # if row['iso_code'] not in coutries_codes or mm != '04': #row['confirmed'] < 1 and row['deaths'] < 1:
    if mm != '04': #row['confirmed'] < 1 and row['deaths'] < 1:
        df.drop(index, inplace=True)
        del_count += 1
        # print('drop index', index)
    
    # if index < 5:
    #     mm = row['updated'][:2]
    #     print(mm)
    #     break

print('number of deleted records', del_count)
df.to_csv(filename_out, index=False)