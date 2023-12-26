# %%
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import learning_curve, cross_val_score
from sklearn.preprocessing import PolynomialFeatures
from xgboost import XGBRegressor
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import ElasticNet
from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from numpy.random import uniform
from sklearn.datasets import make_blobs
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, MinMaxScaler, StandardScaler
from sklearn.preprocessing import OrdinalEncoder
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

from initdb import connection

MYSQL_TABLE_NAME = 'laptops'

def read_df_from_mysql():
    cursor = connection.cursor()
    cursor.execute(f'''
    SELECT 
    price, cpu, ram, ssd, graphic, screen_size, hdd, company, redirect_url
    FROM {MYSQL_TABLE_NAME}
    ''')
    result = cursor.fetchall()

    df = pd.DataFrame(result, columns=[
        'price', 'cpu', 'ram', 'ssd', 'graphic_ram', 'screen_size', 'hdd', 'company', 'redirect_urls'
    ])
    df["stock_status"] = "new"
    return df

def column_index(df, query_cols):
    cols = df.columns.values
    sidx = np.argsort(cols)
    return sidx[np.searchsorted(cols, query_cols, sorter=sidx)]


def turn_into_input(cpu, ram, ssd, graphic_ram, screen_size, stock_status, hdd, company, X_train):
    final_data = np.asarray(X_train)[9]
    for i in range(27):
        final_data[i] = 0
    final_data[0] = ram
    final_data[1] = ssd
    final_data[2] = graphic_ram
    final_data[3] = screen_size
    final_data[4] = hdd
    CPU_INDEX = column_index((X_train), [cpu])
    final_data[CPU_INDEX] = 1
    SS_INDEX = column_index((X_train), [stock_status])
    final_data[SS_INDEX] = 1
    COMPANY_INDEX = column_index((X_train), [company])
    final_data[COMPANY_INDEX] = 1
    return [final_data]


def find_my_best_match(point, features):
    targets = []
    i = 1
    for x in np.asarray(features):
        print(f"point: {point}")
        print(f"X : {x}")
        num = cosine_similarity(np.asarray(point), [np.asarray(x)])
        targets.append((i, abs(num)))
        i = i + 1
    return sorted(targets, key=lambda x: x[1][0][0], reverse=True)

def preprocess(df):
    one_hot = pd.get_dummies(df['cpu'])
    df = df.drop('cpu', axis=1).drop('redirect_urls', axis=1)
    df = df.join(one_hot)

    one_hot = pd.get_dummies(df['stock_status'])
    df = df.drop('stock_status', axis=1)
    df = df.join(one_hot)

    one_hot = pd.get_dummies(df['company'])
    df = df.drop('company', axis=1)
    df = df.join(one_hot)

    minvalue_series = df.min()

    df = df.astype({'price': 'int'})
    df.loc[:, 'price'] /= 100000

    y = df['price'].to_numpy()
    target = y
    X = df.drop('price', axis=1)
    features = X
    
    return features, target

def find_matches(cpu, ram, ssd, graphic_ram, screen_size, stock_status, hdd, company):
    df = read_df_from_mysql()
    result_df = df.copy()
    features, target = preprocess(df)

    request = turn_into_input(cpu, ram, ssd, graphic_ram, 
                              screen_size, stock_status, hdd, company, features)
    return find_my_best_match(request, features), result_df
