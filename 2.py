import pandas as pd
import numpy as np
import requests
import json
import boto3, os
import matplotlib.pyplot as plt



months = ['01','02','03','04','05','06','07','08','09', '10','11','12']
dfs = []
bucket = 'sacredbucket1'
s3_resource = boto3.resource('s3')
s3_client = boto3.client('s3')


for i in months:
    link = f'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?date=2021{i}01&json'
    resp = requests.get(url=link)
    data = resp.json()
    pd.json_normalize(data).to_csv(f'exchange_{i}.csv')
    s3_resource.meta.client.upload_file(f'exchange_{i}.csv', bucket, f'exchange_{i}.csv')

for i in months:
    obj = s3_client.get_object(Bucket=bucket, Key=f'exchange_{i}.csv')
    df = pd.read_csv(obj['Body'])
    dfs.append(df) 
res=pd.concat(dfs)

usd = res[res['cc'] == 'USD']
eur = res[res['cc'] == 'EUR']

x_usd =[i for i in months]
x_eur =[i for i in months]
y_usd = np.array(usd['rate'])
y_eur = np.array(eur['rate'])
plt.plot(x_usd,y_usd,label='usd')
plt.plot(x_eur,y_eur,label='eur')
plt.title('UAH to ')
plt.legend()
plt.show
plt.savefig('1.png')

s3_resource.meta.client.upload_file('1.png', bucket, '1.png')