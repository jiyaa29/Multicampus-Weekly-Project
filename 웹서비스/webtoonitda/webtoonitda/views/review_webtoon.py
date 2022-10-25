# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.0
#   kernelspec:
#     display_name: nlp
#     language: python
#     name: nlp
# ---

# +
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
plt.rc('font', family='NanumGothic')
import os
import time
from glob import glob

pd.set_option("display.max_rows", 1000)
pd.set_option("display.max_columns", 1000)
pd.options.display.float_format = '{:.2f}'.format
# -

# +
def get_reviews(title, USE_CSV_FILE):
    """
    워드 클라우드 키워드 반환하는 함수
    """
    DATA_DIR = os.getcwd() + "/media/"

    if USE_CSV_FILE:
        print("Read csv file.")
        filepath = DATA_DIR + "omniscient-reader_Episode_kr_21.csv"
        df = pd.read_csv(filepath)

    test = df[df['Review'].str.contains(title)] #df에 title파라미터 받음
    a=test.sample(5) #원하는 개수만큼 추출
    print(a)

    return a


# def get_top10_num_reviews(chromedriver_path, platform, lang, titleId, num_episodes, USE_CSV_FILE):
#     """
#     댓글 개수가 높은 에피소드 top10을 반환하는 함수
#     """
#     DATA_DIR = os.getcwd() + "/media/"
#
#     if USE_CSV_FILE:
#         print("Read csv file.")
#         filepath = DATA_DIR + "kr_전지적 독자 시점_num_reviews.csv"
#         df = pd.read_csv(filepath)
#     else:
#         df = get_num_reviews(chromedriver_path, lang, titleId, num_episodes, DATA_DIR)
#
#     df_top10 = df.sort_values(by=['Num_reviews', 'Episode'], ascending=False)
#     df_top10 = df_top10.drop(['Num_pages'], axis=1)
#     df_top10 = df_top10.set_index(keys='Episode', drop=True)
#     print(df_top10[:10])
#
#     return df_top10[:10]

